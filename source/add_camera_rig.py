import bpy
import math
import re


def unique_name(base: str, existing_names: set[str]) -> str:
    """Return a unique name using the .### suffix pattern if needed.

    Examples: "Camera" -> "Camera.001" if "Camera" exists, or "Camera.002" if
    "Camera.001" already exists.
    """
    # Match base or base.### with exactly 3 digits
    pattern = re.compile(r"^" + re.escape(base) + r"(?:\.(\d{3}))?$")
    max_idx = -1
    for name in existing_names:
        m = pattern.match(name)
        if not m:
            continue
        if m.group(1) is None:
            # base exists
            max_idx = max(max_idx, 0)
        else:
            try:
                idx = int(m.group(1))
            except Exception:
                continue
            max_idx = max(max_idx, idx)
    if max_idx == -1:
        return base
    if max_idx == 0:
        return f"{base}.001"
    return f"{base}.{(max_idx + 1):03d}"

class AddSimpleCameraRig(bpy.types.Operator):
    bl_idname = "util.add_simple_camera_rig"
    bl_label = "Add Simple Camera Rig"
    bl_description = "Add a Camera and set it up with a Camera Path and Camera Target"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Create unique names based on current data
        existing_obj_names = {o.name for o in bpy.data.objects}
        existing_col_names = {c.name for c in bpy.data.collections}

        col_base = "Camera Rig"
        target_base = "Camera Target"
        path_base = "Camera Path"
        camera_base = "Camera"

        unique_col_name = unique_name(col_base, existing_col_names)
        unique_target_name = unique_name(target_base, existing_obj_names)
        unique_path_name = unique_name(path_base, existing_obj_names)
        unique_camera_name = unique_name(camera_base, existing_obj_names)

        # Create a new collection for this rig and link to the scene collection
        rig_collection = bpy.data.collections.new(unique_col_name)
        try:
            context.scene.collection.children.link(rig_collection)
        except Exception:
            # Fallback: link to the active collection
            if context.collection is not None:
                context.collection.children.link(rig_collection)

        # Create the target (circle)
        bpy.ops.mesh.primitive_circle_add(radius=1, location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        cameraTarget = bpy.context.active_object
        if cameraTarget is None:
            return {'CANCELLED'}
        cameraTarget.name = unique_target_name

        # Create the camera path
        bpy.ops.curve.primitive_nurbs_path_add(location=(0, 0, 0))
        cameraPath = bpy.context.active_object
        if cameraPath is None:
            return {'CANCELLED'}
        cameraPath.name = unique_path_name

        # Create the camera
        bpy.ops.object.camera_add(location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        camera = bpy.context.active_object
        if camera is None:
            return {'CANCELLED'}
        camera.name = unique_camera_name

        # Move created objects into the new collection and unlink from previous collections
        for obj in (cameraTarget, cameraPath, camera):
            # Link to rig_collection if not already linked
            if rig_collection is not None and obj.name not in rig_collection.objects:
                rig_collection.objects.link(obj)
            # Unlink from other collections to keep rig isolated
            for uc in list(obj.users_collection):
                if uc is not rig_collection:
                    try:
                        uc.objects.unlink(obj)
                    except Exception:
                        pass

        # Add constraints using direct references
        cam_follow = camera.constraints.new(type="FOLLOW_PATH")
        cam_follow.target = cameraPath

        cam_track = camera.constraints.new(type="TRACK_TO")
        cam_track.target = cameraTarget

        # Make the path active/selected
        cameraPath.select_set(True)
        if (context.view_layer is not None):
            context.view_layer.objects.active = cameraPath

        return {'FINISHED'}
    #end execute
#end class
