import flet as ft  # Asegúrate de que esta línea esté al inicio del archivo
from controllers.historia_controller import HistoriaController

def history_management_view(page: ft.Page, menu_controller, dynamic_content: ft.Column):
    controller = HistoriaController()

    # Filtros para búsqueda
    start_date_input = ft.TextField(label="Desde (YYYY-MM-DD)", width=200)
    end_date_input = ft.TextField(label="Hasta (YYYY-MM-DD)", width=200)
    patient_name_input = ft.TextField(label="Nombres y Apellidos", width=250)

    # Tabla de historias clínicas
    histories_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Historia Clínica")),
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

    # Función para buscar historias clínicas con filtros
    def search_histories(e):
        start_date = start_date_input.value.strip() or None
        end_date = end_date_input.value.strip() or None
        patient_name = patient_name_input.value.strip() or None

        histories = controller.load_historias(start_date, end_date, patient_name)

        if not histories:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("No se encontraron historias clínicas"),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()

        histories_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(history[1]))),  # Mostrar history_number
                    ft.DataCell(ft.Text(history[2])),         # Paciente
                    ft.DataCell(ft.Text(str(history[3]))),      # Edad
                    ft.DataCell(ft.Text(history[4])),           # DNI
                    ft.DataCell(ft.Text(history[5])),           # Fecha Cita
                    ft.DataCell(ft.Text(history[6])),           # Hora Cita
                    ft.DataCell(ft.Text(history[7])),           # Estado
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar Historia",
                                on_click=lambda e, history_id=history[0]: menu_controller.show_history_detail_view(dynamic_content, history_id)
                            ),
                        ])
                    ),
                ]
            )
            for history in histories
        ]
        page.update()

    # Función para redirigir a la vista de creación de una nueva historia clínica
    def new_history(e):
        page.go("/new-history")

    # Layout principal
    return ft.Column([
        ft.Text("Gestión de Historias Clínicas", size=24, weight="bold"),
        ft.Row([
            start_date_input, 
            end_date_input, 
            patient_name_input, 
            ft.ElevatedButton("Buscar", on_click=search_histories),
            ft.ElevatedButton("Nuevo", on_click=new_history)
        ]),
        ft.Divider(),
        histories_table
    ])