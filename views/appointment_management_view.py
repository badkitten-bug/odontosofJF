import flet as ft
from controllers.appointment_controller import AppointmentController
from views.edit_appointment_view import edit_appointment_view
from datetime import datetime

def appointment_management_view(page: ft.Page):
    controller = AppointmentController()

    # Filtros para búsqueda
    doctors = controller.load_doctors()
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=f"{doc[1]} - {doc[2]}") for doc in doctors],
        label="Filtrar por Doctor",
        width=250
    )

    statuses = controller.load_appointment_statuses()
    status_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(st[0]), text=st[1]) for st in statuses],
        label="Estado",
        width=200
    )

    # DatePicker para filtrar por fecha
    def change_date(e):
        date_picker_text.value = e.control.value.strftime("%Y-%m-%d")
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2023, 1, 1),
        last_date=datetime(2025, 12, 31),
        on_change=change_date
    )
    page.overlay.append(date_picker)

    date_picker_text = ft.TextField(label="Filtrar por Fecha", width=200, read_only=True)
    date_picker_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(date_picker)  # Corregido: Usar page.open()
    )

    # Tabla de citas agendadas
    appointments_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Inicio")),
            ft.DataColumn(ft.Text("Fin")),
            ft.DataColumn(ft.Text("Notas")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Eliminar")),
        ],
        rows=[]
    )
    
    # Función para mostrar confirmaciones
    def show_confirmation(message):
        page.snack_bar = ft.SnackBar(content=ft.Text(message))
        page.snack_bar.open = True
        page.update()

   
    # Refrescar tabla de citas
    def refresh_table(e=None):
        appointments = controller.load_appointments()
        appointments_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(appt[0]))),
                    ft.DataCell(ft.Text(appt[1])),  # Paciente
                    ft.DataCell(ft.Text(appt[2])),  # Doctor
                    ft.DataCell(ft.Text(appt[3])),  # Fecha
                    ft.DataCell(ft.Text(appt[4])),  # Inicio
                    ft.DataCell(ft.Text(appt[5])),  # Fin
                    ft.DataCell(ft.Text(appt[6])),  # Notas
                    ft.DataCell(ft.Text(str(appt[7]))),  # Estado
                    ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=appt[0]: edit_appointment(id))),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=appt[0]: delete_appointment(id))),
                ]
            )
            for appt in appointments
        ]
        page.update()


    # Función para eliminar una cita
    def delete_appointment(appointment_id):
        controller.delete_appointment(appointment_id)
        show_confirmation("Cita eliminada correctamente")
        refresh_table()

    #  Función para editar una cita
    def edit_appointment(appointment_id):
        print(f"🔍 Se ha llamado a edit_appointment() con ID: {appointment_id}")  # Debug
        edit_appointment_view(page, appointment_id, refresh_table)

    # Cargar la tabla al iniciar
    refresh_table()

    return ft.Column([
        ft.Text("Gestión de Citas", size=24, weight="bold"),
        ft.Row([doctor_dropdown, date_picker_text, date_picker_button, status_dropdown, ft.ElevatedButton("Filtrar", on_click=refresh_table)]),
        ft.Divider(),
        appointments_table
    ])