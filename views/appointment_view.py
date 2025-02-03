import flet as ft
from controllers.appointment_controller import AppointmentController
from datetime import datetime

def appointments_view(page: ft.Page):
    controller = AppointmentController()
    selected_appointment_id = None

    # Obtener especialidades, pacientes y doctores desde la base de datos
    specialties = controller.load_specialties()
    patients = controller.load_patients()
    doctors = controller.load_doctors()

    # Dropdown de pacientes
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
        label="Seleccionar Paciente *",
        width=250
    )

    # Dropdown de doctores
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=f"{doc[1]} - {doc[2]}") for doc in doctors],
        label="Seleccionar Doctor *",
        width=250
    )
    # Dropdown de especialidades
    specialties = [sp for sp in controller.load_specialties() if sp[2].lower() == "activo"]

    specialty_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(sp[0], text=sp[1]) for sp in specialties],
        label="Filtrar por Especialidad",
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

    # Campos de entrada adicionales
    time_picker = ft.TextField(label="Hora * (HH:MM)", width=150)
    duration_input = ft.TextField(label="Duración (min)", keyboard_type=ft.KeyboardType.NUMBER, width=150)
    notes_input = ft.TextField(label="Notas", multiline=True, width=300)
    # Dropdown de estado
    status_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Pending"),
            ft.dropdown.Option("Completed"),
            ft.dropdown.Option("Cancelled")
        ],
        label="Estado *",
        value="Pending",
        width=200
    )

    # Tabla de citas
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Duración")),
            ft.DataColumn(ft.Text("Notas")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Eliminar")),
        ],
        rows=[]
    )

    # Cargar y actualizar la tabla
    def refresh_table(date=None, doctor_id=None, specialty_id=None, status=None):
        appointments = controller.load_appointments(date, doctor_id, specialty_id, status)
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(appt[0]))),
                    ft.DataCell(ft.Text(appt[1])),
                    ft.DataCell(ft.Text(appt[2])),
                    ft.DataCell(ft.Text(appt[3])),
                    ft.DataCell(ft.Text(appt[4])),
                    ft.DataCell(ft.Text(str(appt[5]))),
                    ft.DataCell(ft.Text(appt[6])),
                    ft.DataCell(ft.Text(appt[7])),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=appt[0]: load_appointment_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=appt[0]: delete_appointment(id)
                    )),
                ]
            )
            for appt in appointments
        ]
        page.update()

    # Cargar datos en el formulario para edición
    def load_appointment_to_edit(appointment_id):
        nonlocal selected_appointment_id
        selected_appointment_id = appointment_id
        appointment = controller.get_appointment_by_id(appointment_id)
        if appointment:
            patient_dropdown.value = str(appointment[1])
            doctor_dropdown.value = str(appointment[2])
            date_picker_text.value = appointment[3]
            time_picker.value = appointment[4]
            duration_input.value = str(appointment[5])
            notes_input.value = appointment[6]
            status_dropdown.value = appointment[7]
            page.update()

    # Eliminar una cita
    def delete_appointment(appointment_id):
        controller.delete_appointment(appointment_id)
        refresh_table()

    # Guardar una nueva cita o actualizar una existente
    def save_appointment(e):
        nonlocal selected_appointment_id
        try:
            if not all([patient_dropdown.value, doctor_dropdown.value, date_picker_text.value, time_picker.value, duration_input.value]):
                raise ValueError("Todos los campos obligatorios deben estar completos.")

            data = (
                int(patient_dropdown.value),
                int(doctor_dropdown.value),
                date_picker_text.value,
                time_picker.value,
                int(duration_input.value),
                notes_input.value,
                status_dropdown.value
            )
            controller.save_appointment(selected_appointment_id, data)
            clear_inputs()
            refresh_table()
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    # Limpiar campos del formulario
    def clear_inputs():
        nonlocal selected_appointment_id
        selected_appointment_id = None
        patient_dropdown.value = None
        doctor_dropdown.value = None
        date_picker_text.value = ""
        time_picker.value = ""
        duration_input.value = ""
        notes_input.value = ""
        status_dropdown.value = "Pending"
        page.update()

    refresh_table()

    return ft.Column([
        ft.Text("Gestión de Citas", size=24, weight="bold"),
        ft.Row([patient_dropdown, doctor_dropdown, specialty_dropdown], wrap=True),
        ft.Row([date_picker_text, date_picker_button, time_picker, duration_input, notes_input, status_dropdown], wrap=True),
        ft.Row([ft.ElevatedButton("Guardar", on_click=save_appointment), ft.ElevatedButton("Limpiar", on_click=clear_inputs)]),
        ft.Divider(),
        table
    ])
