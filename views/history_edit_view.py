import flet as ft
from controllers.historia_controller import HistoriaController

def history_edit_view(page: ft.Page, history_id: int):
    controller = HistoriaController()
    
    # Cargar datos de la historia; idealmente, el controlador debe retornar un diccionario.
    history = controller.get_historia(history_id)
    if not history:
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Error: No se pudo cargar la historia clínica.", color="red"),
            duration=4000
        )
        page.snack_bar.open = True
        page.update()
        return

    # Por ejemplo, usamos un input para editar observaciones.
    # Puedes agregar más inputs para cada sección (exploración física, odontograma, etc.).
    observaciones_input = ft.TextField(label="Observaciones", value=history.get("observaciones", ""), multiline=True, width=400)
    
    # (Opcional) Agrega otros inputs para otras secciones...
    # exploracion_input = ft.TextField(label="Exploración Física", value=history.get("exploracion_fisica", ""), multiline=True, width=400)
    # odontograma_input = ft.TextField(label="Odontograma", value=history.get("odontograma", ""), multiline=True, width=400)
    # etc.

    def save_history(e):
        # Recoge los valores editados.
        observaciones = observaciones_input.value
        # Recoger otros campos si se agregaron
        # exploracion = exploracion_input.value
        # odontograma = odontograma_input.value
        # Llamar al controlador para actualizar la historia.
        # Aquí en el ejemplo usamos update_historia pasando vacíos para los otros campos.
        controller.update_historia(history_id, observaciones, "", "", "", "", "", "", "", "")
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Historia clínica actualizada correctamente", color="green"),
            duration=4000
        )
        page.snack_bar.open = True
        page.update()
        # Redirige a la vista de gestión o a la vista detalle, según prefieras.
        page.go("/history-management")

    # Layout de la vista de edición.
    return ft.Column([
        ft.Text("Editar Historia Clínica", size=24, weight="bold"),
        ft.Text(f"Historia: {history.get('history_number', '')}"),  # Número de historia del paciente
        ft.Divider(),
        observaciones_input,
        # Agrega aquí otros inputs para las secciones que desees editar.
        ft.ElevatedButton("Guardar Cambios", on_click=save_history),
        ft.ElevatedButton("Cancelar", on_click=lambda e: page.go("/history-management"))
    ])
