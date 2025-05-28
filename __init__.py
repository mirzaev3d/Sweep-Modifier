bl_info = {
    "name": "Sweep Modifier",
    "author": "Abbos Mirzaev",
    "version": (2, 0, 1),
    "blender": (4, 4, 0),
    "location": "Modifier Tab > Generate, Pie Menu",
    "description": "Adds a Sweep Modifier with profile and bevel curve support using Geometry Nodes",
    "category": "Modifier"
}

import bpy
import os
from bpy.types import Operator, Menu
from bpy.props import EnumProperty


def get_addon_directory():
    return os.path.dirname(__file__)


def register_asset_library():
    addon_path = get_addon_directory()
    lib_name = "Sweep Modifier Assets"
    prefs = bpy.context.preferences.filepaths.asset_libraries
    if not any(lib.name == lib_name for lib in prefs):
        new_lib = prefs.new(name=lib_name)
        new_lib.path = addon_path


def link_profile_object(profile_name: str) -> bpy.types.Object:
    blend_path = os.path.join(get_addon_directory(), "Sweep Modifier.blend")
    if profile_name in bpy.data.objects:
        return bpy.data.objects[profile_name]

    with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
        if profile_name in data_from.objects:
            data_to.objects = [profile_name]
        else:
            return None

    linked_obj = bpy.data.objects.get(profile_name)
    if linked_obj and linked_obj.name not in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.link(linked_obj)

    return linked_obj


class OBJECT_OT_SweepModifierAdd(Operator):
    bl_idname = "object.sweep_modifier_add"
    bl_label = "Sweep Modifier"
    bl_description = "Adds Sweep Modifier Geometry Nodes to selected object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type not in {'MESH', 'CURVE'}:
            self.report({'WARNING'}, "Select a mesh or curve object")
            return {'CANCELLED'}

        asset_path = os.path.join(get_addon_directory(), "Sweep Modifier.blend")
        if not os.path.exists(asset_path):
            self.report({'ERROR'}, "Asset .blend file not found")
            return {'CANCELLED'}

        with bpy.data.libraries.load(asset_path, link=False) as (data_from, data_to):
            if "Sweep Modifier" in data_from.node_groups:
                data_to.node_groups = ["Sweep Modifier"]
            else:
                self.report({'ERROR'}, "Sweep Modifier node group not found")
                return {'CANCELLED'}

        modifier = obj.modifiers.new(name="Sweep Modifier", type='NODES')
        modifier.node_group = bpy.data.node_groups.get("Sweep Modifier")
        return {'FINISHED'}


class OBJECT_OT_ApplySweepProfile(Operator):
    bl_idname = "object.apply_sweep_profile"
    bl_label = "Apply Selected Profile"
    bl_description = "Links the selected profile and assigns it to the Sweep Modifier"

    def execute(self, context):
        wm = context.window_manager
        obj = context.object

        if not obj or obj.type not in {'MESH', 'CURVE'}:
            self.report({'ERROR'}, "Select a mesh or curve")
            return {'CANCELLED'}

        profile_name = wm.sweep_profiles
        profile_obj = link_profile_object(profile_name)

        if not profile_obj:
            self.report({'ERROR'}, f"Could not find profile: {profile_name}")
            return {'CANCELLED'}

        mod = next((m for m in obj.modifiers if m.type == 'NODES' and m.node_group and m.name == "Sweep Modifier"), None)
        if not mod:
            self.report({'ERROR'}, "Sweep Modifier not found on object")
            return {'CANCELLED'}

        try:
            mod["Profile"] = profile_obj
        except:
            self.report({'WARNING'}, "Failed to assign profile to Geometry Nodes input")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Profile '{profile_name}' assigned")
        return {'FINISHED'}


class VIEW3D_PIE_SweepModifier(Menu):
    bl_label = "Sweep Modifier"
    bl_idname = "VIEW3D_PIE_sweep_modifier"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator("object.sweep_modifier_add", text="Add Sweep Modifier", icon='PROP_PROJECTED')


def modifier_menu_func(self, context):
    if context.object and context.object.type in {'MESH', 'CURVE'}:
        self.layout.operator("object.sweep_modifier_add", icon='PROP_PROJECTED')


def sweep_profile_items(self, context):
    items = []
    lib_path = os.path.join(get_addon_directory(), "Sweep Modifier.blend")
    if os.path.exists(lib_path):
        with bpy.data.libraries.load(lib_path, link=True) as (data_from, _):
            for name in data_from.objects:
                items.append((name, name, "", 'MESH_CIRCLE', len(items)))
    return items


addon_keymaps = []

def register_shortcut():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu_pie", 'Q', 'PRESS', ctrl=True, shift=True)
    kmi.properties.name = "VIEW3D_PIE_sweep_modifier"
    addon_keymaps.append((km, kmi))


def unregister_shortcut():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = [
    OBJECT_OT_SweepModifierAdd,
    OBJECT_OT_ApplySweepProfile,
    VIEW3D_PIE_SweepModifier
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.sweep_profiles = EnumProperty(
        name="Profile",
        description="Select a custom bevel profile",
        items=sweep_profile_items
    )

    bpy.types.DATA_PT_modifiers.append(modifier_menu_func)
    register_asset_library()
    register_shortcut()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.WindowManager.sweep_profiles
    bpy.types.DATA_PT_modifiers.remove(modifier_menu_func)
    unregister_shortcut()


if __name__ == "__main__":
    register()
