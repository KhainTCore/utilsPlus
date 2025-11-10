import bpy # pyright: ignore[reportMissingImports]
import bmesh # pyright: ignore[reportMissingImports]

"""
    Creates a Single Vert and adds a Skin Modifier followed by a Subdivision
    Modifier to it.
        NOTE: Helpful for low-poly meshes for Box Modeling
"""
class AddClayVert(bpy.types.Operator):
    bl_idname = "util.add_clay_vert"
    bl_label = "Add Clay Vert"
    bl_description = "Add a single vert with a Skin and Subdivision modifier"

    def execute(self, context):
        self.single_vert_add()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.modifier_add(type='SKIN')
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.transform.skin_resize(value=(2, 2, 2))
        return {'FINISHED'}
    #end execute

    def single_vert_add(self):
        try: # Attempt to use single-vert add-on operator
            bpy.ops.mesh.primitive_vert_add() # pyright: ignore[reportAttributeAccessIssue]
        except: # Fallback if the operator is not available
            bpy.ops.mesh.primitive_plane_add(enter_editmode=True)
            bpy.ops.mesh.merge(type='CENTER')
        #end try
    #end single_vert_add
#end class

"""
    Creates Clay Vert and then applies the modifiers
        NOTE: Helpful for low-poly meshes for Box Modeling
"""
class AddClayBall(bpy.types.Operator):
    bl_idname = "util.add_clay_ball"
    bl_label = "Add Clay Ball"
    bl_description = "Add a Clay Vert and apply the Skin and Subdivision modifiers"

    def execute(self, context):
        bpy.ops.util.add_clay_vert() # pyright: ignore[reportAttributeAccessIssue]
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(modifier="Skin", report=True)
        bpy.ops.object.modifier_apply(modifier="Subdivision", report=True)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.editmode_toggle()

        return {'FINISHED'}
    #end execute
#end class

"""
    Creates Clay Ball and then uses a mirror modifier to modify across the Y-axis
        NOTE: Helpful for low-poly meshes for Box Modeling
"""
class AddClayBallMirrored(bpy.types.Operator):
    bl_idname = "util.add_clay_ball_mirrored"
    bl_label = "Add Clay Ball Mirrored"
    bl_description = "Add a Clay Ball that is mirrored across the Y-axis"

    def execute(self, context):
        bpy.ops.util.add_clay_ball() # pyright: ignore[reportAttributeAccessIssue]
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        # Select vertices with a positive X coordinate
        for v in bm.verts:
            if v.co.y < -0.0001:
                v.select = True
            #end if
        #end for
        bpy.ops.mesh.delete(type='VERT')
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.object.modifier_move_to_index(modifier="Mirror", index=0)

        if bpy.context.object is None:
            return {'CANCELLED'}
        #end if
        bpy.context.object.modifiers["Mirror"].use_axis[0] = False  # X-axis
        bpy.context.object.modifiers["Mirror"].use_axis[1] = True   # Y-axis
        return {"FINISHED"}
    #end execute
#end class

"""
    Defines the "Clay Ball" menu in the Add Mesh menu
"""
class VIEW3D_MT_mesh_clay_ball_add(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_mesh_clay_ball_add"
    bl_label = "Clay Ball"

    def draw(self, context):
        if self.layout is None:
            return
        #end if
        self.layout.operator_context = 'INVOKE_REGION_WIN'
        self.layout.operator("util.add_clay_vert", text="Add Clay Vert")
        self.layout.operator("util.add_clay_ball", text="Add Clay Ball")
        self.layout.operator("util.add_clay_ball_mirrored", text="Add Clay Ball Mirrored")
    #end draw
#end class
