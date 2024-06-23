import bpy
import bmesh
import math
from mathutils import Vector
import os

class CalcularAnguloAristaRadioOperator(bpy.types.Operator):
    bl_idname = "object.calcular_angulo_arista_radio"
    bl_label = "Calcular Ángulos del Triángulo"
    bl_description = "Calcula los ángulos del triángulo formado por la arista seleccionada y el radio desde el centro del objeto"

    def execute(self, context):
        # Obtener el objeto activo
        obj = context.active_object
        
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Por favor, selecciona un objeto de malla.")
            return {'CANCELLED'}
        
        # Crear un bmesh del objeto
        bm = bmesh.from_edit_mesh(obj.data)
        
        # Obtener la arista seleccionada
        arista_seleccionada = [e for e in bm.edges if e.select]
        
        if len(arista_seleccionada) != 1:
            self.report({'ERROR'}, "Por favor, selecciona exactamente una arista.")
            return {'CANCELLED'}
        
        arista = arista_seleccionada[0]
        
        # Calcular el punto medio de la arista
        punto_medio = (arista.verts[0].co + arista.verts[1].co) / 2
        
        # Calcular la longitud de la arista
        longitud_arista = (arista.verts[1].co - arista.verts[0].co).length
        
        # Calcular la distancia desde el centro del objeto al punto medio de la arista (radio)
        radio = (punto_medio - obj.location).length
        
        # Calcular las longitudes de los otros dos lados del triángulo
        longitud_a = longitud_arista
        longitud_b = radio
        longitud_c = (arista.verts[0].co - obj.location).length
        
        # Calcular los ángulos del triángulo usando la ley de cosenos
        angulo_A = math.acos((longitud_b**2 + longitud_c**2 - longitud_a**2) / (2 * longitud_b * longitud_c))
        angulo_B = math.acos((longitud_a**2 + longitud_c**2 - longitud_b**2) / (2 * longitud_a * longitud_c))
        angulo_C = math.acos((longitud_a**2 + longitud_b**2 - longitud_c**2) / (2 * longitud_a * longitud_b))
        
        # Convertir los ángulos de radianes a grados
        angulo_A_grados = math.degrees(angulo_A)
        angulo_B_grados = math.degrees(angulo_B)
        angulo_C_grados = math.degrees(angulo_C)
        
        # Añadir los ángulos a la colección de ángulos
        item = context.scene.angulo_collection.add()
        item.angulo_text = f"Ángulo A: {angulo_A_grados:.2f}°, Ángulo B: {angulo_B_grados:.2f}°, Ángulo C: {angulo_C_grados:.2f}°"
        
        self.report({'INFO'}, "Ángulos calculados y añadidos a la lista")
        return {'FINISHED'}

class GuardarAngulosOperator(bpy.types.Operator):
    bl_idname = "object.guardar_angulos"
    bl_label = "Guardar Ángulos"
    bl_description = "Guardar los ángulos calculados en un archivo de texto"

    def execute(self, context):
        file_path = os.path.join(bpy.path.abspath("//"), "angulos_calculados.txt")
        with open(file_path, 'a') as file:
            for item in context.scene.angulo_collection:
                file.write(item.angulo_text + '\n')
        
        self.report({'INFO'}, f"Ángulos guardados en {file_path}")
        return {'FINISHED'}

class AnguloItem(bpy.types.PropertyGroup):
    angulo_text: bpy.props.StringProperty()

class CalcularAnguloAristaRadioPanel(bpy.types.Panel):
    bl_label = "Calcular Ángulos del Triángulo"
    bl_idname = "OBJECT_PT_calcular_angulo_arista_radio"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("object.calcular_angulo_arista_radio")
        layout.operator("object.guardar_angulos")

        # Mostrar la lista de ángulos calculados
        if hasattr(scene, "angulo_collection"):
            for item in scene.angulo_collection:
                layout.label(text=item.angulo_text)

def register():
    bpy.utils.register_class(CalcularAnguloAristaRadioOperator)
    bpy.utils.register_class(GuardarAngulosOperator)
    bpy.utils.register_class(AnguloItem)
    bpy.utils.register_class(CalcularAnguloAristaRadioPanel)
    bpy.types.Scene.angulo_collection = bpy.props.CollectionProperty(type=AnguloItem)

def unregister():
    bpy.utils.unregister_class(CalcularAnguloAristaRadioOperator)
    bpy.utils.unregister_class(GuardarAngulosOperator)
    bpy.utils.unregister_class(AnguloItem)
    bpy.utils.unregister_class(CalcularAnguloAristaRadioPanel)
    del bpy.types.Scene.angulo_collection

if __name__ == "__main__":
    register()

