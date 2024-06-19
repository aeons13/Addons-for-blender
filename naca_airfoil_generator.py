bl_info = {
    "name": "NACA Airfoil and DAT File Loader",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh
import math
import numpy as np
import os

def parse_naca_number(naca_number):
    if len(naca_number) == 4:
        return "NACA4", int(naca_number[0]), int(naca_number[1]), int(naca_number[2:]) / 100
    elif len(naca_number) == 5:
        return "NACA5", int(naca_number[0]), int(naca_number[1:3]) / 100, int(naca_number[3:]) / 100
    else:
        raise ValueError("Invalid NACA number format")

def naca4_digit_airfoil(m, p, t, num_points=100):
    x = np.linspace(0, 1, num_points)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    
    yc = np.where(x <= p, m / p**2 * (2 * p * x - x**2), m / (1 - p)**2 * ((1 - 2 * p) + 2 * p * x - x**2))
    dyc_dx = np.where(x <= p, 2 * m / p**2 * (p - x), 2 * m / (1 - p)**2 * (p - x))
    theta = np.arctan(dyc_dx)
    
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    x_coords = np.concatenate([xu, xl[::-1]])
    y_coords = np.concatenate([yu, yl[::-1]])
    
    return x_coords, y_coords

def naca5_digit_airfoil(cl, p, t, num_points=100):
    x = np.linspace(0, 1, num_points)
    yt = 5 * t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
    
    if p == 0.15:
        m = 0.058
        k1 = 361.4
    elif p == 0.20:
        m = 0.126
        k1 = 51.64
    elif p == 0.25:
        m = 0.2025
        k1 = 15.957
    elif p == 0.30:
        m = 0.29
        k1 = 6.643
    elif p == 0.35:
        m = 0.391
        k1 = 3.23
    
    yc = np.where(x < p, k1 / 6 * (x**3 - 3 * m * x**2 + m**2 * (3 - m) * x), k1 / 6 * m**3 * (1 - x))
    dyc_dx = np.where(x < p, k1 / 6 * (3 * x**2 - 6 * m * x + m**2 * (3 - m)), -k1 / 6 * m**3)
    theta = np.arctan(dyc_dx)
    
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)
    
    x_coords = np.concatenate([xu, xl[::-1]])
    y_coords = np.concatenate([yu, yl[::-1]])
    
    return x_coords, y_coords

def load_airfoil_from_dat(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        
    coords = []
    for line in lines:
        try:
            x, y = map(float, line.split())
            coords.append((x, y))
        except ValueError:
            continue
    
    x_coords, y_coords = zip(*coords)
    return np.array(x_coords), np.array(y_coords)

class NACA_Airfoil_Generator(bpy.types.Operator):
    bl_idname = "mesh.naca_airfoil_generator"
    bl_label = "NACA Airfoil Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    naca_number: bpy.props.StringProperty(name="NACA Number", default="2412")
    color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', default=[0.8, 0.2, 0.2], min=0.0, max=1.0)
    use_dat_file: bpy.props.BoolProperty(name="Use DAT File", default=False)
    filepath: bpy.props.StringProperty(name="DAT File Path", subtype='FILE_PATH')

    def execute(self, context):
        if self.use_dat_file:
            if not os.path.isfile(self.filepath):
                self.report({'ERROR'}, "DAT file not found")
                return {'CANCELLED'}
            try:
                x_coords, y_coords = load_airfoil_from_dat(self.filepath)
            except Exception as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
        else:
            try:
                airfoil_type, param1, param2, param3 = parse_naca_number(self.naca_number)
                if airfoil_type == "NACA4":
                    x_coords, y_coords = naca4_digit_airfoil(param1 / 100, param2 / 10, param3)
                else:
                    x_coords, y_coords = naca5_digit_airfoil(param1 / 100, param2, param3)
            except ValueError as e:
                self.report({'ERROR'}, str(e))
                return {'CANCELLED'}
        
        mesh = bpy.data.meshes.new("NACA_Airfoil")
        bm = bmesh.new()
        
        verts = [bm.verts.new((x, y, 0)) for x, y in zip(x_coords, y_coords)]
        bm.verts.ensure_lookup_table()
        for i in range(len(verts) - 1):
            bm.edges.new([verts[i], verts[i + 1]])
        bm.edges.new([verts[-1], verts[0]])
        
        bm.to_mesh(mesh)
        bm.free()
        
        obj = bpy.data.objects.new("NACA_Airfoil", mesh)
        context.collection.objects.link(obj)
        
        mat = bpy.data.materials.new(name="AirfoilMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        bsdf.inputs['Emission'].default_value = (*self.color, 1)
        obj.data.materials.append(mat)
        
        # Ensure only edges are colored
        for edge in obj.data.edges:
            edge.use_freestyle_mark = True
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "use_dat_file")
        if self.use_dat_file:
            layout.prop(self, "filepath", text="DAT File Path")
        else:
            layout.prop(self, "naca_number")
        layout.prop(self, "color", text="Edge Color")

def menu_func(self, context):
    self.layout.operator(NACA_Airfoil_Generator.bl_idname)

def register():
    bpy.utils.register_class(NACA_Airfoil_Generator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(NACA_Airfoil_Generator)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

