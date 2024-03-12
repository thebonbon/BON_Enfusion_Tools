bl_info = {
    "name" : "BON Enfusion Tools",
    "description" : "Create decimated objects with different LOD levels",
    "author" : "TheBonBon",
    "version" : (0, 1, 0),
    "blender" : (2, 80, 0),
    "support" : "COMMUNITY",
    "location" : "View3D",
    "category" : "3D View"
}

import bpy
from bpy.types import Operator, Panel


class DecimateObjectOperator(Operator):
    """Create decimated objects with different LOD levels"""
    bl_idname = "object.decimate_objects"
    bl_label = "Decimate Objects"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        if not context.object.name.endswith("LOD0"):
            context.object.name = context.object.name + "_LOD0"

        def create_decimated_objects():
            selected_obj = context.object

            lod_factors = [0.5, 0.25, 0.1, 0.05]

            for i, factor in enumerate(lod_factors):
                
                #Create duplicate, rename and decimate
                bpy.ops.object.duplicate()
                decimated_obj = context.object
                decimated_obj.name = selected_obj.name[:-1] + str(i + 1)
                decimated_obj.modifiers.new("Decimate", type='DECIMATE')
                decimated_obj.modifiers["Decimate"].ratio = factor
                
                # Select main obj again
                bpy.ops.object.select_all(action='DESELECT')
                selected_obj.select_set(True)
                context.view_layer.objects.active = selected_obj
                bpy.ops.object.parent_set(type='OBJECT')

        create_decimated_objects()

        self.report({'INFO'}, "Decimated objects created successfully")
        return {'FINISHED'}


class DecimateObjectPanel(Panel):
    """Display decimate button"""
    bl_label = "Auto LOD"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BON Enfusion Tools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(DecimateObjectOperator.bl_idname, text="Create LODs")


classes = [
    DecimateObjectOperator,
    DecimateObjectPanel,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == '__main__':
    register()
