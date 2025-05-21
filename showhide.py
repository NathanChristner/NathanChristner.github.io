bl_info = {
    "name": "Toggle Overlays and Gizmos",
    "author": "Nate (via Assistant)",
    "version": (1, 0, 1),
    "blender": (4, 3, 0), # Works with 4.3.0 and above, including 4.3.2
    "location": "3D Viewport > Shift + E",
    "description": "Toggles both Show Overlays and Show Gizmo simultaneously.",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}

import bpy

class VIEW3D_OT_toggle_overlays_gizmos(bpy.types.Operator):
    """Toggle Overlays and Gizmos in the 3D View"""
    bl_idname = "view3d.toggle_overlays_gizmos"
    bl_label = "Toggle Overlays & Gizmos"
    bl_options = {'REGISTER', 'UNDO'} # UNDO is good practice

    def execute(self, context):
        # Check if we are in a 3D Viewport
        if context.area.type == 'VIEW_3D':
            space = context.space_data # Get the 3D View space data

            # Determine the new state based on the current state of overlays
            # If overlays are currently on, we want to turn both off.
            # If overlays are currently off, we want to turn both on.
            # This ensures they are always synced.
            current_overlays_state = space.show_overlays
            new_state = not current_overlays_state

            space.show_overlays = new_state
            space.show_gizmo = new_state
            
            # Optional: Provide feedback in the status bar
            if new_state:
                self.report({'INFO'}, "Overlays and Gizmos: ON")
            else:
                self.report({'INFO'}, "Overlays and Gizmos: OFF")

            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Active area is not a 3D Viewport")
            return {'CANCELLED'}

# --- Keymap Registration ---
addon_keymaps = []

def register_keymap():
    wm = bpy.context.window_manager
    # Note: Changing an existing keymap might be risky for distribution.
    # If this addon is just for you, it's fine.
    # For broader distribution, consider a different keymap or making it configurable.
    kc = wm.keyconfigs.addon
    if kc:
        # Add to 3D View (Global)
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(VIEW3D_OT_toggle_overlays_gizmos.bl_idname, 'E', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))

def unregister_keymap():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

# --- Addon Registration ---
def register():
    bpy.utils.register_class(VIEW3D_OT_toggle_overlays_gizmos)
    register_keymap()

def unregister():
    unregister_keymap()
    bpy.utils.unregister_class(VIEW3D_OT_toggle_overlays_gizmos)

# This allows the script to be run directly in Blender's Text Editor
# for testing purposes, without Mnecessarily installing it as an addon.
if __name__ == "__main__":
    # Unregister previous version if it exists (for testing in text editor)
    try:
        unregister()
    except Exception:
        pass
    register()

    # Test call (optional, for direct script run)
    # bpy.ops.view3d.toggle_overlays_gizmos()