import bpy
import math

class AddSimpleCameraRig(bpy.types.Operator):
    bl_idname = "util.add_simple_camera_rig"
    bl_label = "Add Simple Camera Rig"
    bl_description = "Add a Camera and set it up with a Camera Path and Camera Target"

    def execute(self, context):
        # target_collection = bpy.data.collections.get("Render")
        bpy.ops.mesh.primitive_circle_add(radius=1, location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        cameraTarget = bpy.context.active_object
        bpy.ops.curve.primitive_nurbs_path_add(location=(0, 0, 0))
        cameraPath = bpy.context.active_object

        if cameraTarget is None or cameraPath is None:
            return {'CANCELLED'}
        #end if
        cameraTarget.name = "Camera Target"
        cameraPath.name = "Camera Path"

        bpy.ops.object.camera_add(location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        camera = bpy.context.active_object
        cameraPathConstraint = bpy.data.objects["Camera"].constraints.new(type="FOLLOW_PATH")
        cameraPathConstraint.target = cameraPath # type: ignore
        cameraTargetConstraint = bpy.data.objects["Camera"].constraints.new(type="TRACK_TO")
        cameraTargetConstraint.target = cameraTarget # type: ignore
        cameraPath.select_set(True)
        if (bpy.context.view_layer is not None):
            bpy.context.view_layer.objects.active = cameraPath
        #end if
        return {'FINISHED'}
    #end execute
#end class
