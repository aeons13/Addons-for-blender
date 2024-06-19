import bpy
import math

# Definimos las constantes matemáticas, físicas y de otros campos de estudio
constants = {
    "Math": {
        'π': math.pi,
        'e': math.e,
        'τ': math.tau,
        '∞': float('inf'),
    },
    "Physics": {
        'c': 299792458,  # velocidad de la luz en m/s
        'G': 6.67430e-11,  # constante de gravitación en m^3 kg^-1 s^-2
        'h': 6.62607015e-34,  # constante de Planck en J s
        'k': 1.380649e-23,  # constante de Boltzmann en J K^-1
    },
    "Chemistry": {
        'Mol': 6.02214076e23,  # número de Avogadro (mol^-1)
        'Gases': 8.314462618,  # constante de los gases ideales (J/(mol·K))
    },
    "Other": {
        'Gravedad': 9.81,  # aceleración de la gravedad en m/s^2
        'Ry': 10973731.6,  # constante de Rydberg (m^-1)
    },
}

# Conversión entre grados y radianes
def deg_to_rad(degrees):
    return math.radians(degrees)

def rad_to_deg(radians):
    return math.degrees(radians)

class ScientificCalculatorPanel(bpy.types.Panel):
    bl_label = "Scientific Calculator"
    bl_idname = "VIEW3D_PT_scientific_calculator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Calculator'

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        # Display calculator screen
        col.label(text="Calculator")
        col.prop(context.scene, "calculator_screen", text="", emboss=False)

        # Display calculator buttons
        row = col.row(align=True)
        row.operator("calculator.input", text="7").value = "7"
        row.operator("calculator.input", text="8").value = "8"
        row.operator("calculator.input", text="9").value = "9"
        row.operator("calculator.input", text="(").value = "("
        row.operator("calculator.input", text=")").value = ")"
        row.operator("calculator.input", text="/").value = "/"

        row = col.row(align=True)
        row.operator("calculator.input", text="4").value = "4"
        row.operator("calculator.input", text="5").value = "5"
        row.operator("calculator.input", text="6").value = "6"
        row.operator("calculator.input", text="*").value = "*"
        row.operator("calculator.input", text="π").value = "math.pi"
        row.operator("calculator.input", text="e").value = "math.e"

        row = col.row(align=True)
        row.operator("calculator.input", text="1").value = "1"
        row.operator("calculator.input", text="2").value = "2"
        row.operator("calculator.input", text="3").value = "3"
        row.operator("calculator.input", text="-").value = "-"
        row.operator("calculator.input", text="sqrt").value = "math.sqrt("
        row.operator("calculator.input", text="∞").value = "float('inf')"

        row = col.row(align=True)
        row.operator("calculator.input", text="0").value = "0"
        row.operator("calculator.input", text=".").value = "."
        row.operator("calculator.input", text="C").value = "C"
        row.operator("calculator.input", text="+").value = "+"
        row.operator("calculator.input", text="π/2").value = "math.pi/2"
        row.operator("calculator.input", text="τ").value = "math.tau"

        row = col.row(align=True)
        row.operator("calculator.calculate", text="=").operator = "="
        row.operator("calculator.undo", text="Undo")

        # Advanced functions
        col.separator()
        col.label(text="Functions")
        row = col.row(align=True)
        row.operator("calculator.input", text="sin").value = "math.sin("
        row.operator("calculator.input", text="cos").value = "math.cos("
        row.operator("calculator.input", text="tan").value = "math.tan("
        row.operator("calculator.input", text="asin").value = "math.asin("

        row = col.row(align=True)
        row.operator("calculator.input", text="acos").value = "math.acos("
        row.operator("calculator.input", text="atan").value = "math.atan("
        row.operator("calculator.input", text="log").value = "math.log("
        row.operator("calculator.input", text="exp").value = "math.exp("

        row = col.row(align=True)
        row.operator("calculator.input", text="pow").value = "math.pow("
        row.operator("calculator.input", text="abs").value = "abs("

        # Display constants in a dropdown menu
        col.separator()
        col.label(text="Constants")
        col.prop(context.scene, "constant_category", text="Category")
        col.prop(context.scene, "constant_value", text="Constant")

        row = col.row(align=True)
        row.operator("calculator.constant_input", text="Use Constant")

        # Degree and Radian Conversion
        col.separator()
        col.label(text="Angle Conversion")
        row = col.row(align=True)
        row.operator("calculator.deg_to_rad", text="Deg to Rad")
        row.operator("calculator.rad_to_deg", text="Rad to Deg")

class CalculatorInputOperator(bpy.types.Operator):
    bl_idname = "calculator.input"
    bl_label = "Calculator Input"
    value: bpy.props.StringProperty()

    def execute(self, context):
        screen = context.scene.calculator_screen
        if self.value == "C":
            screen = ""
        else:
            screen += self.value
        context.scene.calculator_screen = screen
        return {'FINISHED'}

class CalculatorCalculateOperator(bpy.types.Operator):
    bl_idname = "calculator.calculate"
    bl_label = "Calculator Calculate"
    operator: bpy.props.StringProperty()

    def execute(self, context):
        screen = context.scene.calculator_screen
        try:
            # Evaluar la expresión de forma segura
            result = eval(screen, {"__builtins__": None}, {"math": math, **constants["Math"], **constants["Physics"], **constants["Chemistry"], **constants["Other"]})
            context.scene.calculator_screen = str(result)
        except Exception as e:
            context.scene.calculator_screen = "Error"
        return {'FINISHED'}

class CalculatorDegToRadOperator(bpy.types.Operator):
    bl_idname = "calculator.deg_to_rad"
    bl_label = "Degree to Radian Conversion"

    def execute(self, context):
        screen = context.scene.calculator_screen
        try:
            degrees = float(screen)
            radians = deg_to_rad(degrees)
            context.scene.calculator_screen = str(radians)
        except Exception as e:
            context.scene.calculator_screen = "Error"
        return {'FINISHED'}

class CalculatorRadToDegOperator(bpy.types.Operator):
    bl_idname = "calculator.rad_to_deg"
    bl_label = "Radian to Degree Conversion"

    def execute(self, context):
        screen = context.scene.calculator_screen
        try:
            radians = float(screen)
            degrees = rad_to_deg(radians)
            context.scene.calculator_screen = str(degrees)
        except Exception as e:
            context.scene.calculator_screen = "Error"
        return {'FINISHED'}

class CalculatorUndoOperator(bpy.types.Operator):
    bl_idname = "calculator.undo"
    bl_label = "Calculator Undo"

    def execute(self, context):
        screen = context.scene.calculator_screen
        if screen:
            context.scene.calculator_screen = screen[:-1]
        return {'FINISHED'}

def update_constant_value(self, context):
    category = context.scene.constant_category
    constants_dict = constants[category]
    context.scene.constant_value = str(list(constants_dict.values())[0])

def get_constant_items(self, context):
    category = context.scene.constant_category
    constants_dict = constants[category]
    return [(str(value), const, "") for const, value in constants_dict.items()]

class ConstantInputOperator(bpy.types.Operator):
    bl_idname = "calculator.constant_input"
    bl_label = "Constant Input"

    def execute(self, context):
        screen = context.scene.calculator_screen
        constant = context.scene.constant_value
        screen += constant
        context.scene.calculator_screen = screen
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ScientificCalculatorPanel)
    bpy.utils.register_class(CalculatorInputOperator)
    bpy.utils.register_class(CalculatorCalculateOperator)
    bpy.utils.register_class(CalculatorDegToRadOperator)
    bpy.utils.register_class(CalculatorRadToDegOperator)
    bpy.utils.register_class(CalculatorUndoOperator)
    bpy.utils.register_class(ConstantInputOperator)

    bpy.types.Scene.calculator_screen = bpy.props.StringProperty(name="Calculator Screen", default="")
    bpy.types.Scene.constant_category = bpy.props.EnumProperty(
        name="Constant Category",
        items=[(cat, cat, "") for cat in constants.keys()],
        update=update_constant_value
    )
    bpy.types.Scene.constant_value = bpy.props.EnumProperty(
        name="Constant Value",
        items=get_constant_items,
    )

def unregister():
    bpy.utils.unregister_class(ScientificCalculatorPanel)
    bpy.utils.unregister_class(CalculatorInputOperator)
    bpy.utils.unregister_class(CalculatorCalculateOperator)
    bpy.utils.unregister_class(CalculatorDegToRadOperator)
    bpy.utils.unregister_class(CalculatorRadToDegOperator)
    bpy.utils.unregister_class(CalculatorUndoOperator)
    bpy.utils.unregister_class(ConstantInputOperator)

    del bpy.types.Scene.calculator_screen
    del bpy.types.Scene.constant_category
    del bpy.types.Scene.constant_value

if __name__ == "__main__":
    register()
