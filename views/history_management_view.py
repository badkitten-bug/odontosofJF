import flet as ft
from controllers.historia_controller import HistoriaController
from datetime import datetime

def history_management_view(page: ft.Page):
    controller = HistoriaController()

    # Filtros para búsqueda
    start_date_input = ft.TextField(label="Desde (YYYY-MM-DD)", width=200)
    end_date_input = ft.TextField(label="Hasta (YYYY-MM-DD)", width=200)
    patient_name_input = ft.TextField(label="Nombres y Apellidos", width=250)

    # Tabla de historias clínicas
    histories_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Fecha Cita")),
            ft.DataColumn(ft.Text("Hora Cita")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    # Función para buscar historias clínicas
    def search_histories(e):
        start_date = start_date_input.value
        end_date = end_date_input.value
        patient_name = patient_name_input.value

        histories = controller.load_histories(start_date, end_date, patient_name)
        histories_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(history[0]))),  # ID
                    ft.DataCell(ft.Text(history[1])),  # Paciente
                    ft.DataCell(ft.Text(str(history[2]))),  # Edad
                    ft.DataCell(ft.Text(history[3])),  # DNI
                    ft.DataCell(ft.Text(history[4])),  # Fecha Cita
                    ft.DataCell(ft.Text(history[5])),  # Hora Cita
                    ft.DataCell(ft.Text(history[6])),  # Estado
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        tooltip="Editar Historia",
                        on_click=lambda e, id=history[0]: edit_history(id)
                    )),
                ]
            )
            for history in histories
        ]
        page.update()

    # Función para editar una historia clínica
    def edit_history(history_id):
        page.go(f"/history-detail/{history_id}")

    return ft.Column([
        ft.Text("Gestión de Historias Clínicas", size=24, weight="bold"),
        ft.Row([start_date_input, end_date_input, patient_name_input, ft.ElevatedButton("Buscar", on_click=search_histories)]),
        ft.Divider(),
        histories_table
    ])