import flet as ft
from controllers.treatment_controller import TreatmentController

def treatment_view(page: ft.Page, dynamic_content: ft.Column, menu_controller, historia_id: int):
    controller = TreatmentController()

    # **Lista de Tratamientos Aplicados**
    def load_applied_treatments():
        applied_treatments_list.controls.clear()
        for treatment in controller.get_treatments_by_historia(historia_id):
            applied_treatments_list.controls.append(create_treatment_row(treatment))
        page.update()

    # **Fila de tratamiento aplicado**
    def create_treatment_row(treatment):
        treatment_id, name, description, notes = treatment
        return ft.Row([
            ft.Text(name, width=150),
            ft.Text(description, width=250),
            ft.Text(notes, width=200)
        ], spacing=10)

    # **Diálogo para aplicar un nuevo tratamiento**
    def open_apply_treatment_dialog():
        available_treatments = controller.get_treatments()
        treatment_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(str(t[0]), t[1]) for t in available_treatments],
            label="Seleccionar Tratamiento"
        )
        notes_input = ft.TextField(label="Notas sobre el tratamiento")

        def save_treatment(e):
            treatment_id = int(treatment_dropdown.value)
            notes = notes_input.value
            controller.apply_treatment(historia_id, treatment_id, notes)
            page.close(dialog)
            page.snack_bar = ft.SnackBar(ft.Text("Tratamiento aplicado correctamente."), open=True)
            page.update()
            load_applied_treatments()

        dialog = ft.AlertDialog(
            title=ft.Text("Aplicar Tratamiento"),
            content=ft.Column([treatment_dropdown, notes_input], spacing=10),
            actions=[
                ft.TextButton("Guardar", on_click=save_treatment),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = dialog
        page.open(dialog)

    # **Lista de Tratamientos Aplicados**
    applied_treatments_list = ft.Column(scroll=ft.ScrollMode.AUTO)
    load_applied_treatments()

    return ft.Column([
        ft.Text("Tratamientos Aplicados", size=24, weight="bold"),
        ft.ElevatedButton("Aplicar Tratamiento", on_click=lambda e: open_apply_treatment_dialog()),
        ft.Container(applied_treatments_list, padding=10, border_radius=5, bgcolor=ft.Colors.WHITE, shadow=ft.BoxShadow(blur_radius=5)),
        ft.ElevatedButton("Volver", on_click=lambda e: menu_controller.show_history_detail_view(dynamic_content, historia_id))
    ], spacing=10)
