import flet as ft
from controllers.appointment_controller import AppointmentController
from datetime import datetime, timedelta

def appointment_schedule_view(page: ft.Page):
    controller = AppointmentController()

    # Dropdown de especialidades
    specialties = controller.load_specialties()
    specialty_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(spec[0]), text=spec[1]) for spec in specialties],
        label="Seleccionar Especialidad *",
        width=250,
        on_change=lambda e: update_doctors_dropdown(e)  # Actualizar doctores al cambiar especialidad
    )

    # Dropdown de doctores (se actualiza al seleccionar una especialidad)
    doctors_dropdown = ft.Dropdown(
        label="Seleccionar Doctor *",
        width=250,
        disabled=True  # Inicialmente deshabilitado hasta que se seleccione una especialidad
    )

    def update_doctors_dropdown(e):
        specialty_id = specialty_dropdown.value
        if not specialty_id:
            return
        doctors = controller.load_doctors_by_specialty(specialty_id)
        doctors_dropdown.options = [ft.dropdown.Option(str(doc[0]), text=f"{doc[1]} {doc[2]}") for doc in doctors]
        doctors_dropdown.disabled = False
        page.update()

    # DatePicker para la fecha de la cita
    def change_date(e):
        selected_date = e.control.value
        # Si selected_date es datetime, lo comparamos con la fecha actual
        if selected_date.date() < datetime.now().date():
            page.snack_bar = ft.SnackBar(
                content=ft.Text("La fecha no puede ser en el pasado"),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return
        date_picker_text.value = selected_date.strftime("%Y-%m-%d")
        page.update()

    # Usar objetos datetime para first_date y last_date
    first_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    last_date = first_date + timedelta(days=365)
    date_picker = ft.DatePicker(
        first_date=first_date,
        last_date=last_date,
        on_change=change_date
    )
    # NOTA: No se utiliza page.overlay.append(date_picker)

    date_picker_text = ft.TextField(label="Fecha * (YYYY-MM-DD)", width=200, read_only=True)
    date_picker_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(date_picker)  # Se abre el DatePicker con page.open()
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

    def search_available_slots(e):
        date = date_picker_text.value
        doctor_id = doctors_dropdown.value

        if not date or not doctor_id:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Debe seleccionar fecha y doctor"),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return

        # Convertir la fecha a objeto datetime y obtener el día de la semana (0 = lunes, 6 = domingo)
        selected_date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = selected_date_obj.weekday() + 1  # Ajustar para coincidir con tu tabla

        # Obtener el horario del doctor para ese día
        doctor_schedule = controller.get_doctor_schedule(doctor_id, day_of_week)
        if not doctor_schedule:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("El doctor no trabaja ese día"),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return

        start_time = doctor_schedule['start_time']
        end_time = doctor_schedule['end_time']

        booked_slots = controller.get_booked_slots(doctor_id, date)

        available_slots = []
        current_time = start_time
        while current_time < end_time:
            slot_end_time = (datetime.combine(selected_date_obj, current_time) + timedelta(minutes=30)).time()
            if not any(booked['start_time'] <= current_time < booked['end_time'] for booked in booked_slots):
                available_slots.append((current_time.strftime("%H:%M"), slot_end_time.strftime("%H:%M")))
            current_time = (datetime.combine(selected_date_obj, current_time) + timedelta(minutes=30)).time()

        if not available_slots:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("No hay horarios disponibles para la fecha seleccionada"),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return

        available_slots_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{slot[0]} - {slot[1]}")),
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
        if not all([patient_dropdown.value, doctors_dropdown.value, date_picker_text.value, selected_time.value]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Debe seleccionar paciente, doctor, fecha y hora."),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return

        duration = 30
        data = (
            int(patient_dropdown.value),
            int(doctors_dropdown.value),
            date_picker_text.value,
            selected_time.value,
            duration,
            notes_input.value,
            1
        )

        try:
            controller.create_appointment(data)
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Cita agendada para {date_picker_text.value} a las {selected_time.value}"),
                duration=4000
            )
            page.snack_bar.open = True
            page.close(confirm_dialog)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error al agendar la cita: {str(ex)}"),
                duration=4000
            )
            page.snack_bar.open = True
        page.update()

    def confirm_reservation(e):
        if not all([patient_dropdown.value, doctors_dropdown.value, date_picker_text.value, selected_time.value]):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Debe seleccionar paciente, doctor, fecha y hora."),
                duration=4000
            )
            page.snack_bar.open = True
            page.update()
            return

        doctor_name = next((doc[1] for doc in controller.load_doctors() if str(doc[0]) == doctors_dropdown.value), "Desconocido")
        patient_name = next((pt[1] for pt in controller.load_patients() if str(pt[0]) == patient_dropdown.value), "Desconocido")

        confirm_dialog.content = ft.Column([
            ft.Text(f"Doctor: {doctor_name}"),
            ft.Text(f"Paciente: {patient_name}"),
            ft.Text(f"Fecha: {date_picker_text.value}"),
            ft.Text(f"Hora: {selected_time.value}"),
        ])
        page.open(confirm_dialog)

    return ft.Column([
        ft.Text("Agendar Cita", size=24, weight="bold"),
        ft.Row([specialty_dropdown, doctors_dropdown]),
        ft.Row([date_picker_text, date_picker_button]),
        ft.ElevatedButton("Buscar Disponibilidad", on_click=search_available_slots),
        ft.Divider(),
        available_slots_table,
        ft.Divider(),
        ft.Text("Detalles de la Cita", size=20, weight="bold"),
        ft.Row([patient_dropdown, selected_time, notes_input]),
        ft.ElevatedButton("Reservar Cita", on_click=confirm_reservation),
    ])
