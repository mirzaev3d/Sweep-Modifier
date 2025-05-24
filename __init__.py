bl_info = {
    "name": "Sweep Modifier",
    "author": "Abbos Mirzaev",
    "version": (2, 0, 0),
    "blender": (3, 0, 0),
    "location": "Modifier > Generate, Shift+Ctrl+Q Pie Menu",
    "description": "Adds a Sweep Modifier using Geometry Nodes",
    "category": "Modifier",
}

import bpy
import os

NODE_GROUP_NAME = "Sweep Modifier"
SWEEP_BLEND_PATH = os.path.join(os.path.dirname(__file__), "Sweep Modifier.blend")


def load_node_group():
    if NODE_GROUP_NAME not in bpy.data.node_groups:
        with bpy.data.libraries.load(SWEEP_BLEND_PATH, link=False) as (data_from, data_to):
            if NODE_GROUP_NAME in data_from.node_groups:
                data_to.node_groups.append(NODE_GROUP_NAME)
    return bpy.data.node_groups.get(NODE_GROUP_NAME)


def add_sweep_modifier(obj):
    node_group = load_node_group()
    if not node_group:
        return None
    mod = obj.modifiers.new(name="Sweep Modifier", type='NODES')
    mod.node_group = node_group
    return mod


class OBJECT_OT_add_sweep_modifier(bpy.types.Operator):
    bl_idname = "object.sweep_modifier_add"
    bl_label = "Sweep Modifier"
    bl_description = "Add Sweep Modifier using Geometry Nodes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type not in {'MESH', 'CURVE'}:
            self.report({'ERROR'}, "Select a Mesh or Curve object.")
            return {'CANCELLED'}
        if not add_sweep_modifier(obj):
            self.report({'ERROR'}, "Failed to add modifier.")
            return {'CANCELLED'}
        return {'FINISHED'}


def draw_modifier_generate_button(self, context):
    self.layout.operator("object.sweep_modifier_add", text="Sweep Modifier", icon='PROP_PROJECTED')


class SWEEP_MT_pie_menu(bpy.types.Menu):
    bl_label = "Sweep Modifier"
    bl_idname = "SWEEP_MT_pie_menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator("object.sweep_modifier_add", text="Add Sweep Modifier", icon='PROP_PROJECTED')


class OBJECT_OT_call_sweep_pie(bpy.types.Operator):
    bl_idname = "wm.call_sweep_pie_menu"
    bl_label = "Call Sweep Modifier Pie Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="SWEEP_MT_pie_menu")
        return {'FINISHED'}


addon_keymaps = []


def register():
    bpy.utils.register_class(OBJECT_OT_add_sweep_modifier)
    bpy.utils.register_class(SWEEP_MT_pie_menu)
    bpy.utils.register_class(OBJECT_OT_call_sweep_pie)
    bpy.types.DATA_PT_modifiers.append(draw_modifier_generate_button)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_sweep_pie_menu", type='Q', value='PRESS', ctrl=True, shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.DATA_PT_modifiers.remove(draw_modifier_generate_button)
    bpy.utils.unregister_class(OBJECT_OT_add_sweep_modifier)
    bpy.utils.unregister_class(SWEEP_MT_pie_menu)
    bpy.utils.unregister_class(OBJECT_OT_call_sweep_pie)


if __name__ == "__main__":
    register()
