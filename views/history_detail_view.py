import flet as ft
from controllers.historia_controller import HistoriaController

def history_detail_view(page: ft.Page, dynamic_content: ft.Column, menu_controller, history_id: int):
    controller = HistoriaController()
    histories = controller.get_history_by_id(history_id)
    
    if not histories:
        page.snack_bar = ft.SnackBar(ft.Text("⚠️ Error: No se pudo cargar la historia clínica.", color="red"))
        page.snack_bar.open = True
        page.update()
        return

    history = histories[0]

    patient_info = ft.Column([
        ft.Text(f"Nombre: {history[5]} {history[6]}"),
        ft.Text(f"Edad: {history[7]}"),
        ft.Text(f"DNI: {history[8]}"),
        ft.Text(f"Fecha de la Cita: {history[10]}"),
        ft.Text(f"Hora de la Cita: {history[11]}"),
        ft.Text(f"Estado: {history[13]}"),
    ])

    menu = ft.Column([
        ft.Text("📂 Datos del Paciente", size=18, weight="bold"),
        ft.ElevatedButton("Exploración Física", on_click=lambda e: menu_controller.show_exploracion_fisica_view(dynamic_content, history_id)),
        ft.ElevatedButton("Odontograma", on_click=lambda e: menu_controller.show_odontograma_view(dynamic_content, history_id)),
        ft.ElevatedButton("Diagnóstico", on_click=lambda e: menu_controller.show_diagnostico_view(dynamic_content, history_id)),
        ft.ElevatedButton("Exámenes Auxiliares", on_click=lambda e: page.go(f"/examenes-auxiliares/{history_id}")),
        ft.ElevatedButton("Tratamientos", on_click=lambda e: menu_controller.show_treatments_view(dynamic_content, history_id)),
        ft.ElevatedButton("Citas", on_click=lambda e: menu_controller.show_citas_view(dynamic_content, history_id)),
    ])

    """ft.ElevatedButton("Evolución", on_click=lambda e: page.go(f"/evolucion/{history_id}")),""" 
    """ falta agregar la vista de evolución """

    return ft.Row([
        ft.Container(
            menu,
            width=250,
            padding=10,
            border=ft.Border(
                left=ft.BorderSide(1, ft.Colors.BLACK),
                top=ft.BorderSide(1, ft.Colors.BLACK),
                right=ft.BorderSide(1, ft.Colors.BLACK),
                bottom=ft.BorderSide(1, ft.Colors.BLACK)
            )
        ),
        ft.VerticalDivider(width=1),
        ft.Container(patient_info, expand=True, padding=20)
    ])
