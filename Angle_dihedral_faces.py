import bpy
import bmesh
import math
from mathutils import Vector

class MESH_OT_calculate_dihedral_angles(bpy.types.Operator):
    """Calculates dihedral angles between selected faces."""
    bl_idname = "mesh.calculate_dihedral_angles"
    bl_label = "Calcular Ángulos Dihedrales"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the active object and check if it's a mesh
        obj = context.active_object
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Seleccione una malla en modo edición")
            return {'CANCELLED'}

        # Check if the object is in edit mode
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Seleccione una malla en modo edición")
            return {'CANCELLED'}

        # Switch to object mode to access bmesh
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the selected faces
        selected_faces = [face for face in obj.data.polygons if face.select]

        # Check if at least two faces are selected
        if len(selected_faces) < 2:
            self.report({'ERROR'}, "Seleccione al menos dos caras")
            bpy.ops.object.mode_set(mode='EDIT')
            return {'CANCELLED'}

        # Calculate and store dihedral angles
        dihedral_angles = []
        for i in range(1, len(selected_faces)):
            face1 = selected_faces[i - 1]
            face2 = selected_faces[i]
            angle = calculate_dihedral_angle(obj, face1, face2)
            dihedral_angles.append(angle)

        # Set the angles in scene properties for display in the panel
        context.scene.dihedral_angles.clear()
        for angle in dihedral_angles:
            item = context.scene.dihedral_angles.add()
            item.angle = angle

        # Switch back to edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

def calculate_face_center(obj, face):
    """Calculates the center of a face."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    bm_face = bm.faces[face.index]
    face_center = bm_face.calc_center_median()
    bm.free()
    return obj.matrix_world @ face_center

def calculate_dihedral_angle(obj, face1, face2):
    """Calculates the dihedral angle between two faces."""
    normal1 = obj.matrix_world.to_3x3() @ face1.normal
    normal2 = obj.matrix_world.to_3x3() @ face2.normal

    # Calculate the dihedral angle between the normals
    angle_rad = normal1.angle(normal2)
    angle_deg = math.degrees(angle_rad)

    return angle_deg

class DihedralAngleItem(bpy.types.PropertyGroup):
    angle: bpy.props.FloatProperty()

class MESH_PT_face_angle_panel(bpy.types.Panel):
    """Panel for displaying dihedral angles between object center and face centers."""
    bl_label = "Ángulos Dihedrales"
    bl_idname = "MESH_PT_face_angle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Herramientas'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("mesh.calculate_dihedral_angles", text="Calcular Ángulos")
        row = layout.row()
        row.operator("mesh.add_and_select_faces", text="Añadir y Seleccionar Caras")
        row = layout.row()
        row.operator("mesh.clear_dihedral_angles", text="Limpiar Ángulos")
        row = layout.row()
        row.operator("mesh.save_dihedral_angles", text="Guardar Ángulos en TXT")

        if len(scene.dihedral_angles) > 0:
            for i, item in enumerate(scene.dihedral_angles):
                layout.label(text=f"Ángulo Dihedral {i + 1}: {item.angle:.2f}°")
        else:
            layout.label(text="Seleccione al menos dos caras para calcular los ángulos")

class MESH_OT_add_and_select_faces(bpy.types.Operator):
    """Adds a cube and selects it."""
    bl_idname = "mesh.add_and_select_faces"
    bl_label = "Añadir y Seleccionar Caras"

    def execute(self, context):
        # Create a new cube
        bpy.ops.mesh.primitive_cube_add(size=1)

        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all faces of the cube
        bpy.ops.mesh.select_all(action='SELECT')

        return {'FINISHED'}

class MESH_OT_clear_dihedral_angles(bpy.types.Operator):
    """Clears the calculated dihedral angles."""
    bl_idname = "mesh.clear_dihedral_angles"
    bl_label = "Limpiar Ángulos"

    def execute(self, context):
        context.scene.dihedral_angles.clear()
        return {'FINISHED'}

class MESH_OT_save_dihedral_angles(bpy.types.Operator):
    """Saves the calculated dihedral angles to a text file."""
    bl_idname = "mesh.save_dihedral_angles"
    bl_label = "Guardar Ángulos en TXT"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        with open(self.filepath, 'w') as file:
            for i, item in enumerate(context.scene.dihedral_angles):
                file.write(f"Ángulo Dihedral {i + 1}: {item.angle:.2f}°\n")
        self.report({'INFO'}, "Ángulos guardados correctamente")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(MESH_OT_calculate_dihedral_angles)
    bpy.utils.register_class(DihedralAngleItem)
    bpy.utils.register_class(MESH_PT_face_angle_panel)
    bpy.utils.register_class(MESH_OT_add_and_select_faces)
    bpy.utils.register_class(MESH_OT_clear_dihedral_angles)
    bpy.utils.register_class(MESH_OT_save_dihedral_angles)
    bpy.types.Scene.dihedral_angles = bpy.props.CollectionProperty(type=DihedralAngleItem)

def unregister():
    bpy.utils.unregister_class(MESH_OT_calculate_dihedral_angles)
    bpy.utils.unregister_class(DihedralAngleItem)
    bpy.utils.unregister_class(MESH_PT_face_angle_panel)
    bpy.utils.unregister_class(MESH_OT_add_and_select_faces)
    bpy.utils.unregister_class(MESH_OT_clear_dihedral_angles)
    bpy.utils.unregister_class(MESH_OT_save_dihedral_angles)
    del bpy.types.Scene.dihedral_angles

if __name__ == "__main__":
    register()
