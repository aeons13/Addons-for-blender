import bpy
import math
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add

def add_tetraedro(self, context):
    verts = [
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, -1),
        (1, -1, -1)
    ]
    faces = [
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 1),
        (1, 2, 3)
    ]
    mesh = bpy.data.meshes.new(name="Tetraedro")
    mesh.from_pydata(verts, [], faces)
    object_data_add(context, mesh, operator=self)

def add_dodecaedro(self, context):
    phi = (1 + 5**0.5) / 2
    verts = [
        ( 1,  1,  1),
        ( 1,  1, -1),
        ( 1, -1,  1),
        ( 1, -1, -1),
        (-1,  1,  1),
        (-1,  1, -1),
        (-1, -1,  1),
        (-1, -1, -1),
        (0,  1/phi,  phi),
        (0,  1/phi, -phi),
        (0, -1/phi,  phi),
        (0, -1/phi, -phi),
        ( 1/phi,  phi, 0),
        ( 1/phi, -phi, 0),
        (-1/phi,  phi, 0),
        (-1/phi, -phi, 0),
        ( phi, 0,  1/phi),
        ( phi, 0, -1/phi),
        (-phi, 0,  1/phi),
        (-phi, 0, -1/phi)
    ]
    faces = [
        (0,  8,  10, 2,  16),
        (0,  16, 17, 1,  12),
        (0,  12, 14, 4,  8),
        (1,  9,  11, 3,  17),
        (2,  10, 6,  15, 13),
        (2,  13, 3,  17, 16),
        (3,  13, 15, 7,  11),
        (4,  14, 5,  19, 18),
        (4,  18, 6,  10, 8),
        (5,  9,  1,  12, 14),
        (5,  19, 7,  11, 9),
        (6,  18, 19, 7,  15)
    ]
    mesh = bpy.data.meshes.new(name="Dodecaedro")
    mesh.from_pydata(verts, [], faces)
    object_data_add(context, mesh, operator=self)

def add_octaedro(self, context):
    verts = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]
    faces = [
        (0, 2, 4),
        (0, 4, 3),
        (0, 3, 5),
        (0, 5, 2),
        (1, 2, 4),
        (1, 4, 3),
        (1, 3, 5),
        (1, 5, 2)
    ]
    mesh = bpy.data.meshes.new(name="Octaedro")
    mesh.from_pydata(verts, [], faces)
    object_data_add(context, mesh, operator=self)

class AddTetraedro(Operator, AddObjectHelper):
    bl_idname = "mesh.add_tetraedro"
    bl_label = "Add Tetraedro"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_tetraedro(self, context)
        return {'FINISHED'}

class AddDodecaedro(Operator, AddObjectHelper):
    bl_idname = "mesh.add_dodecaedro"
    bl_label = "Add Dodecaedro"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_dodecaedro(self, context)
        return {'FINISHED'}

class AddOctaedro(Operator, AddObjectHelper):
    bl_idname = "mesh.add_octaedro"
    bl_label = "Add Octaedro"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_octaedro(self, context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(AddTetraedro.bl_idname, icon='MESH_ICOSPHERE')
    self.layout.operator(AddDodecaedro.bl_idname, icon='MESH_ICOSPHERE')
    self.layout.operator(AddOctaedro.bl_idname, icon='MESH_ICOSPHERE')

def register():
    bpy.utils.register_class(AddTetraedro)
    bpy.utils.register_class(AddDodecaedro)
    bpy.utils.register_class(AddOctaedro)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddTetraedro)
    bpy.utils.unregister_class(AddDodecaedro)
    bpy.utils.unregister_class(AddOctaedro)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()