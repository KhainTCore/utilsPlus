bl_info = {
    "name": "Util Plus Addon",
    "blender": (4, 5, 0),  # Minimum Blender version
    "category": "User Interface",  # Category in the Add-ons preferences
    "author": "Khain Lescallette",
    "description": "A collection of utility functions to help improve the blender UX",
    "version": (1, 1, 1),
    "warning": "",
    "doc_url": "",
    "tracker_url": ""
}
addon_keymaps = []

import bpy
import bmesh
import math

"""
    Creates a Collection in the Outliner at the root Scene level,
    either with the default Collection Name schema, or a custom user
    defined name (presented in a dialog).

    Attributes:
        bl_idname (str): Part of the custom Util category
        bl_label (str): Name of this particular util is Utils Plus
"""
class MakeSceneCollection(bpy.types.Operator):
    bl_idname = "util.outliner_make_scene_collection"
    bl_label = "Make Scene Collection"
    collectionName: bpy.props.StringProperty(
        name = "Collection Name",
        description = "Enter Collection Name Here",
        default = "Collection"
    )
    bl_property = "collectionName" # Focus on this element

    def execute(self, context):
        new_collection = bpy.data.collections.new(self.collectionName)
        bpy.context.scene.collection.children.link(new_collection)
        return set()
    #end execute

    def invoke(self, context, event):
        self.setDefaultName()
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    #end invoke

    def setDefaultName(self):
        count = 0;
        for el in bpy.data.collections:
            if "Collection" in el.name:
                count+=1
            #end if
        #end for
        if count > 0:
            self.collectionName += str(count)
        #end if
    #end setDefaultName
#end class

class SemiTransparent(bpy.types.Operator):
    bl_idname = "util.add_semi_transparent_node"
    bl_label = "Semi Transparent"
    bl_description = "Add a Transparent and Translucent node and combine with a Mix Shader Node"

    def execute(self, context):
        return {"FINISHED"}
    #end execute
#end class

class MoveObjectToCollection(bpy.types.Operator):
    bl_idname = "util.move_object_to_collection"
    bl_label = "Move Object to Collection"
    bl_description = "Move the currently selected Object to a different Collection"

    def execute(self, context):
        return {"Finished"}
    #end execute
#end class

class CreateCameraRig(bpy.types.Operator):
    bl_idname = "util.create_camera_rig"
    bl_label = "Create Camera Rig"
    bl_description = "Create a Camera and set it up with a Camera Path and Camera Target"

    def execute(self, context):
        # target_collection = bpy.data.collections.get("Render")
        bpy.ops.mesh.primitive_circle_add(radius=1, location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        cameraTarget = bpy.context.active_object
        cameraTarget.name = "Camera Target"
        bpy.ops.curve.primitive_nurbs_path_add(location=(0, 0, 0))
        cameraPath = bpy.context.active_object
        cameraPath.name = "Camera Path"

        bpy.ops.object.camera_add(location=(0, 0, 0), rotation=(0, math.radians(90), 0))
        bpy.ops.object.constraint_add(type='FOLLOW_PATH')
        bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["Camera Path"]
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["Camera Target"]

        return {"Finished"}
    #end execute
#end class

"""
    Creates a Single Vert and adds a Skin Modifier followed by a Subdivision
    Modifier to it.

        NOTE: Helpful for low-poly meshes for Box Modeling

    Attributes:
        bl_idname (str): Part of the custom Util category
        bl_label (str): Name of this particular util is Utils Plus
"""
class AddClayVert(bpy.types.Operator):
    bl_idname = "util.add_clay_vert"
    bl_label = "Add Clay Vert"
    bl_description = "Add a single vert with a Skin and Subdivision modifier"

    def execute(self, context):
        bpy.ops.mesh.primitive_vert_add()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.modifier_add(type='SKIN')
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.transform.skin_resize(value=(2, 2, 2))
        return {"FINISHED"}
    #end execute
#end class

"""
    Creates Clay Vert and then applies the modifiers

        NOTE: Helpful for low-poly meshes for Box Modeling

    Attributes:
        bl_idname (str): Part of the custom Util category
        bl_label (str): Name of this particular util is Utils Plus
"""
class AddClayBall(bpy.types.Operator):
    bl_idname = "util.add_clay_ball"
    bl_label = "Add Clay Ball"
    bl_description = "Add a Clay Vert and apply the Skin and Subdivision modifiers"

    def execute(self, context):
        AddClayVert.execute(self, context)
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(modifier="Skin", report=True)
        bpy.ops.object.modifier_apply(modifier="Subdivision", report=True)
        bpy.ops.object.modifier_add(type='SUBSURF')
        bpy.ops.object.editmode_toggle()

        return {"FINISHED"}
    #end execute
#end class

"""
    Creates Clay Ball and then uses a mirror modifier to modify across the Y-axis

        NOTE: Helpful for low-poly meshes for Box Modeling

    Attributes:
        bl_idname (str): Part of the custom Util category
        bl_label (str): Name of this particular util is Utils Plus
"""
class AddClayBallMirrored(bpy.types.Operator):
    bl_idname = "util.add_clay_ball_mirrored"
    bl_label = "Add Clay Ball Mirrored"
    bl_description = "Add a Clay Ball that is mirrored across the Y-axis"

    def execute(self, context):
        AddClayBall.execute(self, context)
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
        bpy.context.object.modifiers["Mirror"].use_axis[1] = True
        bpy.context.object.modifiers["Mirror"].use_axis[0] = False

        return {"FINISHED"}
    #end execute
#end class

class VIEW3D_MT_mesh_clay_ball_add(bpy.types.Menu):
    # Define the "Clay Ball" menu
    bl_idname = "VIEW3D_MT_mesh_clay_ball_add"
    bl_label = "Clay Ball"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("util.add_clay_vert", text="Add Clay Vert")
        #layout.separator()
        layout.operator("util.add_clay_ball", text="Add Clay Ball")
        layout.operator("util.add_clay_ball_mirrored", text="Add Clay Ball Mirrored")
        layout.operator("util.create_camera_rig", text="Create Camera Rig")
    #end draw
#end class

def setKeybinding():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = wm.keyconfigs.addon.keymaps.new(name='Outliner', space_type='OUTLINER') # Or other relevant space_type
    kmi = km.keymap_items.new(MakeSceneCollection.bl_idname, 'N', 'PRESS', ctrl=True) # Example: Ctrl+N
    addon_keymaps.append((km, kmi))
#end setKeybinding

def menu_func(self, context):
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'
    layout.menu("VIEW3D_MT_mesh_clay_ball_add", text="Clay Ball", icon='DECORATE')
#end menu_func

# Register
classes = [
    MakeSceneCollection,
    CreateCameraRig,
    AddClayVert,
    AddClayBall,
    AddClayBallMirrored,
    VIEW3D_MT_mesh_clay_ball_add
]

def unregister():
    # Remove the custom keymaps
    wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for el in classes:
        bpy.utils.unregister_class(el)
        print(f"Unregistered: {el.bl_label}")
    #end for
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
#end unregister

def register():
    for el in classes:
        bpy.utils.register_class(el)
    #end for

    setKeybinding()
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
#end register

if __name__ == "__main__":
    register()
#end if
