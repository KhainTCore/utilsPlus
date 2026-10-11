import bpy
from typing import Any, cast

def _scene_camera_items(self, context):
    scene = context.scene
    if scene is None:
        return []
    return [
        (obj.name, obj.name, f"Make {obj.name} the active camera", 'CAMERA_DATA', index)
        for index, obj in enumerate(obj for obj in scene.objects if obj.type == 'CAMERA')
    ]
#end _scene_camera_items

class ActiveCameraList(bpy.types.Operator):
    bl_idname = "util.active_camera_list"
    bl_label = "Active Camera List"
    bl_description = "Choose the active camera from the current scene"
    camera_name: bpy.props.EnumProperty(
        name="Camera",
        items=_scene_camera_items,
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        scene = context.scene
        if scene is None:
            return {'CANCELLED'}

        camera = scene.objects.get(self.camera_name)
        if camera is None or camera.type != 'CAMERA':
            self.report({'WARNING'}, "The selected camera is no longer in this scene.")
            return {'CANCELLED'}

        scene.camera = camera

        screen = context.screen
        if screen is not None:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = cast(Any, area.spaces.active)
                    if space is not None and space.region_3d is not None:
                        space.region_3d.view_perspective = 'CAMERA'
                #end if
            #end for
        #end if

        return {'FINISHED'}

    def invoke(self, context, event):
        scene = context.scene
        if scene is None:
            return {'CANCELLED'}

        cameras = [obj for obj in scene.objects if obj.type == 'CAMERA']
        if not cameras:
            self.report({'INFO'}, "The current scene has no cameras.")
            return {'CANCELLED'}

        window_manager = context.window_manager
        if window_manager is None:
            return {'CANCELLED'}

        active_camera = scene.camera
        self.camera_name = active_camera.name if active_camera in cameras else cameras[0].name
        return window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        if layout is not None:
            layout.label(text="Choose the camera to activate:")
            column = layout.column(align=True)
            scene = context.scene
            if scene is None:
                return
            for camera in scene.objects:
                if camera.type == 'CAMERA':
                    column.prop_enum(
                        self,
                        "camera_name",
                        camera.name,
                        text=camera.name,
                        icon='CAMERA_DATA',
                    )
                #end if
            #end for
    #end draw

#end class
