bl_info = {
    "name": "Quick Transform Keyframes",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "3D View",
    "description": "Sets keyframes for all transforms (location, rotation, scale) with 'I' key",
    "category": "Animation",
}

import bpy

class ANIMATION_OT_quick_transform_keyframes(bpy.types.Operator):
    """Insert keyframes for location, rotation, and scale on selected objects"""
    bl_idname = "object.quick_keyframe_all_transforms"
    bl_label = "Keyframe All Transforms"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.selected_objects and context.mode == 'OBJECT'
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
            
        try:
            # This is the most direct way to insert keyframes for LocRotScale
            # It's equivalent to pressing 'I' and selecting 'LocRotScale' from the menu
            bpy.ops.anim.keyframe_insert(type='LocRotScale')
            self.report({'INFO'}, f"Added transform keyframes for {len(context.selected_objects)} object(s)")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

# Store keymaps here to access after registration
addon_keymaps = []

def register():
    bpy.utils.register_class(ANIMATION_OT_quick_transform_keyframes)
    
    # Handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    
    kmi = km.keymap_items.new(
        ANIMATION_OT_quick_transform_keyframes.bl_idname, 
        'I', 'PRESS'
    )
    addon_keymaps.append((km, kmi))

def unregister():
    # Remove the keymap items
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(ANIMATION_OT_quick_transform_keyframes)

if __name__ == "__main__":
    register()