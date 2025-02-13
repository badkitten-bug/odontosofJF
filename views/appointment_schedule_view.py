import flet as ft
from controllers.appointment_controller import AppointmentController
from datetime import datetime

def appointment_schedule_view(page: ft.Page):
    controller = AppointmentController()

    # Dropdown de doctores
    doctors = controller.load_doctors()
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=f"{doc[1]} - {doc[2]}") for doc in doctors],
        label="Seleccionar Doctor *",
        width=250
    )

    # DatePicker para la fecha de la cita
    def change_date(e):
        date_picker_text.value = e.control.value.strftime("%Y-%m-%d")
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2023, 1, 1),
        last_date=datetime(2025, 12, 31),
        on_change=change_date
    )
    page.overlay.append(date_picker)

    date_picker_text = ft.TextField(label="Fecha * (YYYY-MM-DD)", width=200, read_only=True)
    date_picker_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(date_picker)
    )

    # Tabla de horarios disponibles
    available_slots_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Reservar")),
        ],
        rows=[]
    )

    # Función para buscar horarios disponibles
    def search_available_slots(e):
        date = date_picker_text.value
        doctor_id = doctor_dropdown.value

        if not date or not doctor_id:
            page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar fecha y doctor"))
            page.snack_bar.open = True
            page.update()
            return

        available_slots = controller.load_available_slots(date, doctor_id)

        available_slots_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(slot[0])),
                    ft.DataCell(ft.Text("Disponible")),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.ADD,
                        tooltip="Reservar Cita",
                        on_click=lambda e, slot_time=slot[0]: open_booking_form(slot_time)
                    )),
                ]
            )
            for slot in available_slots
        ]
        page.update()

    # Formulario para reservar una cita
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in controller.load_patients()],
        label="Seleccionar Paciente *",
        width=250
    )
    notes_input = ft.TextField(label="Notas", multiline=True, width=300)
    selected_time = ft.TextField(label="Hora Seleccionada", width=200, read_only=True)

    def open_booking_form(slot_time):
        selected_time.value = slot_time
        page.update()

    # AlertDialog para confirmar la reserva
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Reserva"),
        content=ft.Text("¿Está seguro de que desea reservar esta cita?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: save_appointment(e)),
            ft.TextButton("No", on_click=lambda e: page.close(confirm_dialog)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def save_appointment(e):
        if not all([patient_dropdown.value, doctor_dropdown.value, date_picker_text.value, selected_time.value]):
            page.snack_bar = ft.SnackBar(ft.Text("Debe seleccionar paciente, doctor, fecha y hora."))
            page.snack_bar.open = True
            page.update()
            return

        duration = 30  # Duración predeterminada de 30 minutos
        data = (
            int(patient_dropdown.value),
            int(doctor_dropdown.value),
            date_picker_text.value,
            selected_time.value,
            duration,
            notes_input.value,
            1  # Estado predeterminado (por ejemplo, "Confirmada")
        )

        try:
            controller.create_appointment(data)
            page.snack_bar = ft.SnackBar(ft.Text(f"Cita agendada para {date_picker_text.value} a las {selected_time.value}"))
            page.snack_bar.open = True
            page.close(confirm_dialog)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al agendar la cita: {str(ex)}"))
            page.snack_bar.open = True
        page.update()

    def confirm_reservation(e):
        page.open(confirm_dialog)

    return ft.Column([
        ft.Text("Agendar Cita", size=24, weight="bold"),
        ft.Row([doctor_dropdown, date_picker_text, date_picker_button]),
        ft.ElevatedButton("Buscar Disponibilidad", on_click=search_available_slots),
        ft.Divider(),
        available_slots_table,
        ft.Divider(),
        ft.Text("Detalles de la Cita", size=20, weight="bold"),
        ft.Row([patient_dropdown, selected_time, notes_input]),
        ft.ElevatedButton("Reservar Cita", on_click=confirm_reservation),
    ])