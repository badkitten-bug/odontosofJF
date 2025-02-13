import flet as ft
from controllers.treatment_material_controller import TreatmentMaterialController
from controllers.treatment_controller import TreatmentController
from controllers.material_controller import MaterialController

def treatment_materials_view(page: ft.Page):
    treatment_controller = TreatmentController()
    material_controller = MaterialController()
    controller = TreatmentMaterialController()

    # Dropdowns para tratamientos y materiales
    treatments_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(t[0], text=t[1]) for t in treatment_controller.load_treatments()
        ],
        label="Seleccionar Tratamiento",
    )
    materials_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option(m[0], text=m[1]) for m in material_controller.load_materials()
        ],
        label="Seleccionar Material",
    )
    quantity_input = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)

    # Tabla de relaciones
    relationships_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Tratamiento")),
            ft.DataColumn(ft.Text("Material")),
            ft.DataColumn(ft.Text("Cantidad")),
        ],
        rows=[],
    )

    def refresh_relationships():
        relationships = controller.get_all_relationships()
        relationships_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(r[0])),  # Tratamiento
                    ft.DataCell(ft.Text(r[1])),  # Material
                    ft.DataCell(ft.Text(str(r[2]))),  # Cantidad
                ]
            )
            for r in relationships
        ]
        page.update()

    def add_relationship(e):
        controller.add_relation(
            int(treatments_dropdown.value),
            int(materials_dropdown.value),
            int(quantity_input.value),
        )
        refresh_relationships()

    refresh_relationships()

    return ft.Column([
        ft.Row([treatments_dropdown, materials_dropdown, quantity_input]),
        ft.ElevatedButton("Asignar", on_click=add_relationship),
        relationships_table,
    ])
