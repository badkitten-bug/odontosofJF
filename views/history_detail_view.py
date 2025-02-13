import flet as ft
from controllers.historia_controller import HistoriaController

def history_detail_view(page: ft.Page, history_id: int):
    controller = HistoriaController()
    history = controller.get_history_by_id(history_id)

    # Campos del formulario
    exploracion_fisica_input = ft.TextField(label="Exploración Física", multiline=True, value=history["exploracion_fisica"])
    odontograma_input = ft.TextField(label="Odontograma", multiline=True, value=history["odontograma"])
    diagnostico_input = ft.TextField(label="Diagnóstico", multiline=True, value=history["diagnostico"])
    evolucion_input = ft.TextField(label="Evolución", multiline=True, value=history["evolucion"])
    examenes_auxiliares_input = ft.TextField(label="Exámenes Auxiliares", multiline=True, value=history["examenes_auxiliares"])
    tratamientos_realizados_input = ft.TextField(label="Tratamientos Realizados", multiline=True, value=history["tratamientos_realizados"])

    # Función para guardar los cambios
    def save_changes(e):
        data = (
            exploracion_fisica_input.value,
            odontograma_input.value,
            diagnostico_input.value,
            evolucion_input.value,
            examenes_auxiliares_input.value,
            tratamientos_realizados_input.value,
        )
        controller.update_history(history_id, data)
        page.snack_bar = ft.SnackBar(ft.Text("Historia clínica actualizada correctamente"))
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        ft.Text("Historia Clínica", size=24, weight="bold"),
        ft.Text(f"Paciente: {history['nombres']} {history['apellidos']}"),
        ft.Text(f"Edad: {history['edad']}"),
        ft.Text(f"DNI: {history['dni']}"),
        ft.Text(f"Fecha de la Cita: {history['date']}"),
        ft.Text(f"Hora de la Cita: {history['time']}"),
        ft.Text(f"Estado: {history['estado']}"),
        ft.Divider(),
        exploracion_fisica_input,
        odontograma_input,
        diagnostico_input,
        evolucion_input,
        examenes_auxiliares_input,
        tratamientos_realizados_input,
        ft.ElevatedButton("Guardar Cambios", on_click=save_changes),
    ])