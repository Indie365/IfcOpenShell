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
import ifcopenshell.api
import blenderbim.tool as tool
import blenderbim.core.system as core
import blenderbim.bim.handler
from blenderbim.bim.ifc import IfcStore
from blenderbim.bim.module.system.data import PortData
from mathutils import Matrix


class Operator:
    def execute(self, context):
        IfcStore.execute_ifc_operator(self, context)
        blenderbim.bim.handler.refresh_ui_data()
        return {"FINISHED"}


class LoadSystems(bpy.types.Operator, Operator):
    bl_idname = "bim.load_systems"
    bl_label = "Load Systems"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.load_systems(tool.System)


class DisableSystemEditingUI(bpy.types.Operator, Operator):
    bl_idname = "bim.disable_system_editing_ui"
    bl_label = "Disable System Editing UI"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.disable_system_editing_ui(tool.System)


class AddSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.add_system"
    bl_label = "Add System"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.add_system(tool.Ifc, tool.System, ifc_class=context.scene.BIMSystemProperties.system_class)


class EditSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.edit_system"
    bl_label = "Edit System"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.edit_system(
            tool.Ifc, tool.System, system=tool.Ifc.get().by_id(context.scene.BIMSystemProperties.active_system_id)
        )


class RemoveSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.remove_system"
    bl_label = "Remove System"
    bl_options = {"REGISTER", "UNDO"}
    system: bpy.props.IntProperty()

    def _execute(self, context):
        core.remove_system(tool.Ifc, tool.System, system=tool.Ifc.get().by_id(self.system))


class EnableEditingSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.enable_editing_system"
    bl_label = "Enable Editing System"
    bl_options = {"REGISTER", "UNDO"}
    system: bpy.props.IntProperty()

    def _execute(self, context):
        core.enable_editing_system(tool.System, system=tool.Ifc.get().by_id(self.system))


class DisableEditingSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.disable_editing_system"
    bl_label = "Disable Editing System"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.disable_editing_system(tool.System)


class AssignSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.assign_system"
    bl_label = "Assign System"
    bl_options = {"REGISTER", "UNDO"}
    system: bpy.props.IntProperty()

    def _execute(self, context):
        for obj in context.selected_objects:
            element = tool.Ifc.get_entity(obj)
            if element:
                core.assign_system(tool.Ifc, system=tool.Ifc.get().by_id(self.system), product=element)


class UnassignSystem(bpy.types.Operator, Operator):
    bl_idname = "bim.unassign_system"
    bl_label = "Unassign System"
    bl_options = {"REGISTER", "UNDO"}
    system: bpy.props.IntProperty()

    def _execute(self, context):
        for obj in context.selected_objects:
            element = tool.Ifc.get_entity(obj)
            if element:
                core.unassign_system(tool.Ifc, system=tool.Ifc.get().by_id(self.system), product=element)


class SelectSystemProducts(bpy.types.Operator, Operator):
    bl_idname = "bim.select_system_products"
    bl_label = "Select System Products"
    bl_options = {"REGISTER", "UNDO"}
    system: bpy.props.IntProperty()

    def _execute(self, context):
        core.select_system_products(tool.System, system=tool.Ifc.get().by_id(self.system))


class ShowPorts(bpy.types.Operator, Operator):
    bl_idname = "bim.show_ports"
    bl_label = "Show Ports"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not PortData.is_loaded:
            PortData.load()
        if PortData.data["total_ports"] == 0:
            cls.poll_message_set("No ports found")
            return False
        return True

    def _execute(self, context):
        core.show_ports(tool.Ifc, tool.System, tool.Spatial, element=tool.Ifc.get_entity(context.active_object))


class HidePorts(bpy.types.Operator, Operator):
    bl_idname = "bim.hide_ports"
    bl_label = "Hide Ports"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return ShowPorts.poll(context)

    def _execute(self, context):
        core.hide_ports(tool.Ifc, tool.System, element=tool.Ifc.get_entity(context.active_object))


class AddPort(bpy.types.Operator, Operator):
    bl_idname = "bim.add_port"
    bl_description = "Add port at current cursor position"
    bl_label = "Add Port"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.add_port(tool.Ifc, tool.System, element=tool.Ifc.get_entity(context.active_object))


class RemovePort(bpy.types.Operator, Operator):
    bl_idname = "bim.remove_port"
    bl_label = "Remove Port"
    bl_options = {"REGISTER", "UNDO"}

    def _execute(self, context):
        core.remove_port(tool.Ifc, tool.System, port=tool.Ifc.get_entity(context.active_object))


class ConnectPort(bpy.types.Operator, Operator):
    bl_idname = "bim.connect_port"
    bl_label = "Connect Ports"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) == 2

    def _execute(self, context):
        obj1 = context.active_object
        obj2 = context.selected_objects[0] if context.selected_objects[1] == obj1 else context.selected_objects[1]
        core.connect_port(tool.Ifc, port1=tool.Ifc.get_entity(obj1), port2=tool.Ifc.get_entity(obj2))


class DisconnectPort(bpy.types.Operator, Operator):
    bl_idname = "bim.disconnect_port"
    bl_label = "Disconnect Ports"
    bl_options = {"REGISTER", "UNDO"}

    element_id: bpy.props.IntProperty(default=0, options={"SKIP_SAVE"})

    def _execute(self, context):
        if self.element_id != 0:
            element = tool.Ifc.get().by_id(self.element_id)
        else:
            element = tool.Ifc.get_entity(context.active_object)
        core.disconnect_port(tool.Ifc, port=element)


class MEPConnectElements(bpy.types.Operator, Operator):
    bl_idname = "bim.mep_connect_elements"
    bl_label = "Connect MEP Elements"
    bl_description = "Connects two selected elements by their closest located ports and adjusts them"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if not len(context.selected_objects) == 2:
            cls.poll_message_set("Need to select 2 objects.")
            return False
        return True

    def _execute(self, context):
        obj1 = context.active_object
        obj2 = next(o for o in context.selected_objects if o != obj1)

        el1 = tool.Ifc.get_entity(obj1)
        el2 = tool.Ifc.get_entity(obj2)

        connected_elements = ifcopenshell.util.system.get_connected_to(el1)
        connected_elements += ifcopenshell.util.system.get_connected_to(el2)

        if el2 in connected_elements:
            self.report({"ERROR"}, "MEP elements are already connected to each other.")
            return {"CANCELLED"}

        obj1_ports = [p for p in tool.System.get_ports(el1) if not tool.System.get_connected_port(p)]
        obj2_ports = [p for p in tool.System.get_ports(el2) if not tool.System.get_connected_port(p)]

        if not obj1_ports or not obj2_ports:
            self.report({"ERROR"}, "Couldn't find free ports to connect.")
            return {"CANCELLED"}

        ports_distance = dict()
        for port1 in obj1_ports:
            port1_location = tool.Model.get_element_matrix(port1).translation
            for port2 in obj2_ports:
                port2_location = tool.Model.get_element_matrix(port2).translation
                distance = (port1_location - port2_location).length
                ports_distance[(port1, port2)] = distance

        closest_ports = min(ports_distance, key=lambda x: ports_distance[x])
        core.connect_port(tool.Ifc, *closest_ports)
        bpy.ops.bim.regenerate_distribution_element()
        return {"FINISHED"}


class SetFlowDirection(bpy.types.Operator, Operator):
    bl_idname = "bim.set_flow_direction"
    bl_label = "Set Flow Direction"
    bl_options = {"REGISTER", "UNDO"}
    direction: bpy.props.StringProperty()

    def _execute(self, context):
        port = tool.Ifc.get_entity(context.active_object)
        second_port = tool.System.get_connected_port(port)
        if not second_port:
            self.report({"ERROR"}, "To set flow direction port has to be connected to another one.")
            return
        core.set_flow_direction(
            tool.Ifc, tool.System, port=tool.Ifc.get_entity(context.active_object), direction=self.direction
        )


class SelectSystemProductsByGuid(bpy.types.Operator, Operator):
    """Select All IFC Products in the IFC System"""
    bl_idname = "bim.select_system_products_by_guid"
    bl_label = "Select System Projects By Guid"
    
    guid: bpy.props.StringProperty(
      name = "",
      default = "")
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        ifcSystem = blenderbim.tool.Ifc.get().by_guid(self.guid)
        [obj.select_set(False) for obj in bpy.data.objects]
        blenderbim.tool.System.select_system_products(ifcSystem)
        return {'FINISHED'}


class GetIfcSystemInfoByGuid(bpy.types.Operator, Operator):
    """View IFC System Info"""
    bl_idname = "bim.get_ifc_system_info_by_guid"
    bl_label = "Get Ifc System Info By Guid"
    
    guid: bpy.props.StringProperty(
        name = "",
        default = "")

    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        ifcSystem = blenderbim.tool.Ifc.get().by_guid(self.guid)
        print(ifcSystem.get_info())
        #self.report({"INFO"}, "This is a test")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 300)
    
    def draw(self, context):
        ifcSystem = blenderbim.tool.Ifc.get().by_guid(self.guid)
        ifcSystemInfo = ifcSystem.get_info()
        self.row = self.layout
        for info in ifcSystemInfo:
            self.row = self.layout.split(factor = 0.3)
            self.row.label(text = info)
            self.row.label(text = str(ifcSystemInfo[info]))
            self.row = self.layout.row()


class IfcSystemEditingPanel(bpy.types.Operator, Operator):
    """Edit IFC System Info or Appearence"""
    bl_idname = "bim.ifc_system_editing_panel"
    bl_label = "Ifc System Editing Panel"
    
    guid: bpy.props.StringProperty(
        name = "",
        default = "")
    
    ifcSystemColor: bpy.props.FloatVectorProperty(
        name = "Color Picker",
        subtype = "COLOR",
        size = 4,
        min = 0.0,
        max = 1.0,
        default = (0,0,0,0) #Controlled by BIM_PT_systems_navigator_sub_panel
        )

    def execute(self, context):
        for relatedObj in self.ifcSystemProductList:
            entity = self.file.by_guid(relatedObj.GlobalId)
            obj = tool.Ifc.get_object(entity)
            if obj is not None:
                obj.color = self.ifcSystemColor
        return {'FINISHED'}
    
    def invoke(self, context, event):
        self.file = tool.Ifc.get()
        self.ifcSystem = self.file.by_guid(self.guid)
        self.commonColor = []
        self.ifcSystemProductList = self.ifcSystem.IsGroupedBy[0].RelatedObjects
        for relatedObj in self.ifcSystemProductList:
            entity = self.file.by_guid(relatedObj.GlobalId)
            obj = tool.Ifc.get_object(entity)
            if obj is not None:
                self.commonColor.append((obj.color[0],obj.color[1],obj.color[2],obj.color[3]))
        self.uniqueColor = set(self.commonColor)
        self.colorCount = 0
        for unique in self.uniqueColor:
            count = self.commonColor.count(unique)
            if count > self.colorCount:
                colorCount = count
                self.ifcSystemColor = unique
        return context.window_manager.invoke_props_dialog(self, width = 250)
    
    def draw(self, context):
        self.col = self.layout.row().split(factor = 0.4)
        self.col.label(text = "System Color")
        self.col.prop(self, "ifcSystemColor", text="")
