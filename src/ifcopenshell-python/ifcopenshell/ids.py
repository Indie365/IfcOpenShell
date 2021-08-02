import re
import logging
import operator
import os
import csv

import ifcopenshell.util.element

from bcf.v2.bcfxml import BcfXml
from bcf.v2.data import Topic, Viewpoint
from bcf import bcfxml

from xmlschema import XMLSchema
from xmlschema import XMLSchemaConverter
from xmlschema import etree_tostring
from lxml import etree as ElementTree
from xmlschema.validators import facets
from xmlschema.validators import identities

ids_schema = XMLSchema("http://standards.buildingsmart.org/IDS/ids_04.xsd")


def error(msg):
    raise Exception(msg)


class facet_evaluation:
    """
    The evaluation of a facet with data from IFC. Converts to bool and has a human readable string format.
    """

    def __init__(self, success, str):
        self.success = success
        self.str = str

    def __bool__(self):
        return self.success

    def __str__(self):
        return self.str


class meta_facet(type):
    """
    A metaclass for automatically registering facets in a map to be instantiated based on XML tagnames.
    """

    facets = {}

    def __new__(cls, clsname, bases, attrs):
        newclass = super(meta_facet, cls).__new__(cls, clsname, bases, attrs)
        meta_facet.facets[clsname] = newclass
        return newclass


class facet(metaclass=meta_facet):
    """
    The base class for IDS facets. IDS facets are functors constructed from
    XML nodes that return True or False. A getattr method is provided for
    conveniently extracting XML child node text content.
    """

    def __init__(self, node=None, location=None):
        if node:
            self.node = node
            if "@location" in self:
                self.location = self.node["@location"]
            else:
                self.location = "any"
        if location:
            self.location = location
        else:
            self.location = "any"

    def __getattr__(self, k):
        if k in self.node:
            v = self.node[k]
            if 'simpleValue' in v.keys():
                return v['simpleValue']
            else:   # is restriction
                return restriction( v["restriction"][0] )
                # TODO handle more than one restriction: return [restriction(r) for r in v["restriction"]]
        else:
            return None

    def __iter__(self):
        for k in self.parameters:
            yield k, getattr(self, k)

    def __str__(self):
        di = dict(list(self))
        for k, v in di.items():
            if isinstance(v, str) and not len(v):
                di[k] = "not specified"
        return self.message % di


class entity(facet):
    """
    The IDS entity facet currently *with* inheritance
    """

    parameters = ["name", "predefinedtype"]

    @staticmethod
    def create(name=None, predefinedtype=None):
        inst = entity()
        inst.name = name
        inst.predefinedtype = predefinedtype
        return inst

    def asdict(self):
        fac_dict = {"name": {'simpleValue': self.name}}
        if "predefinedtype" in self:
            fac_dict["predefinedtype"] = self.predefinedtype
        return fac_dict

    def __call__(self, inst, logger):
        # @nb with inheritance
        if self.predefinedtype and hasattr(inst, "PredefinedType"):
            self.message = "an entity name '%(name)s' of predefined type '%(predefinedtype)s'"
            return facet_evaluation(
                inst.is_a(self.name) and inst.PredefinedType == self.predefinedtype,
                self.message % {"name": inst.is_a(), "predefinedtype": inst.PredefinedType},
            )
        else:
            self.message = "an entity name '%(name)s'"
            return facet_evaluation(inst.is_a(self.name), self.message % {"name": inst.is_a()})


class classification(facet):
    """
    The IDS classification facet by traversing the HasAssociations inverse attribute
    """

    parameters = ["system", "value", "location"]
    message = "%(location)sclassification reference %(value)s from '%(system)s'"

    @staticmethod
    def create(location="any", value=None, system=None):
        inst = classification()
        inst.location = location
        inst.value = value
        inst.system = system
        return inst

    def asdict(self):
        fac_dict = {
            "value": {'simpleValue': self.value}, 
            "system": {'simpleValue': self.system},
            "@location": self.location, 
            # "instructions": "SAMPLE_INSTRUCTIONS",
        }
        return fac_dict

    def __call__(self, inst, logger):

        instance_classiciations = inst.HasAssociations
        if ifcopenshell.util.element.get_type(inst):
            type_classifications = ifcopenshell.util.element.get_type(inst).HasAssociations
        else:
            type_classifications = ()

        if self.location == "instance" and instance_classiciations:
            associations = instance_classiciations
        elif self.location == "type" and type_classifications:
            associations = type_classifications
        elif self.location == "any" and (instance_classiciations or type_classifications):
            associations = instance_classiciations + type_classifications
        else:
            associations = ()

        refs = []
        for association in associations:
            if association.is_a("IfcRelAssociatesClassification"):
                cref = association.RelatingClassification
                if hasattr(cref, "ItemReference"):  # IFC2x3
                    refs.append((cref.ReferencedSource.Name, cref.ItemReference))
                elif hasattr(cref, "Identification"):  # IFC4
                    refs.append((cref.ReferencedSource.Name, cref.Identification))

        self.location_msg = location[self.location]

        if refs:
            return facet_evaluation(
                (self.system, self.value) in refs,
                self.message
                % {
                    "system": refs[0][0],
                    "value": "'" + refs[0][1] + "'",
                    "location": self.location_msg,
                },  # what if not first item of refs?
            )
        else:
            return facet_evaluation(False, "does not have %sclassification reference" % self.location_msg)


class property(facet):
    """
    The IDS property facet implemented using `ifcopenshell.util.element`
    """

    parameters = ["name", "propertyset", "value", "location"]
    message = "%(location)sproperty '%(name)s' in '%(propertyset)s' with a value %(value)s"

    @staticmethod
    def create(location="any", propertyset=None, name=None, value=None):
        inst = property()
        inst.location = location
        inst.propertyset = propertyset
        inst.name = name
        inst.value = value
        # cls.attributes = {'@location': location} # 'type', 'instance', 'any'
        # BUG '@href': 'http://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/FireRating', #https://identifier.buildingsmart.org/uri/something
        # BUG 'instructions': 'Please add the desired rating.',
        return inst

    def asdict(self):
        fac_dict = {
            "@location": self.location,
            "propertyset": {'simpleValue': self.propertyset},
            "name": {'simpleValue': self.name},
            "value": {'simpleValue': self.value},
            # "instructions": "SAMPLE_INSTRUCTIONS",
            # TODO '@href': 'http://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/FireRating', #https://identifier.buildingsmart.org/uri/something
        }
        return fac_dict

    def __call__(self, inst, logger):

        self.location = self.node["@location"]

        instance_props = ifcopenshell.util.element.get_psets(inst)

        if ifcopenshell.util.element.get_type(inst):
            type_props = ifcopenshell.util.element.get_psets(ifcopenshell.util.element.get_type(inst))
        else:
            type_props = {}

        if self.location == "instance":
            props = instance_props
        elif self.location == "type" and type_props:
            props = type_props
        elif self.location == "any" and (instance_props or type_props):
            props = {**instance_props, **type_props}
        else:
            props = {}

        pset = props.get(self.propertyset)
        val = pset.get(self.name) if pset else None

        self.location_msg = location[self.location]
        di = {"name": self.name, "propertyset": self.propertyset, "value": "'%s'" % val, "location": self.location_msg}

        if val is not None:
            msg = self.message % di
        else:
            if pset:
                msg = "does not have %(location)sproperty '%(name)s' in a set '%(propertyset)s'" % di
            else:
                msg = "does not have %(location)sset '%(propertyset)s'" % di

        return facet_evaluation(val == self.value, msg)


class material(facet):
    """
    The IDS material facet by traversing the HasAssociations inverse attribute
    """

    parameters = ["value", "location"]
    message = "%(location)smaterial '%(value)s'"

    @staticmethod
    def create(location="any", value=None):
        inst = material()
        inst.location = location
        inst.value = value
        #     self.attributes = {'@location': location} # 'type', 'instance', 'any'
        #     # BUG '@use': 'optional'
        #     # BUG '@href': 'https://identifier.buildingsmart.org/uri/something',
        #     # BUG 'instructions': 'Please add the desired...',
        return inst

    def asdict(self):
        fac_dict = {
            "value": {'simpleValue': self.value},
            "@location": self.location,
            # "instructions": "SAMPLE_INSTRUCTIONS",
            # TODO '@href': 'http://identifier.buildingsmart.org/uri/buildingsmart/ifc-4.3/prop/FireRating', #https://identifier.buildingsmart.org/uri/something
            # TODO '@use': 'optional'
        }
        return fac_dict

    def __call__(self, inst, logger):

        self.location = self.node["@location"]

        instance_material_rel = [rel for rel in inst.HasAssociations if rel.is_a("IfcRelAssociatesMaterial")]
        if ifcopenshell.util.element.get_type(inst):
            type_material_rel = [
                rel
                for rel in ifcopenshell.util.element.get_type(inst).HasAssociations
                if rel.is_a("IfcRelAssociatesMaterial")
            ]
        else:
            type_material_rel = []

        if self.location == "instance":
            material_relations = list(instance_material_rel)
        elif self.location == "type" and type_material_rel:
            material_relations = list(type_material_rel)
        elif self.location == "any" and (instance_material_rel or type_material_rel):
            material_relations = instance_material_rel + type_material_rel
        else:
            material_relations = []

        materials = []
        for rel in material_relations:
            if rel.RelatingMaterial.is_a() == "IfcMaterial":
                materials.append(rel.RelatingMaterial.Name)
            elif rel.RelatingMaterial.is_a() == "IfcMaterialMaterialList":  # DEPRECATED in IFC4
                [materials.append(mat.Name) for mat in rel.RelatingMaterial]
            elif rel.RelatingMaterial.is_a() == "IfcMaterialConstituentSet":
                [materials.append(mat.Material.Name) for mat in rel.RelatingMaterial.MaterialConstituents]
            elif rel.RelatingMaterial.is_a() == "IfcMaterialLayerSet":
                [materials.append(mat.Name) for mat in rel.RelatingMaterial.MaterialLayers]
            elif rel.RelatingMaterial.is_a() == "IfcMaterialLayerSetUsage":
                layers = rel.RelatingMaterial.ForLayerSet.MaterialLayers
                [materials.append(layer.Material.Name) for layer in layers]
            elif rel.RelatingMaterial.is_a() == "IfcMaterialProfileSet":
                [materials.append(mat.Material.Name) for mat in rel.RelatingMaterial.MaterialProfiles]
            elif rel.RelatingMaterial.is_a() == "IfcMaterialProfileSetUsage":
                profileSets = rel.RelatingMaterial.ForProfileSet.MaterialProfiles
                [materials.append(pset.Material.Name) for pset in profileSets]
            else:
                print("IfcRelAssociatesMaterial not implemented")

        if not materials:
            materials.append("UNDEFINED")

        self.location_msg = location[self.location]

        return facet_evaluation(
            self.value in materials,
            self.message % {"value": "'/'".join(materials), "location": self.location_msg},
        )


class boolean_logic:
    """
    Boolean conjunction over a collection of functions
    """

    def __init__(self, terms):
        self.terms = terms

    def __call__(self, *args):
        eval = [t(*args) for t in self.terms]
        join = [" and ", " or "][self.fold == any]
        return facet_evaluation(self.fold(eval), join.join(map(str, eval)))

    def __str__(self):
        return [" and ", " or "][self.fold == any].join(map(str, self.terms))


class boolean_and(boolean_logic):
    fold = all


class boolean_or(boolean_logic):
    fold = any


class restriction:
    """
    The value restriction from XSD implemented as a list of values and a containment test
    """

    def __init__(self, node=None):

        self.type = ""
        self.options = []

        if node:
            self.restriction_on = node["@base"][3:]
            for n in node:
                if n == "enumeration":
                    self.type = "enumeration"
                    for x in node[n]:
                        self.options.append(x["@value"])
                elif n[-7:] == "clusive":
                    self.type = "bounds"
                    self.options.append({n: node[n]["@value"]})
                elif n[-5:] == "ength":
                    self.type = "length"
                    if n[3:6] == "min":
                        self.options.append(">=")
                    elif n[3:6] == "max":
                        self.options.append("<=")
                    else:
                        self.options.append("==")
                    self.options[-1] += str(node[n]["@value"])
                elif n == "pattern":
                    self.type = "pattern"
                    self.options.append(node[n]["@value"])
                # TODO add fractionDigits
                # TODO add totalDigits
                # TODO add whiteSpace
                elif n == "@base":
                    pass
                else:
                    print("Error! Restriction not implemented")

    @staticmethod
    def create(options, type='', restriction_on='string'):
        """ 
        type:           enumeration/pattern/bounds
        restriction_on: string/boolean/decimal/integer
        options:        list if enumeration
                        regex string if pattern
                        if bounds dict with possible keys: minInclusive, maxInclusive, minExclusive, maxExclusive
        """
        rest = restriction()
        if type in ["enumeration", "pattern", "bounds"]:
            rest.type = type
            rest.restriction_on = restriction_on
            if type == 'enumeration' and isinstance(options, list):
                rest.options = options
            elif type == 'pattern' and isinstance(options, str):
                rest.options = options
            elif type == 'bounds' and isinstance(options, dict):
                for option in options:
                    if option in ['minInclusive', 'maxInclusive', 'minExclusive', 'maxExclusive']:
                        rest.options.append( {option: options[option]} )
            else:
                Exception("Options were not properly defined.")
            return rest
        else:
            raise Exception("Such restriction not implemented. Try: 'enumeration', 'pattern' or 'min/maxInclusive' or 'min/maxExclusive'.")


    def __eq__(self, other):
        result = False
        # TODO implement data type comparison
        if self and (other or other == 0):
            if self.type == "enumeration" and self.restriction_on == "bool":
                self.options = [x.lower() for x in self.options]
                result = str(other).lower() in self.options
            elif self.type == "enumeration":
                result = other in self.options
            elif self.type == "bounds":
                result = True
                for option in self.options:
                    sign = list(option.keys())[0]
                    if sign == 'minInclusive' and other < option[sign]:
                        result = False
                    elif sign == 'maxInclusive' and other > option[sign]:
                        result = False
                    elif sign == 'minExclusive' and other <= option[sign]:
                        result = False
                    elif sign == 'maxExclusive' and other >= option[sign]:
                        result = False
            elif self.type == "length":
                for op in self.options:
                    if eval(str(len(other)) + op):  # TODO eval not safe?
                        result = True
            elif self.type == "pattern":
                translated_pattern = identities.translate_pattern(self.options)
                regex_pattern = re.compile(translated_pattern)
                if regex_pattern.fullmatch(other) is not None:
                    result = True
            # TODO add fractionDigits
            # TODO add totalDigits
            # TODO add whiteSpace
        return result

    def __repr__(self):
        if self.type == "enumeration":
            return "'%s'" % "' or '".join(self.options)
        elif self.type == "bounds":
            return "of type '%s', having a value %s" % (self.restriction_on, " and ".join([bounds[list(x.keys())[0]] + str( x[list(x.keys())[0]] ) for x in self.options]))
        elif self.type == "length":
            return "of type '%s' with %s letters" % (self.restriction_on, " and ".join(self.options))
        elif self.type == "pattern":
            return "of type '%s' respecting pattern '%s'" % (self.restriction_on, " and ".join(self.options))
        # TODO add fractionDigits
        # TODO add totalDigits
        # TODO add whiteSpace


class specification:
    """
    Represents the XML <specification> node and its two children <applicability> and <requirements>
    """

    def __init__(self, name="Specification", necessity="required"):
        self.name = name
        self.applicability = None
        self.requirements = None
        self.necessity = necessity

    def asdict(self):
        # if older python collections.OrderedDict()
        spec_dict = {
            "@name": self.name,
            "@necessity": self.necessity,
            "applicability": {},
            "requirements": {},
        }
        for x in ["applicability", "requirements"]:
            for fac in (getattr(self, x)).terms:
                fclass = type(fac).__name__
                if fclass in spec_dict[x]:
                    spec_dict[x][fclass].append(fac.asdict())
                else:
                    spec_dict[x][fclass] = [fac.asdict()]
        return spec_dict

    @staticmethod
    def parse(ids_dict):
        def parse_rules(dict):
            facet_names = list(dict.keys())
            facet_properties = [v[0] if isinstance(v, list) else v for v in list(dict.values())]
            classes = [meta_facet.facets.__getitem__(f) for f in facet_names]
            facets = [cls(n) for cls, n in zip(classes, facet_properties)]
            return facets

        spec = specification()
        spec.name = ids_dict["@name"]
        spec.necessity = ids_dict["@necessity"]
        spec.applicability = boolean_and(parse_rules(ids_dict["applicability"]))
        spec.requirements = boolean_and(parse_rules(ids_dict["requirements"]))
        return spec

    def add_applicability(self, facet):
        """
        Applicability specifies what conditions must be meet for an IFC object to be used for validation.
        Takes: entity, classification, property or material objects as an input (at least one entity is required).
        """
        if self.applicability:
            self.applicability = boolean_and(self.applicability.terms + [facet])
        else:
            self.applicability = boolean_and([facet])

    def add_requirement(self, facet):
        """
        Requirement is validated on all applicable IFC elements.
        Takes: entity, classification, property or material objects as an input (at least one of them is required).
        """
        if self.requirements:
            self.requirements = boolean_and(self.requirements.terms + [facet])
        else:
            self.requirements = boolean_and([facet])

    def __call__(self, inst, logger):
        if self.applicability(inst, logger):

            valid = self.requirements(inst, logger)

            if valid:
                logger.info(
                    {
                        "guid": inst.GlobalId,
                        "result": valid.success,
                        "sentence": str(self)
                        + ".\n"
                        + inst.is_a()
                        + " '"
                        + str(inst.Name)
                        + "' (#"
                        + str(inst.id())
                        + ") has "
                        + str(valid)
                        + " so is compliant",
                    }
                )
                return True, True
            else:
                # BUG "has does not have"
                logger.error(
                    {
                        "guid": inst.GlobalId,
                        "result": valid.success,
                        "sentence": str(self)
                        + ".\n"
                        + inst.is_a()
                        + " '"
                        + str(inst.Name)
                        + "' (#"
                        + str(inst.id())
                        + ") has "
                        + str(valid)
                        + " so is not compliant",
                    }
                )
                return True, False
        else:
            return False, False

    def __str__(self):
        return "Given an instance with %(applicability)s\nWe expect %(requirements)s" % self.__dict__


class ids:
    """
    Represents the XML root <ids> node and its <specification> childNodes.
    """

    def __init__(self):
        self.specifications = []
        self.info = None  # TODO ifcversion, description, author, copyright, version, date, purpose, milestone

    def asdict(self):
        ids_dict = {
            "@xmlns": "http://standards.buildingsmart.org/IDS",
            "@xmlns:xs": "http://www.w3.org/2001/XMLSchema",
            "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "@xsi:schemaLocation": "http://standards.buildingsmart.org/IDS/ids_04.xsd",
            "specification": [],
            "info": self.info,
        }
        for spec in self.specifications:
            ids_dict["specification"].append(spec.asdict())
        return ids_dict

    def to_xml(self, fn="./", ids_schema=ids_schema):
        if fn.endswith("/"):
            fn = fn + "IDS"
        if not fn.endswith(".xml"):
            fn = fn + ".xml"

        ids_dict = self.asdict()

        ids_xml = ids_schema.encode(
            ids_dict,
            namespaces={
                "": "http://standards.buildingsmart.org/IDS",
                "xs": "http://www.w3.org/2001/XMLSchema",
                "xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:schemaLocation": "http://standards.buildingsmart.org/IDS/ids_04.xsd",
            },
        )  # validation='skip',

        ids_str = etree_tostring(
            ids_xml,
            namespaces={
                "": "http://standards.buildingsmart.org/IDS",
                # 'xs': 'http://www.w3.org/2001/XMLSchema',
                # 'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                # 'xsi:schemaLocation': "http://standards.buildingsmart.org/IDS/ids_04.xsd"
            },
        )

        with open(fn, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write("<!-- IDS (INFORMATION DELIVERY SPECIFICATION) CREATED USING IFCOPENSHELL -->\n")
            f.write(ids_str)
            f.close()

        # ids_schema.validate(fn)
        return ids_schema.is_valid(fn)

    @staticmethod
    def parse(fn, ids_schema=ids_schema):
        ids_schema.validate(fn)
        ids_content = ids_schema.decode(fn, strip_namespaces=True, namespaces={"": "http://standards.buildingsmart.org/IDS"})
        new_ids = ids()
        new_ids.specifications = [specification.parse(s) for s in ids_content["specification"]]
        return new_ids

    def validate(self, ifc_file, logger):
        # TODO should we do other way around: for elem, for spec so we can see if an element pass all IDSes?
        self.ifc_checked = 0
        self.ifc_passed = 0
        for spec in self.specifications:
            for elem in ifc_file.by_type("IfcObject"):
                apply, comply = spec(elem, logger)
                if apply:
                    self.ifc_checked += 1
                if comply:
                    self.ifc_passed += 1
        for h in logger.handlers:
            h.flush()


class SimpleHandler(logging.StreamHandler):
    def __init__(self, report_valid=False):
        logging.StreamHandler.__init__(self)
        self.statements = []
        if report_valid:
            self.setLevel(logging.INFO)
        else:
            self.setLevel(logging.ERROR)

    def emit(self, mymsg):
        self.statements.append(mymsg.msg)


class BcfHandler(logging.StreamHandler):
    def __init__(self, project_name="Default IDS Project", author="your@email.com", filepath=None, report_valid=False):
        logging.StreamHandler.__init__(self)
        if report_valid:
            self.setLevel(logging.INFO)
        else:
            self.setLevel(logging.ERROR)
        self.bcf = BcfXml()
        self.bcf.author = author
        self.bcf.new_project()
        self.bcf.project.name = project_name
        self.filepath = filepath

    def emit(self, mymsg):
        newtopic = Topic()
        newtopic.title = mymsg.msg["sentence"].split(".\n")[1]
        newtopic.description = mymsg.msg["sentence"].split(".\n")[0]

        # TODO
        # newviewpoint = Viewpoint()
        # TODO add references in Topic
        self.bcf.add_topic(newtopic)
        self.bcf.edit_project()

    def flush(self):
        if not self.filepath:
            self.filepath = os.getcwd() + r"\IDS_report.bcfzip"
        if not (self.filepath.endswith(".bcf") or self.filepath.endswith(".bcfzip")):
            self.filepath = self.filepath + r"\IDS_report.bcfzip"
        self.bcf.save_project(self.filepath)



location = {"instance": "an instance ", "type": "a type ", "any": "a "}
bounds = {
    "minInclusive": "larger or equal ",
    "maxInclusive": "smaller or equal ",
    "minExclusive": "larger than ",
    "maxExclusive": "smaller than ",
}

if __name__ == "__main__":
    import time

    start_time = time.time()
    import sys, os
    import ifcopenshell
    from datetime import date

    # filename = os.path.join(os.getcwd(), 'IDS results/'+str(date.today())+"_ids_result.txt")
    filename = (
        "C:/Users/arturbt/Desktop/OneDrive - NTNU/Code/Ifc_sandbox/ifc_experiments/"
        + "IDS results/"
        + str(date.today())
        + "_ids_result.txt"
    )

    logger = logging.getLogger("IDS")
    logging.basicConfig(filename=filename, level=logging.INFO, format="%(message)s")
    logging.FileHandler(filename, mode='w')

    ids_file = ids.parse(sys.argv[1])
    ifc_file = ifcopenshell.open(sys.argv[2])

    ids_file.validate(ifc_file, logger)
