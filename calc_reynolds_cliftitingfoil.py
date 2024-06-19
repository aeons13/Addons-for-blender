bl_info = {
    "name": "Reynolds and Lift Calculator",
    "author": "ChatGPT",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Reynolds & Lift",
    "description": "Calculates the Reynolds number and lift force",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

import bpy

class ReynoldsCalculatorPanel(bpy.types.Panel):
    bl_label = "Reynolds Calculator"
    bl_idname = "OBJECT_PT_reynolds_calculator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Reynolds & Lift'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Reynolds Number Calculation")
        layout.prop(scene, "density")
        layout.prop(scene, "velocity")
        layout.prop(scene, "characteristic_length")
        layout.prop(scene, "viscosity")
        layout.operator("object.calculate_reynolds", text="Calculate Reynolds Number")
        layout.label(text="Reynolds Number: " + str(scene.reynolds_number))

class LiftCalculatorPanel(bpy.types.Panel):
    bl_label = "Lift Calculator"
    bl_idname = "OBJECT_PT_lift_calculator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Reynolds & Lift'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.label(text="Lift Force Calculation")
        layout.prop(scene, "density_lift")
        layout.prop(scene, "velocity_lift")
        layout.prop(scene, "wing_area")
        layout.prop(scene, "lift_coefficient")
        layout.operator("object.calculate_lift", text="Calculate Lift Force")
        layout.label(text="Lift Force: " + str(scene.lift_force) + " N")

class CalculateReynoldsOperator(bpy.types.Operator):
    bl_label = "Calculate Reynolds"
    bl_idname = "object.calculate_reynolds"

    def execute(self, context):
        scene = context.scene
        density = scene.density
        velocity = scene.velocity
        characteristic_length = scene.characteristic_length
        viscosity = scene.viscosity
        
        # Calculate Reynolds Number
        reynolds_number = (density * velocity * characteristic_length) / viscosity
        scene.reynolds_number = reynolds_number
        
        return {'FINISHED'}

class CalculateLiftOperator(bpy.types.Operator):
    bl_label = "Calculate Lift"
    bl_idname = "object.calculate_lift"

    def execute(self, context):
        scene = context.scene
        density = scene.density_lift
        velocity = scene.velocity_lift
        wing_area = scene.wing_area
        lift_coefficient = scene.lift_coefficient
        
        # Calculate Lift Force
        lift_force = 0.5 * density * (velocity ** 2) * wing_area * lift_coefficient
        scene.lift_force = lift_force
        
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ReynoldsCalculatorPanel)
    bpy.utils.register_class(LiftCalculatorPanel)
    bpy.utils.register_class(CalculateReynoldsOperator)
    bpy.utils.register_class(CalculateLiftOperator)
    
    bpy.types.Scene.density = bpy.props.FloatProperty(
        name="Density (kg/m^3)",
        description="Density of the fluid for Reynolds calculation",
        default=1.225,
        min=0.0
    )
    
    bpy.types.Scene.velocity = bpy.props.FloatProperty(
        name="Velocity (m/s)",
        description="Velocity of the fluid for Reynolds calculation",
        default=10.0,
        min=0.0
    )
    
    bpy.types.Scene.characteristic_length = bpy.props.FloatProperty(
        name="Characteristic Length (m)",
        description="Characteristic length of the object for Reynolds calculation",
        default=1.0,
        min=0.0
    )
    
    bpy.types.Scene.viscosity = bpy.props.FloatProperty(
        name="Viscosity (Pa.s)",
        description="Dynamic viscosity of the fluid for Reynolds calculation",
        default=0.0000181,
        min=0.0
    )
    
    bpy.types.Scene.reynolds_number = bpy.props.FloatProperty(
        name="Reynolds Number",
        description="Calculated Reynolds Number",
        default=0.0
    )
    
    bpy.types.Scene.density_lift = bpy.props.FloatProperty(
        name="Density (kg/m^3)",
        description="Density of the fluid for lift calculation",
        default=1.225,
        min=0.0
    )
    
    bpy.types.Scene.velocity_lift = bpy.props.FloatProperty(
        name="Velocity (m/s)",
        description="Velocity of the fluid for lift calculation",
        default=10.0,
        min=0.0
    )
    
    bpy.types.Scene.wing_area = bpy.props.FloatProperty(
        name="Wing Area (m²)",
        description="Wing area of the airplane",
        default=20.0,
        min=0.0
    )
    
    bpy.types.Scene.lift_coefficient = bpy.props.FloatProperty(
        name="Lift Coefficient (C_L)",
        description="Lift coefficient",
        default=1.5,
        min=0.0
    )
    
    bpy.types.Scene.lift_force = bpy.props.FloatProperty(
        name="Lift Force (N)",
        description="Calculated Lift Force",
        default=0.0
    )

def unregister():
    bpy.utils.unregister_class(ReynoldsCalculatorPanel)
    bpy.utils.unregister_class(LiftCalculatorPanel)
    bpy.utils.unregister_class(CalculateReynoldsOperator)
    bpy.utils.unregister_class(CalculateLiftOperator)
    
    del bpy.types.Scene.density
    del bpy.types.Scene.velocity
    del bpy.types.Scene.characteristic_length
    del bpy.types.Scene.viscosity
    del bpy.types.Scene.reynolds_number
    del bpy.types.Scene.density_lift
    del bpy.types.Scene.velocity_lift
    del bpy.types.Scene.wing_area
    del bpy.types.Scene.lift_coefficient
    del bpy.types.Scene.lift_force

if __name__ == "__main__":
    register()
