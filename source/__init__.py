addon_keymaps = []

import bpy

from .hide_and_show_objects import *
from .auto_highlight_listener import *
from .add_scene_collection import *
from .add_camera_rig import *
from .add_clay_ball import *
from .misc import *
from .rotate_menu import *

# Register
classes = [
    MakeSceneCollection,
    AddSimpleCameraRig,
    AddClayVert,
    AddClayBall,
    AddClayBallMirrored,
    # AutoHighlightListener,
    BackupDuplicate,
    QuickOriginToActive,
    ToggleRenderByValue,
    ToggleViewportByValue,
    VIEW3D_MT_mesh_clay_ball_add,
    RotateOnAxisByDegrees,
    RotateOnAxisByDegreesEditMode,
    VIEW3D_MT_mesh_axis_rotation
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
    except Exception:
        pass
    try:
        bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(object_context_axis_rotation)
    except Exception:
        pass
#end unregister

def register():
    for el in classes:
        bpy.utils.register_class(el)
    #end for

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
