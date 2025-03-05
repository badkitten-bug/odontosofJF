import flet as ft
from controllers.treatment_controller import TreatmentController

def treatments_management_view(page: ft.Page):
    controller = TreatmentController()

    # **Lista de Tratamientos**
    def load_treatments():
        treatments_list.controls.clear()
        for treatment in controller.get_treatments():
            treatments_list.controls.append(create_treatment_row(treatment))
        page.update()

    # **Crear fila de tratamiento**
    def create_treatment_row(treatment):
        treatment_id, name, description, cost = treatment

        return ft.Row([
            ft.Text(name, width=150),
            ft.Text(description, width=250),
            ft.Text(f"S/. {cost}", width=80),
            ft.IconButton(ft.icons.EDIT, on_click=lambda e: open_edit_dialog(treatment_id, name, description, cost)),
            ft.IconButton(ft.icons.DELETE, on_click=lambda e: open_delete_dialog(treatment_id))
        ], spacing=10)

    # **Diálogo de edición**
    def open_edit_dialog(treatment_id, name, description, cost):
        name_input = ft.TextField(label="Nombre", value=name)
        description_input = ft.TextField(label="Descripción", value=description)
        cost_input = ft.TextField(label="Costo", value=str(cost))

        def save_changes(e):
            controller.update_treatment(treatment_id, name_input.value, description_input.value, float(cost_input.value))
            page.close(dialog)
            page.snack_bar = ft.SnackBar(ft.Text("Tratamiento actualizado correctamente."), open=True)
            page.update()
            load_treatments()

        dialog = ft.AlertDialog(
            title=ft.Text("Editar Tratamiento"),
            content=ft.Column([name_input, description_input, cost_input], spacing=10),
            actions=[
                ft.TextButton("Guardar", on_click=save_changes),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        page.open(dialog)

    # **Diálogo de eliminación**
    def open_delete_dialog(treatment_id):
        def confirm_delete(e):
            controller.delete_treatment(treatment_id)
            page.close(dialog)
            page.snack_bar = ft.SnackBar(ft.Text("Tratamiento eliminado."), open=True)
            page.update()
            load_treatments()

        dialog = ft.AlertDialog(
            title=ft.Text("Eliminar Tratamiento"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este tratamiento?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.TextButton("Eliminar", on_click=confirm_delete)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        page.open(dialog)

    # **Formulario para agregar tratamiento**
    name_input = ft.TextField(label="Nombre del Tratamiento")
    description_input = ft.TextField(label="Descripción")
    cost_input = ft.TextField(label="Costo")

    def add_treatment(e):
        controller.add_treatment(name_input.value, description_input.value, float(cost_input.value))
        page.snack_bar = ft.SnackBar(ft.Text("Tratamiento agregado correctamente."), open=True)
        page.update()
        load_treatments()
        name_input.value, description_input.value, cost_input.value = "", "", ""
        page.update()

    # **Interfaz**
    treatments_list = ft.Column(scroll=ft.ScrollMode.AUTO)

    return ft.Column([
        ft.Text("Gestión de Tratamientos", size=24, weight="bold"),
        ft.Row([name_input, description_input, cost_input, ft.ElevatedButton("Agregar", on_click=add_treatment)], spacing=10),
        ft.Container(treatments_list, padding=10, border_radius=5, bgcolor=ft.Colors.WHITE, shadow=ft.BoxShadow(blur_radius=5)),
    ], spacing=10)
