# views/treatment_view.py
import flet as ft
from controllers.treatment_controller import TreatmentController
from controllers.material_controller import MaterialController

def treatment_view(page: ft.Page):
    treatment_controller = TreatmentController()
    material_controller = MaterialController()

    # Inputs
    name_input = ft.TextField(label="Nombre del Tratamiento")
    description_input = ft.TextField(label="Descripción", multiline=True)
    cost_input = ft.TextField(label="Costo", keyboard_type=ft.KeyboardType.NUMBER)
    category_input = ft.Dropdown(
        options=[ft.dropdown.Option("Curaciones"), ft.dropdown.Option("Extracciones"), ft.dropdown.Option("Endodoncia"), ft.dropdown.Option("Prótesis")],
        label="Categoría"
    )

    # Tabla de tratamientos
    treatments_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Costo")),
            ft.DataColumn(ft.Text("Categoría"))
        ],
        rows=[]
    )

    def refresh_treatments():
        treatments = treatment_controller.load_treatments()
        treatments_table.rows = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(str(t[0]))),
                ft.DataCell(ft.Text(t[1])),
                ft.DataCell(ft.Text(t[2])),
                ft.DataCell(ft.Text(str(t[3]))),
                ft.DataCell(ft.Text(t[4]))
            ]) for t in treatments
        ]
        page.update()

    def add_treatment(e):
        treatment_controller.add_treatment(
            name_input.value, description_input.value, float(cost_input.value), category_input.value
        )
        refresh_treatments()

    add_button = ft.ElevatedButton("Guardar", on_click=add_treatment)

    refresh_treatments()

    return ft.Column([
        ft.Row([name_input, description_input, cost_input, category_input]),
        add_button,
        treatments_table
    ])
