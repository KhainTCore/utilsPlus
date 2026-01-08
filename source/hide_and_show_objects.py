import bpy

class ToggleViewportByValue(bpy.types.Operator):
    bl_idname = "util.toggle_viewport_by_value"
    bl_label = "Toggle Viewport by Value"
    bl_description = "Toggle visibility in the viewport for all objects with a specific substring in their name"
    bl_property = "nameSubstring"  # Focus on this element

    nameSubstring: bpy.props.StringProperty(
        name="Value",
        description="Substring to search for in object names; semicolon (;) for multiple",
        default=""
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        if bpy.context.scene is None or self.nameSubstring == "":
            return {'CANCELLED'}
        #end if

        for obj in bpy.context.scene.objects:
            if self.nameSubstring.lower() in obj.name.lower():
                obj.hide_viewport = not obj.hide_viewport
            #end if
        #end for

        return {'FINISHED'}
    #end execute

    def invoke(self, context, event):
        wm = context.window_manager
        if (wm is not None):
            return wm.invoke_props_dialog(self)
        # end if

        return {'CANCELLED'}
    #end invoke

    def draw(self, context):
        layout = self.layout
        if (layout is None):
            return
        layout.prop(self, "nameSubstring")
    #end draw
#end class

class ToggleRenderByValue(bpy.types.Operator):
    bl_idname = "util.toggle_render_by_value"
    bl_label = "Toggle Render by Value"
    bl_description = "Toggle render visibility for all objects with a specific substring in their name"
    bl_property = "nameSubstring"  # Focus on this element

    nameSubstring: bpy.props.StringProperty(
        name="Value",
        description="Substring to search for in object names; semicolon (;) for multiple",
        default=""
    ) # pyright: ignore[reportInvalidTypeForm]

    def execute(self, context):
        if bpy.context.scene is None or self.nameSubstring == "":
            return {'CANCELLED'}
        #end if

        for obj in bpy.context.scene.objects:
            if self.nameSubstring.lower() in obj.name.lower():
                obj.hide_render = not obj.hide_render
            #end if
        #end for

        return {'FINISHED'}
    #end execute

    def invoke(self, context, event):
        wm = context.window_manager
        if (wm is not None):
            return wm.invoke_props_dialog(self)
        # end if

        return {'CANCELLED'}
    #end invoke

    def draw(self, context):
        layout = self.layout
        if (layout is None):
            return
        layout.prop(self, "nameSubstring")
    #end draw
#end class
