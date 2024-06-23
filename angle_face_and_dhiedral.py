import bpy
import math
from mathutils import Vector
from bpy.props import StringProperty, CollectionProperty

class AngleMeasurement(bpy.types.PropertyGroup):
    value: StringProperty()

class PANEL_PT_MedidasAngulos(bpy.types.Panel):
    bl_label = "Medidas de Ángulos y Aristas"
    bl_idname = "PANEL_PT_MedidasAngulos"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.operator("script.obtener_medidas", text="Actualizar Medidas")

        layout.label(text="Registro de medidas:")
        for item in scene.measurement_register:
            layout.label(text=item.value)

        row = layout.row()
        row.operator("script.limpiar_registro", text="Limpiar Registro")

class SCRIPT_OT_ObtenerMedidas(bpy.types.Operator):
    bl_idname = "script.obtener_medidas"
    bl_label = "Obtener Medidas"
    bl_description = "Obtiene las medidas de ángulos y longitudes de las caras y aristas seleccionadas"

    def execute(self, context):
        measurements = obtener_y_escribir_medidas()
        agregar_a_editor_texto(measurements)
        
        # Agregar nuevas medidas al registro
        for line in measurements.split('\n'):
            if line:
                item = context.scene.measurement_register.add()
                item.value = line

        return {'FINISHED'}

class SCRIPT_OT_LimpiarRegistro(bpy.types.Operator):
    bl_idname = "script.limpiar_registro"
    bl_label = "Limpiar Registro"
    bl_description = "Limpia el registro de medidas"

    def execute(self, context):
        context.scene.measurement_register.clear()
        limpiar_editor_texto()
        return {'FINISHED'}

def obtener_y_escribir_medidas():
    obj = bpy.context.active_object
    if not (obj and obj.type == 'MESH' and obj.mode == 'EDIT'):
        return "Seleccione un objeto de malla en modo de edición."

    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = obj.data
    
    result = []
    
    selected_faces = [f for f in mesh.polygons if f.select]
    for face in selected_faces:
        angles = calcular_angulos_poligono(mesh, face)
        result.append(f"Cara {face.index}: Ángulos = {[f'{a:.2f}°' for a in angles]}")
    
    selected_edges = [e for e in mesh.edges if e.select]
    for edge in selected_edges:
        angle = calcular_angulo_borde(mesh, edge)
        length = calcular_longitud_arista(mesh, edge)
        if angle is not None:
            result.append(f"Borde {edge.index}: Ángulo = {angle:.2f}°, Longitud = {length:.4f}")
        else:
            result.append(f"Borde {edge.index}: No se pudo calcular el ángulo, Longitud = {length:.4f}")
    
    bpy.ops.object.mode_set(mode='EDIT')
    return '\n'.join(result)

def calcular_angulos_poligono(mesh, face):
    vertices = face.vertices
    angles = []
    for i in range(len(vertices)):
        v1 = mesh.vertices[vertices[i]].co
        v2 = mesh.vertices[vertices[(i + 1) % len(vertices)]].co
        v3 = mesh.vertices[vertices[(i - 1) % len(vertices)]].co
        vec1 = (v2 - v1).normalized()
        vec2 = (v3 - v1).normalized()
        angle = math.degrees(vec1.angle(vec2))
        angles.append(angle)
    return angles

def calcular_angulo_borde(mesh, edge):
    face_pair = []
    for face in mesh.polygons:
        if edge.key in face.edge_keys:
            face_pair.append(face)
    
    if len(face_pair) == 2:
        angle = face_pair[0].normal.angle(face_pair[1].normal)
        return math.degrees(angle)
    else:
        return None

def calcular_longitud_arista(mesh, edge):
    v1 = mesh.vertices[edge.vertices[0]].co
    v2 = mesh.vertices[edge.vertices[1]].co
    return (v2 - v1).length

def agregar_a_editor_texto(content):
    text_name = "Medidas de Ángulos y Aristas"
    if text_name not in bpy.data.texts:
        text = bpy.data.texts.new(text_name)
    else:
        text = bpy.data.texts[text_name]
    
    text.write(content + '\n\n')  # Agregar dos saltos de línea para separar las mediciones

def limpiar_editor_texto():
    text_name = "Medidas de Ángulos y Aristas"
    if text_name in bpy.data.texts:
        text = bpy.data.texts[text_name]
        text.clear()

classes = (
    AngleMeasurement,
    PANEL_PT_MedidasAngulos,
    SCRIPT_OT_ObtenerMedidas,
    SCRIPT_OT_LimpiarRegistro
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.measurement_register = CollectionProperty(type=AngleMeasurement)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.measurement_register

if __name__ == "__main__":
    register()