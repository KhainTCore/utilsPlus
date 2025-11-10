import bpy

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
        if self.collectionName is None:
            self.collectionName = "Collection"
        #end if
        new_collection = bpy.data.collections.new(self.collectionName)
        if bpy.context.scene is None:
            return {'CANCELLED'}
        #end if

        bpy.context.scene.collection.children.link(new_collection)
        return {'FINISHED'}
    #end execute

    def invoke(self, context, event):
        if self.collectionName is None:
            self.collectionName = "Collection"
        #end if

        wm = context.window_manager
        if (wm is not None):
            return wm.invoke_props_dialog(self)
        # end if

        return {'CANCELLED'}
    #end invoke
#end class
