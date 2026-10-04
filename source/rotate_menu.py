import bpy # pyright: ignore[reportMissingImports]
import bmesh # pyright: ignore[reportMissingImports]
import math
from mathutils import Matrix, Vector

"""
    Rotate the active object on the Y axis by a specified angle in degrees.
"""
class RotateOnAxisByDegrees(bpy.types.Operator):
    bl_idname = "util.rotate_on_axis_by_degrees"
    bl_label = "Rotate on Axis"
    bl_description = "Rotate the selected object on the specified axis"
    bl_options = {'REGISTER', 'UNDO'}
    # Angle in degrees that the caller can set when invoking the operator
    angle: bpy.props.FloatProperty(
        name="Angle (degrees)",
        default=90.0,
        description="Degrees to rotate around the specified axis",
    ) # pyright: ignore[reportInvalidTypeForm]
    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X', "X Axis", "Rotate around the X axis"),
            ('Y', "Y Axis", "Rotate around the Y axis"),
            ('Z', "Z Axis", "Rotate around the Z axis"),
        ],
        default='Y',
        description="Axis to rotate around",
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        if context.active_object is None:
            self.report({'ERROR'}, "No active object to rotate.")
            return {'CANCELLED'}
        #end if

        angle_value = float(self.angle)

        # Convert degrees to radians and apply rotation
        rot_radians = math.radians(angle_value)
        if self.axis == 'X':
            context.active_object.rotation_euler[0] += rot_radians
        elif self.axis == 'Y':
            context.active_object.rotation_euler[1] += rot_radians
        elif self.axis == 'Z':
            context.active_object.rotation_euler[2] += rot_radians
        #end if

        return {'FINISHED'}
    #end execute
#end class

class RotateOnAxisByDegreesEditMode(bpy.types.Operator):
    bl_idname = "util.rotate_on_axis_by_degrees_edit"
    bl_label = "Rotate on Axis"
    bl_description = "Rotate the selected object on the specified axis"
    bl_options = {'REGISTER', 'UNDO'}
    # Angle in degrees that the caller can set when invoking the operator
    angle: bpy.props.FloatProperty(
        name="Angle (degrees)",
        default=90.0,
        description="Degrees to rotate around the specified axis"
    ) # pyright: ignore[reportInvalidTypeForm]
    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[
            ('X', "X Axis", "Rotate around the X axis"),
            ('Y', "Y Axis", "Rotate around the Y axis"),
            ('Z', "Z Axis", "Rotate around the Z axis"),
        ],
        default='Y',
        description="Axis to rotate around"
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        if context.active_object is None:
            self.report({'ERROR'}, "No active object to rotate.")
            return {'CANCELLED'}
        #end if

        angle_value = float(self.angle)
        #axis_value = str(self.axis)

        orient_type = getattr(context.space_data, "transform_orientation", None)
        if orient_type is None:
            slots = getattr(context.scene, "transform_orientation_slots", None)
            if slots and len(slots) > 0:
                orient_type = getattr(slots[0], "type", 'GLOBAL')
            else:
                orient_type = 'GLOBAL'

        bpy.ops.transform.rotate(
            value=math.radians(angle_value),
            orient_type=orient_type,
            constraint_axis=(self.axis == 'X', self.axis == 'Y', self.axis == 'Z'),
            use_proportional_edit=False,
        )

        print(f"Rotated {context.active_object.name} around {self.axis} by {angle_value} degrees.")
        return {'FINISHED'}
    #end execute
#end class

"""
    Defines the "Axis Rotation" menu in 3D Viewport Object Context Menu
"""
class VIEW3D_MT_mesh_axis_rotation(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_axis_rotation"
    bl_label = "Axis Rotation"

    def draw(self, context):
        if self.layout is None:
            return
        #end if
        self.layout.operator_context = 'INVOKE_REGION_WIN'

        operator_id = "util.rotate_on_axis_by_degrees_edit" if context.mode == 'EDIT_MESH' else "util.rotate_on_axis_by_degrees"

        for axis in ['X', 'Y', 'Z']:
            self.layout.label(text=f"Rotate {axis} Axis")
            for angle in [30.0, 45.0, 90.0, 180.0]:
                row = self.layout.row(align=True)
                op = row.operator(operator_id, text=f"{axis} {angle}\u00b0")
                op.angle = float(angle)
                op.axis = axis
            #end for
            row.separator()
        #end for
    #end draw
#end class


def object_context_axis_rotation(self, context):
    """Appendable function to add the Axis Rotation submenu to the Object Context Menu."""
    layout = self.layout
    layout.separator()
    layout.menu(VIEW3D_MT_mesh_axis_rotation.bl_idname, text="Axis Rotation", icon='DRIVER')
# end object_context_axis_rotation
