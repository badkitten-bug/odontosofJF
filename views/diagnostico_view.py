import flet as ft
from controllers.diagnostico_controller import DiagnosticoController

def diagnostico_view(page: ft.Page, dynamic_content: ft.Column, menu_controller, historia_id: int):
    controller = DiagnosticoController()
    diagnosticos = controller.get_diagnosticos(historia_id)

    # **Lista de Diagnósticos**
    def create_diagnostico_row(diagnostico):
        diagnostico_id, diagnostico_text, observaciones = diagnostico
        return ft.ListTile(
            title=ft.Text(diagnostico_text),
            subtitle=ft.Text(observaciones),
            trailing=ft.IconButton(
                icon=ft.Icons.EDIT,
                on_click=lambda e: open_edit_dialog(diagnostico_id, diagnostico_text, observaciones)
            )
        )

    # **Abrir Diálogo para Agregar/Editar Diagnóstico**
    def open_edit_dialog(diagnostico_id=None, diagnostico_text="", observaciones=""):
        diagnostico_input = ft.TextField(label="Diagnóstico", value=diagnostico_text)
        observaciones_input = ft.TextField(label="Observaciones", value=observaciones)

        def save_diagnostico(e):
            new_diagnostico = diagnostico_input.value
            new_observaciones = observaciones_input.value

            if diagnostico_id:
                controller.update_diagnostico(diagnostico_id, new_diagnostico, new_observaciones)
            else:
                controller.add_diagnostico(historia_id, new_diagnostico, new_observaciones)

            page.snack_bar = ft.SnackBar(ft.Text("Diagnóstico guardado correctamente."))
            page.snack_bar.open = True
            page.update()
            page.close(dialog)

            refresh_diagnosticos()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar/Editar Diagnóstico"),
            content=ft.Column([diagnostico_input, observaciones_input]),
            actions=[
                ft.TextButton("Guardar", on_click=save_diagnostico),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        page.open(dialog)

    # **Actualizar la Lista de Diagnósticos**
    def refresh_diagnosticos():
        diagnostico_list.controls.clear()
        for d in controller.get_diagnosticos(historia_id):
            diagnostico_list.controls.append(create_diagnostico_row(d))
        page.update()

    diagnostico_list = ft.Column([create_diagnostico_row(d) for d in diagnosticos])

    return ft.Container(
        ft.Column([
            ft.Text("Diagnóstico", size=24, weight="bold"),
            diagnostico_list,
            ft.ElevatedButton("Agregar Diagnóstico", on_click=lambda e: open_edit_dialog()),
            ft.ElevatedButton("Volver", on_click=lambda e: menu_controller.show_history_detail_view(dynamic_content, historia_id))
        ], spacing=10),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.GREY_300)
    )
