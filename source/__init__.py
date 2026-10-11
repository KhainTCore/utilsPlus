addon_keymaps = []

import bpy

from .hide_and_show_objects import *
from .active_camera_dialog import *
from .add_scene_collection import *
from .add_camera_rig import *
from .add_clay_ball import *
from .auto_highlight_listener import *
from .misc import *
from .rotate_menu import *
from .workspaceManager import *

# Register
classes = [
    MakeSceneCollection,
    AddSimpleCameraRig,
    AddClayVert,
    AddClayBall,
    AddClayBallMirrored,
    BackupDuplicate,
    ActiveCameraList,
    QuickOriginToActive,
    ToggleRenderByValue,
    ToggleViewportByValue,
    VIEW3D_MT_mesh_clay_ball_add,
    RotateOnAxisByDegrees,
    RotateOnAxisByDegreesEditMode,
    VIEW3D_MT_mesh_axis_rotation,
    NavigateWorkspace,
    WorkspaceOverflowMenu,
    Workspace_navigator,
]

def setKeybinding():
    wm = bpy.context.window_manager
    if wm is None or wm.keyconfigs.addon is None:
        return
    #end if
    kc = wm.keyconfigs.addon
    km = wm.keyconfigs.addon.keymaps.new(name='Outliner', space_type='OUTLINER') # Or other relevant space_type
    kmi = km.keymap_items.new(MakeSceneCollection.bl_idname, 'N', 'PRESS', ctrl=True) # Example: Ctrl+N
    addon_keymaps.append((km, kmi))

    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'W', 'PRESS', shift=True)
    if kmi.properties is not None:
        kmi.properties.name = Workspace_navigator.bl_idname
    addon_keymaps.append((km, kmi))
#end setKeybinding

def clay_ball_menu_func(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.menu("VIEW3D_MT_mesh_clay_ball_add", text="Clay Ball", icon='DECORATE')
#end menu_func

def camera_menu_func(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.operator(AddSimpleCameraRig.bl_idname, text="Simple Camera Rig", icon='CAMERA_DATA')
#end camera_menu_func

def unregister():
    stop_auto_highlight_listener()

    # Remove the custom keymaps
    wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    #end for
    addon_keymaps.clear()

    for el in classes:
        bpy.utils.unregister_class(el)
        print(f"Unregistered: {el.bl_label}")
    #end for
    # bpy.utils.unregister_class(AutoHighlightListener)
    bpy.types.VIEW3D_MT_mesh_add.remove(clay_ball_menu_func)
    try:
        bpy.types.VIEW3D_MT_object_context_menu.remove(object_context_axis_rotation)
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(object_context_axis_rotation)
    except Exception:
        pass
#end unregister

def register():
    for el in classes:
        bpy.utils.register_class(el)
    #end for

    start_auto_highlight_listener()
    setKeybinding()
    bpy.types.VIEW3D_MT_mesh_add.append(clay_ball_menu_func)
    bpy.types.VIEW3D_MT_camera_add.append(camera_menu_func)
    # Append the Axis Rotation submenu to both object and edit-mesh context menus
    bpy.types.VIEW3D_MT_object_context_menu.append(object_context_axis_rotation)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(object_context_axis_rotation)
#end register

if __name__ == "__main__":
    register()
#end if
