import bpy

"""
    Creates and Manages shortcuts for navigating Blender Workspace Tabs.
    Allows Users to quickly reorder Workspaces in an easier and more intuitive way.

    Attributes:
        bl_idname (str): Part of the custom Util category
        bl_label (str): Name of this particular util is Utils Plus
"""

class NavigateWorkspace(bpy.types.Operator):
    bl_idname = "util.navigate_workspace"
    bl_label = "Navigate Workspace"
    bl_description = "Navigate between Blender Workspace Tabs"
    bl_options = {'REGISTER', 'UNDO'}
    name: bpy.props.StringProperty(
        name="Workspace Name",
        default="",
        description="Name of the workspace to navigate to"
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        workspace = bpy.data.workspaces.get(self.name)
        if workspace is None:
            self.report({'WARNING'}, f"Workspace '{self.name}' no longer exists.")
            return {'CANCELLED'}

        if context.window is None:
            return {'CANCELLED'}

        context.window.workspace = workspace
        return {'FINISHED'}
    #end execute
#end class

"""
    Defines the "Workspace Navigator" menu in 3D Viewport Object Context Menu
"""
class Workspace_navigator(bpy.types.Menu):
    bl_idname = "util.workspace_navigator"
    bl_label = "Workspace Navigator"

    def draw(self, context):
        layout = self.layout
        if layout is None:
            return
        #end if
        pie = layout.menu_pie()
        workspaces = list(bpy.data.workspaces)
        visible_workspaces = workspaces[:7] if len(workspaces) > 8 else workspaces

        for workspace in visible_workspaces:
            op = pie.operator("util.navigate_workspace", text=workspace.name)
            op.name = workspace.name
        #end for

        if len(workspaces) > 8:
            pie.menu("UTIL_MT_workspace_overflow", text="More Workspaces")
        #end if
    #end draw
#end class


class WorkspaceOverflowMenu(bpy.types.Menu):
    bl_idname = "UTIL_MT_workspace_overflow"
    bl_label = "More Workspaces"

    def draw(self, context):
        layout = self.layout
        if layout is None:
            return

        for workspace in list(bpy.data.workspaces)[7:]:
            op = layout.operator("util.navigate_workspace", text=workspace.name)
            op.name = workspace.name
        #end for
    #end draw
#end class
