import flet as ft
from controllers.material_controller import MaterialController

def materials_view(page: ft.Page):
    controller = MaterialController()

    # Inputs
    name_input = ft.TextField(label="Nombre del Material")
    description_input = ft.TextField(label="Descripción", multiline=True)
    cost_input = ft.TextField(label="Costo Unitario", keyboard_type=ft.KeyboardType.NUMBER)

    # Tabla de materiales
    materials_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Costo Unitario")),
        ],
        rows=[],
    )

    def refresh_materials():
        materials = controller.load_materials()
        materials_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(m[0]))),
                    ft.DataCell(ft.Text(m[1])),
                    ft.DataCell(ft.Text(m[2])),
                    ft.DataCell(ft.Text(str(m[3]))),
                ]
            )
            for m in materials
        ]
        page.update()

    def add_material(e):
        controller.add_material(
            name_input.value, description_input.value, float(cost_input.value)
        )
        refresh_materials()

    refresh_materials()

    return ft.Column([
        ft.Row([name_input, description_input, cost_input]),
        ft.ElevatedButton("Guardar", on_click=add_material),
        materials_table,
    ])
