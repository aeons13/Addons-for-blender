import bpy
import bmesh
import math
from mathutils import Vector

class VertexNormalAngleItem(bpy.types.PropertyGroup):
    vertex_index: bpy.props.IntProperty()
    angle: bpy.props.FloatProperty()
    edge_length_1: bpy.props.FloatProperty()
    edge_length_2: bpy.props.FloatProperty()

class MESH_OT_calculate_vertex_normal_angles(bpy.types.Operator):
    """Calcula el ángulo entre el centro de la cara y las normales de los vértices"""
    bl_idname = "mesh.calculate_vertex_normal_angles"
    bl_label = "Calcular Ángulos Normales de Vértices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Seleccione un objeto de malla en modo edición")
            return {'CANCELLED'}
        if obj.mode != 'EDIT':
            self.report({'ERROR'}, "Seleccione un objeto de malla en modo edición")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [face for face in bm.faces if face.select]
        if len(selected_faces) != 1:
            self.report({'ERROR'}, "Seleccione exactamente una cara")
            return {'CANCELLED'}

        face = selected_faces[0]

        # Calcula el centro de la cara
        face_center = face.calc_center_median()

        context.scene.vertex_normal_angles.clear()

        # Calcula las normales de los vértices y los ángulos
        for vert in face.verts:
            vert_normal = vert.normal
            angle = math.degrees(face_center.angle(vert_normal))

            # Obtiene las longitudes de las aristas conectadas a este vértice en la cara
            edges = [edge for edge in vert.link_edges if edge in face.edges]
            edge_length_1 = edges[0].calc_length() if len(edges) > 0 else 0.0
            edge_length_2 = edges[1].calc_length() if len(edges) > 1 else 0.0

            item = context.scene.vertex_normal_angles.add()
            item.vertex_index = vert.index
            item.angle = angle
            item.edge_length_1 = edge_length_1
            item.edge_length_2 = edge_length_2

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.mode_set(mode='EDIT')
        bmesh.update_edit_mesh(obj.data)

        return {'FINISHED'}

class MESH_PT_vertex_normal_angle_panel(bpy.types.Panel):
    """Panel para mostrar los ángulos entre el centro de la cara y las normales de los vértices"""
    bl_label = "Ángulos Normales de Vértices"
    bl_idname = "MESH_PT_vertex_normal_angle_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("mesh.calculate_vertex_normal_angles", text="Calcular Ángulos Normales de Vértices")
        layout.operator("mesh.clear_vertex_normal_angles", text="Limpiar Ángulos")
        layout.operator("mesh.save_vertex_normal_angles", text="Guardar Ángulos")

        if len(scene.vertex_normal_angles) > 0:
            for item in scene.vertex_normal_angles:
                layout.label(text=f"Vértice {item.vertex_index + 1}: {item.angle:.4f}°")
                layout.label(text=f"  Arista 1: {item.edge_length_1:.4f}")
                layout.label(text=f"  Arista 2: {item.edge_length_2:.4f}")
        else:
            layout.label(text="Seleccione una cara para calcular los ángulos")

class MESH_OT_clear_vertex_normal_angles(bpy.types.Operator):
    """Limpia la lista de ángulos normales de vértices"""
    bl_idname = "mesh.clear_vertex_normal_angles"
    bl_label = "Limpiar Ángulos Normales de Vértices"

    def execute(self, context):
        context.scene.vertex_normal_angles.clear()
        return {'FINISHED'}

class MESH_OT_save_vertex_normal_angles(bpy.types.Operator):
    """Guarda los ángulos normales de vértices en un archivo de texto"""
    bl_idname = "mesh.save_vertex_normal_angles"
    bl_label = "Guardar Ángulos Normales de Vértices"

    def execute(self, context):
        filepath = bpy.path.abspath("//vertex_normal_angles.txt")
        with open(filepath, 'w') as file:
            for item in context.scene.vertex_normal_angles:
                file.write(f"Vértice {item.vertex_index + 1}: {item.angle:.4f}°\n")
                file.write(f"  Arista 1: {item.edge_length_1:.4f}\n")
                file.write(f"  Arista 2: {item.edge_length_2:.4f}\n")
        self.report({'INFO'}, f"Ángulos normales de vértices guardados en {filepath}")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(VertexNormalAngleItem)
    bpy.utils.register_class(MESH_OT_calculate_vertex_normal_angles)
    bpy.utils.register_class(MESH_PT_vertex_normal_angle_panel)
    bpy.utils.register_class(MESH_OT_clear_vertex_normal_angles)
    bpy.utils.register_class(MESH_OT_save_vertex_normal_angles)
    bpy.types.Scene.vertex_normal_angles = bpy.props.CollectionProperty(type=VertexNormalAngleItem)

def unregister():
    bpy.utils.unregister_class(VertexNormalAngleItem)
    bpy.utils.unregister_class(MESH_OT_calculate_vertex_normal_angles)
    bpy.utils.unregister_class(MESH_PT_vertex_normal_angle_panel)
    bpy.utils.unregister_class(MESH_OT_clear_vertex_normal_angles)
    bpy.utils.unregister_class(MESH_OT_save_vertex_normal_angles)
    del bpy.types.Scene.vertex_normal_angles

if __name__ == "__main__":
    register()
