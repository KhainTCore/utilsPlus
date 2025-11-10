import bpy

class UtilsPlusPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__ if __package__ is not None else "utilsPlusPackage"
    show_clay_ball = bpy.props.BoolProperty(
        name = "Clay Ball Menu",
        default = True,
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(heading="Util Functions Settings")
        col.prop(self, "show_clay_ball", text="Show Clay Ball Menu in Add Mesh")
    #end draw
# end UtilsPlusPreferences
