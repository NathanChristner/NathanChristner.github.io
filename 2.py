bl_info = {
    "name": "Delete Selected Keyframes",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 2, 0),
    "location": "Dopesheet/Graph Editor",
    "description": "Deletes selected keyframes with Ctrl+X shortcut",
    "category": "Animation",
}

import bpy
from bpy.types import Operator
from bpy.props import BoolProperty

class DELETE_SELECTED_KEYFRAMES_OT_delete(Operator):
    """Delete selected keyframes"""
    bl_idname = "anim.delete_selected_keyframes"
    bl_label = "Delete Selected Keyframes"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        # Check if we are in a context where keyframes can be selected
        return context.space_data and context.space_data.type in {'DOPESHEET_EDITOR', 'GRAPH_EDITOR'}
    
    def execute(self, context):
        # Delete selected keyframes
        # In Blender 4.2, we need to use the correct operator depending on the context
        if context.space_data.type == 'DOPESHEET_EDITOR':
            try:
                bpy.ops.action.delete()
                self.report({'INFO'}, "Deleted selected keyframes from Dopesheet")
                return {'FINISHED'}
            except Exception as e:
                self.report({'ERROR'}, f"Error: {str(e)}")
                return {'CANCELLED'}
        elif context.space_data.type == 'GRAPH_EDITOR':
            try:
                bpy.ops.graph.delete()
                self.report({'INFO'}, "Deleted selected keyframes from Graph Editor")
                return {'FINISHED'}
            except Exception as e:
                self.report({'ERROR'}, f"Error: {str(e)}")
                return {'CANCELLED'}
        else:
            self.report({'WARNING'}, "No keyframes selected or unsupported editor")
            return {'CANCELLED'}

addon_keymaps = []

def register():
    # Register operator
    bpy.utils.register_class(DELETE_SELECTED_KEYFRAMES_OT_delete)
    
    # Add keymap entry
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # Create keymap for dopesheet editor
        km_dopesheet = kc.keymaps.new(name='Dopesheet', space_type='DOPESHEET_EDITOR')
        kmi_dopesheet = km_dopesheet.keymap_items.new(
            DELETE_SELECTED_KEYFRAMES_OT_delete.bl_idname, 
            'X', 'PRESS', ctrl=True
        )
        addon_keymaps.append((km_dopesheet, kmi_dopesheet))
        
        # Create keymap for graph editor
        km_graph = kc.keymaps.new(name='Graph Editor', space_type='GRAPH_EDITOR')
        kmi_graph = km_graph.keymap_items.new(
            DELETE_SELECTED_KEYFRAMES_OT_delete.bl_idname, 
            'X', 'PRESS', ctrl=True
        )
        addon_keymaps.append((km_graph, kmi_graph))

def unregister():
    # Remove keymap entries
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    # Unregister operator
    bpy.utils.unregister_class(DELETE_SELECTED_KEYFRAMES_OT_delete)

if __name__ == "__main__":
    register()