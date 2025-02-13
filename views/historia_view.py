import flet as ft
from controllers.historia_controller import HistoriaController

def historia_view(page: ft.Page):
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

        histories = controller.load_historias(start_date, end_date, patient_name)
        histories_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(history[0]))) for history in histories
                ]
            )
        ]
        page.update()

    return ft.Column([
        ft.Text("Gestión de Historias Clínicas", size=24, weight="bold"),
        ft.Row([start_date_input, end_date_input, patient_name_input, ft.ElevatedButton("Buscar", on_click=search_histories)]),
        ft.Divider(),
        histories_table
    ])