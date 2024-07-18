# BlenderBIM Add-on - OpenBIM Blender Add-on
# Copyright (C) 2020, 2021 Dion Moult <dion@thinkmoult.com>
#
# This file is part of BlenderBIM Add-on.
#
# BlenderBIM Add-on is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BlenderBIM Add-on is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BlenderBIM Add-on.  If not, see <http://www.gnu.org/licenses/>.

import bpy
from ifcopenshell.util.doc import get_entity_doc
import blenderbim.tool as tool
from .data import MaterialsData, ObjectMaterialData
from ...ifc import IfcStore
from ...prop import StrProperty, Attribute
from bpy.types import PropertyGroup
from bpy.props import (
    PointerProperty,
    StringProperty,
    EnumProperty,
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    CollectionProperty,
)

materialtypes_enum = []
profileclasses_enum = []
parameterizedprofileclasses_enum = []


def purge():
    global materialtypes_enum
    global profileclasses_enum
    global parameterizedprofileclasses_enum
    materialtypes_enum = []
    profileclasses_enum = []
    parameterizedprofileclasses_enum = []


def get_profile_classes(self, context):
    global profileclasses_enum
    if len(profileclasses_enum) == 0 and IfcStore.get_schema():
        version = tool.Ifc.get_schema()
        profileclasses_enum.clear()
        profileclasses_enum = [
            (t.name(), t.name(), get_entity_doc(version, t.name()).get("description", ""))
            for t in IfcStore.get_schema().declaration_by_name("IfcProfileDef").subtypes()
        ]
    return profileclasses_enum


def get_parameterized_profile_classes(self, context):
    global parameterizedprofileclasses_enum
    if len(parameterizedprofileclasses_enum) == 0 and IfcStore.get_schema():
        version = tool.Ifc.get_schema()
        parameterizedprofileclasses_enum.clear()
        parameterizedprofileclasses_enum = [
            (t.name(), t.name(), get_entity_doc(version, t.name()).get("description", ""))
            for t in IfcStore.get_schema().declaration_by_name("IfcParameterizedProfileDef").subtypes()
        ]
        for ifc_class in parameterizedprofileclasses_enum:
            parameterizedprofileclasses_enum.extend(
                [
                    (t.name(), t.name(), get_entity_doc(version, t.name()).get("description", ""))
                    for t in IfcStore.get_schema().declaration_by_name(ifc_class[0]).subtypes() or []
                ]
            )
    return parameterizedprofileclasses_enum


def get_materials(self, context):
    if not ObjectMaterialData.is_loaded:
        ObjectMaterialData.load()
    return ObjectMaterialData.data["materials"]


def get_object_material_type(self, context):
    if not ObjectMaterialData.is_loaded:
        ObjectMaterialData.load()
    return ObjectMaterialData.data["material_type"]


def get_material_types(self, context):
    if not MaterialsData.is_loaded:
        MaterialsData.load()
    return MaterialsData.data["material_types"]


def update_material_type(self, context):
    MaterialsData.data["total_materials"] = MaterialsData.total_materials()


def get_profiles(self, context):
    if not MaterialsData.is_loaded:
        MaterialsData.load()
    return MaterialsData.data["profiles"]


def get_styles(self, context):
    if not MaterialsData.is_loaded:
        MaterialsData.load()
    return MaterialsData.data["styles"]


def get_contexts(self, context):
    if not MaterialsData.is_loaded:
        MaterialsData.load()
    return MaterialsData.data["contexts"]


def update_material_name(self: "Material", context: bpy.types.Context) -> None:
    ifc_file = tool.Ifc.get()
    name = self.name
    material = ifc_file.by_id(self.ifc_definition_id)
    if material.is_a("IfcMaterialLayerSet"):
        material.LayerSetName = name
    else:
        material.Name = name


class Material(PropertyGroup):
    name: StringProperty(name="Name", update=update_material_name)
    ifc_definition_id: IntProperty(name="IFC Definition ID")
    is_category: BoolProperty(name="Is Category", default=False)
    is_expanded: BoolProperty(name="Is Expanded", default=False)
    has_style: BoolProperty(name="Has Style", default=True)
    total_elements: IntProperty(name="Total Elements")


class BIMMaterialProperties(PropertyGroup):
    is_editing: BoolProperty(name="Is Editing", default=False)
    material_type: EnumProperty(items=get_material_types, update=update_material_type, name="Material Type")
    materials: CollectionProperty(name="Materials", type=Material)
    active_material_index: IntProperty(name="Active Material Index")
    profiles: EnumProperty(items=get_profiles, name="Profiles")
    active_material_id: IntProperty(name="Active Material ID")
    material_attributes: CollectionProperty(name="Material Attributes", type=Attribute)
    editing_material_type: StringProperty(name="Editing Material Type")
    styles: EnumProperty(items=get_styles, name="Styles")
    contexts: EnumProperty(items=get_contexts, name="Contexts")


class BIMObjectMaterialProperties(PropertyGroup):
    material_type: EnumProperty(items=get_object_material_type, name="Material Type")
    material: EnumProperty(items=get_materials, name="Material", description="Currently selected IfcMaterial")
    is_editing: BoolProperty(name="Is Editing", default=False)
    material_set_usage_attributes: CollectionProperty(name="Material Set Usage Attributes", type=Attribute)
    material_set_attributes: CollectionProperty(name="Material Set Attributes", type=Attribute)
    active_material_set_item_id: IntProperty(name="Active Material Set ID")
    material_set_item_attributes: CollectionProperty(name="Material Set Item Attributes", type=Attribute)
    material_set_item_profile_attributes: CollectionProperty(
        name="Material Set Item Profile Attributes", type=Attribute
    )
    material_set_item_material: EnumProperty(items=get_materials, name="Material")
    profile_classes: EnumProperty(items=get_profile_classes, name="Profile Classes")
    parameterized_profile_classes: EnumProperty(
        items=get_parameterized_profile_classes, name="Parameterized Profile Classes"
    )
