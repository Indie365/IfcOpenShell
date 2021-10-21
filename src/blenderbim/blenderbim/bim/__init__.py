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
import importlib
from . import handler, ui, prop, operator, helper

modules = {
    "project": None,
    "search": None,
    "bcf": None,
    "root": None,
    "unit": None,
    "model": None,
    "georeference": None,
    "context": None,
    "drawing": None,
    "misc": None,
    "attribute": None,
    "type": None,
    "spatial": None,
    "void": None,
    "aggregate": None,
    "geometry": None,
    "cobie": None,
    "resource": None,
    "cost": None,
    "sequence": None,
    "group": None,
    "system": None,
    "structural": None,
    "boundary": None,
    "profile": None,
    "material": None,
    "style": None,
    "layer": None,
    "owner": None,
    "pset": None,
    "qto": None,
    "classification": None,
    "constraint": None,
    "document": None,
    "pset_template": None,
    "clash": None,
    "lca": None,
    "csv": None,
    "bimtester": None,
    "diff": None,
    "patch": None,
    "covetool": None,
    "augin": None,
    "debug": None,
}

dynamic_operators = [] #temporary list to hold dynamically generated operators
module_dict = {} #dictionary which will be used to store the current state of each module (active/inactive)

for name in modules.keys():
    modules[name] = importlib.import_module(f"blenderbim.bim.module.{name}")

    name_uppercase = name.capitalize()
    module_dict[name_uppercase] = bpy.props.BoolProperty(name=name_uppercase, default=True)

    new_operator = helper.generate_operators(name, modules[name])
    dynamic_operators.append(new_operator)

#create a propertygroup that stores module state
module_propertygroup = type(
    "ModuleActiveState",
    (bpy.types.PropertyGroup,),
    {'__annotations__':module_dict}
)

classes = [
    operator.OpenUri,
    operator.SelectDataDir,
    operator.SelectSchemaDir,
    operator.SelectIfcFile,
    operator.OpenUpstream,
    operator.AddSectionPlane,
    operator.RemoveSectionPlane,
    operator.ReloadIfcFile,
    operator.AddIfcFile,
    operator.RemoveIfcFile,
    operator.ConfigureVisibility,
    prop.StrProperty,
    prop.Attribute,
    prop.BIMProperties,
    prop.IfcParameter,
    prop.PsetQto,
    prop.GlobalId,
    prop.BIMObjectProperties,
    prop.BIMMaterialProperties,
    prop.BIMMeshProperties,
    ui.BIM_PT_section_plane,
    ui.BIM_UL_generic,
    ui.BIM_UL_topics,
    ui.BIM_ADDON_preferences,
    module_propertygroup
]

classes.extend(dynamic_operators)

for mod in modules.values():
    classes.extend(mod.classes)


def on_register(scene):
    handler.setDefaultProperties(scene)
    bpy.app.handlers.depsgraph_update_post.remove(on_register)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.app.handlers.depsgraph_update_post.append(on_register)
    bpy.app.handlers.undo_pre.append(handler.undo_pre)
    bpy.app.handlers.undo_post.append(handler.undo_post)
    bpy.app.handlers.redo_pre.append(handler.redo_pre)
    bpy.app.handlers.redo_post.append(handler.redo_post)
    bpy.app.handlers.load_post.append(handler.setDefaultProperties)
    bpy.app.handlers.load_post.append(handler.loadIfcStore)
    bpy.app.handlers.save_pre.append(handler.ensureIfcExported)
    bpy.types.Scene.BIMProperties = bpy.props.PointerProperty(type=prop.BIMProperties)
    bpy.types.Object.BIMObjectProperties = bpy.props.PointerProperty(type=prop.BIMObjectProperties)
    bpy.types.Material.BIMObjectProperties = bpy.props.PointerProperty(type=prop.BIMObjectProperties)
    bpy.types.Material.BIMMaterialProperties = bpy.props.PointerProperty(type=prop.BIMMaterialProperties)
    bpy.types.Mesh.BIMMeshProperties = bpy.props.PointerProperty(type=prop.BIMMeshProperties)
    bpy.types.Curve.BIMMeshProperties = bpy.props.PointerProperty(type=prop.BIMMeshProperties)
    bpy.types.Camera.BIMMeshProperties = bpy.props.PointerProperty(type=prop.BIMMeshProperties)
    bpy.types.PointLight.BIMMeshProperties = bpy.props.PointerProperty(type=prop.BIMMeshProperties)
    bpy.types.SCENE_PT_unit.append(ui.ifc_units)
    bpy.types.Scene.module_state = bpy.props.PointerProperty(type= module_propertygroup)

    for mod in modules.values():
        mod.register()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    bpy.app.handlers.load_post.remove(handler.setDefaultProperties)
    bpy.app.handlers.load_post.remove(handler.loadIfcStore)
    bpy.app.handlers.save_pre.remove(handler.ensureIfcExported)
    del bpy.types.Scene.BIMProperties
    del bpy.types.Object.BIMObjectProperties
    del bpy.types.Material.BIMObjectProperties
    del bpy.types.Material.BIMMaterialProperties
    del bpy.types.Mesh.BIMMeshProperties
    del bpy.types.Curve.BIMMeshProperties
    del bpy.types.Camera.BIMMeshProperties
    del bpy.types.PointLight.BIMMeshProperties
    del bpy.types.Scene.module_state
    bpy.types.SCENE_PT_unit.remove(ui.ifc_units)

    for mod in reversed(list(modules.values())):
        mod.unregister()
