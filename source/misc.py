import bpy

class SemiTransparent(bpy.types.Operator):
    bl_idname = "util.add_semi_transparent_node"
    bl_label = "Semi Transparent"
    bl_description = "Add a Transparent and Translucent node and combine with a Mix Shader Node"

    def execute(self, context):
        return {'FINISHED'}
    #end execute
#end class

class ListStoredNamedVariables(bpy.types.Operator):
    bl_idname = "util.list_stored_named_variables"
    bl_label = "List Stored Named Variables"
    bl_description = "List all stored named variables in the console"

    def execute(self, context):
        return {'FINISHED'}
    #end execute
#end class

class MoveObjectToCollection(bpy.types.Operator):
    bl_idname = "util.move_object_to_collection"
    bl_label = "Move Object to Collection"
    bl_description = "Move the currently selected Object to a different Collection"

    def execute(self, context):
        return {'FINISHED'}
    #end execute
#end class
