import bpy
import bmesh
from mathutils import Vector

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

class QuickOriginToActive(bpy.types.Operator):
    bl_idname = "util.quick_origin_to_active"
    bl_label = "Quick Origin to Active"
    bl_description = "Set the origin to the currently selected mesh data (vertex, edge, face)"

    def execute(self, context):
        if bpy.context.view_layer is None or bpy.context.mode != 'EDIT_MESH' or bpy.context.scene is None:
            return {'CANCELLED'}
        #end if
        obj = bpy.context.view_layer.objects.active
        if obj is None or obj.data is None:
            return {'CANCELLED'}
        #end if

        obj.select_set(True) # NOTE: Make sure object is selected for origin set to work
        meshObj = bmesh.from_edit_mesh(obj.data)
        originalCursorLocation = bpy.context.scene.cursor.location.copy()
        if meshObj.select_history:
            active_element = meshObj.select_history[-1]
            errorCode = self.moveCursorToSelected()
            if errorCode != 0:
                return {'CANCELLED'}

            bpy.ops.object.editmode_toggle()

            if isinstance(active_element, bmesh.types.BMVert):
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            elif isinstance(active_element, bmesh.types.BMEdge):
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            elif isinstance(active_element, bmesh.types.BMFace):
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            #end if

            bpy.context.scene.cursor.location = originalCursorLocation
            bpy.ops.object.editmode_toggle()
        #end if

        return {'FINISHED'}
    #end execute

    def moveCursorToSelected(self):
        obj = bpy.context.edit_object
        # if bpy.context.mode != 'EDIT_MESH' or bpy.context.selected_objects is None or obj is None or bpy.context.scene is None:
        #     return 1

        mesh = bmesh.from_edit_mesh(obj.data)
        selected_verts = [v for v in mesh.verts if v.select]
        if selected_verts:
            # Calculate the average (median) position of selected vertices
            # Need to transform the local coordinates to world coordinates
            world_coords = [obj.matrix_world @ v.co for v in selected_verts]
            avg_location = sum(world_coords, Vector()) / len(world_coords)
            bpy.context.scene.cursor.location = avg_location
            bmesh.update_edit_mesh(obj.data)

        return 0
    # end function
#end class

class BackupDuplicate(bpy.types.Operator):
    bl_idname = "util.backup_duplicate"
    bl_label = "Backup Duplicate"
    bl_description = "Duplicate the active object into its collection's backup folder"

    def execute(self, context):
        if context.mode != 'OBJECT' or context.view_layer is None:
            return {'CANCELLED'}
        #end if

        original = context.view_layer.objects.active
        if original is None:
            self.report({'WARNING'}, "No active object to duplicate.")
            return {'CANCELLED'}
        #end if

        original_collections = list(original.users_collection)
        if not original_collections:
            self.report({'WARNING'}, "The active object is not linked to a collection.")
            return {'CANCELLED'}

        original_collection = context.collection
        if original_collection not in original_collections:
            original_collection = original_collections[0]

        backup_collection = self.find_backup_collection(original_collection)
        if backup_collection is None:
            backup_collection = bpy.data.collections.new(f"{original_collection.name} Backups")
            backup_collection.hide_render = True
            backup_collection.hide_viewport = True
            backup_collection.hide_select = True
            original_collection.children.link(backup_collection)
        #end if

        duplicate = original.copy()
        if original.data is not None:
            duplicate.data = original.data.copy()
        #end if
        duplicate.name = f"{original.name}_backup"
        backup_collection.objects.link(duplicate)
        duplicate.select_set(False)
        context.view_layer.objects.active = original

        return {'FINISHED'}
    #end execute

    def find_backup_collection(self, parent):
        for child in parent.children:
            if "backup" in child.name.casefold():
                return child
            nested_backup = self.find_backup_collection(child)
            if nested_backup is not None:
                return nested_backup
        #end for
        return None
    #end find_backup_collection
#end class
