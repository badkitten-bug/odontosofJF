import flet as ft
from controllers.historia_controller import HistoriaController

def history_detail_view(page: ft.Page, history_id: int):
    controller = HistoriaController()
    history = controller.get_history_by_id(history_id)

    if not history:
        page.snack_bar = ft.SnackBar(ft.Text("⚠️ Error: No se pudo cargar la historia clínica.", color="red"))
        page.snack_bar.open = True
        page.update()
        return

    # 📌 Información del paciente
    patient_info = ft.Column([
        ft.Text(f"Nombre: {history['nombres']} {history['apellidos']}"),
        ft.Text(f"Edad: {history['edad']}"),
        ft.Text(f"DNI: {history['dni']}"),
        ft.Text(f"Fecha de la Cita: {history['date']}"),
        ft.Text(f"Hora de la Cita: {history['time']}"),
        ft.Text(f"Estado: {history['estado']}"),
    ])

 
    # 📌 Menú lateral con accesos a secciones
    menu = ft.Column([
        ft.Text("📂 Datos del Paciente", size=18, weight="bold"),
        ft.ElevatedButton("Exploración Física", on_click=lambda e: page.go(f"/exploracion-fisica/{history_id}")),
        ft.ElevatedButton("Odontograma", on_click=lambda e: page.go(f"/odontograma/{history_id}")),
        ft.ElevatedButton("Diagnóstico", on_click=lambda e: page.go(f"/diagnostico/{history_id}")),
        ft.ElevatedButton("Evolución", on_click=lambda e: page.go(f"/evolucion/{history_id}")),
        ft.ElevatedButton("Exámenes Auxiliares", on_click=lambda e: page.go(f"/examenes-auxiliares/{history_id}")),
        ft.ElevatedButton("Tratamientos Realizados", on_click=lambda e: page.go(f"/tratamientos-realizados/{history_id}")),
        ft.ElevatedButton("Citas", on_click=lambda e: page.go(f"/citas/{history_id}")),
    ])

    # 📌 Layout principal
    return ft.Row([
        ft.Container(menu, width=250, padding=10, border=ft.Border.all(1)),
        ft.VerticalDivider(width=1),
        ft.Container(patient_info, expand=True, padding=20)
    ])
