import flet as ft
from controllers.appointment_controller import AppointmentController

def appointments_view(page: ft.Page):
    controller = AppointmentController()
    selected_appointment_id = None

    # Cargar datos para los dropdowns
    patients = controller.load_patients()
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
        label="Seleccionar Paciente"
    )
    doctors = controller.load_doctors()
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=f"{doc[1]} - {doc[2]}") for doc in doctors],
        label="Seleccionar Doctor"
    )

    date_picker = ft.TextField(label="Fecha (YYYY-MM-DD)")
    time_picker = ft.TextField(label="Hora (HH:MM)")
    duration_input = ft.TextField(label="Duración (minutos)", keyboard_type=ft.KeyboardType.NUMBER)
    notes_input = ft.TextField(label="Notas", multiline=True)
    status_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Pending"), ft.dropdown.Option("Completed"), ft.dropdown.Option("Cancelled")],
        label="Estado",
        value="Pending"
    )
    save_button = ft.ElevatedButton("Guardar", on_click=lambda e: save_appointment(e))
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda e: clear_inputs())

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

    def refresh_table(date=None, doctor_id=None, status=None):
        appointments = controller.load_appointments(date, doctor_id, status)
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
                        icon=ft.icons.EDIT,
                        on_click=lambda e, id=appt[0]: load_appointment_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, id=appt[0]: delete_appointment(id)
                    )),
                ]
            )
            for appt in appointments
        ]
        page.update()

    def load_appointment_to_edit(appointment_id):
        nonlocal selected_appointment_id
        selected_appointment_id = appointment_id
        appointment = controller.get_appointment_by_id(appointment_id)
        if appointment:
            patient_dropdown.value = str(appointment[0])
            doctor_dropdown.value = str(appointment[1])
            date_picker.value = appointment[2]
            time_picker.value = appointment[3]
            duration_input.value = str(appointment[4])
            notes_input.value = appointment[5]
            status_dropdown.value = appointment[6]
            page.update()

    def delete_appointment(appointment_id):
        controller.delete_appointment(appointment_id)
        refresh_table()

    def save_appointment(e):
        nonlocal selected_appointment_id
        try:
            if not patient_dropdown.value or not doctor_dropdown.value:
                raise ValueError("Seleccione un paciente y un doctor.")
            if not date_picker.value or not time_picker.value or not duration_input.value:
                raise ValueError("Complete la fecha, hora y duración.")

            data = (
                int(patient_dropdown.value),
                int(doctor_dropdown.value),
                date_picker.value,
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

    def clear_inputs():
        nonlocal selected_appointment_id
        selected_appointment_id = None
        patient_dropdown.value = None
        doctor_dropdown.value = None
        date_picker.value = ""
        time_picker.value = ""
        duration_input.value = ""
        notes_input.value = ""
        status_dropdown.value = "Pending"
        page.update()

    refresh_table()

    return ft.Column([
        ft.Text("Gestión de Citas", size=24, weight="bold"),
        ft.Row([
            patient_dropdown,
            doctor_dropdown,
            date_picker,
            time_picker,
            duration_input,
            notes_input,
            status_dropdown,
            save_button,
            clear_button
        ]),
        table,
    ])
