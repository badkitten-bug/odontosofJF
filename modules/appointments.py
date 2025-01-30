import flet as ft
from database.db_config import connect_db

def appointments_view(page: ft.Page, only_form=False, only_table=False):
    selected_appointment_id = None

    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, history_number FROM patients WHERE is_deleted = 0")
            return cursor.fetchall()

    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM doctors")
            return cursor.fetchall()

    def load_appointments():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT appointments.id, patients.name, doctors.name, appointments.date, appointments.time, appointments.notes, appointments.status
                FROM appointments
                JOIN patients ON appointments.patient_id = patients.id
                JOIN doctors ON appointments.doctor_id = doctors.id
                WHERE appointments.is_deleted = 0
            ''')
            return cursor.fetchall()

    def refresh_table(table):
        appointments = load_appointments()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(appt[0]))),
                    ft.DataCell(ft.Text(appt[1])),  # Patient name
                    ft.DataCell(ft.Text(appt[2])),  # Doctor name
                    ft.DataCell(ft.Text(appt[3])),  # Date
                    ft.DataCell(ft.Text(appt[4])),  # Time
                    ft.DataCell(ft.Text(appt[5])),  # Notes
                    ft.DataCell(ft.Text(appt[6])),  # Status
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=appt[0]: load_appointment_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=appt[0]: delete_appointment(id, table)
                    )),
                ]
            )
            for appt in appointments
        ]
        page.update()

    def add_appointment(e, table):
        if not patient_dropdown.value or not doctor_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("Patient and Doctor are required."))
            page.snack_bar.open = True
            return

        if not date_picker.value or not time_picker.value:
            page.snack_bar = ft.SnackBar(ft.Text("Date and Time are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_appointment_id:
                cursor.execute(
                    "UPDATE appointments SET patient_id = ?, doctor_id = ?, date = ?, time = ?, notes = ?, status = ? WHERE id = ?",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_picker.value, time_picker.value, notes_input.value, status_dropdown.value, selected_appointment_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO appointments (patient_id, doctor_id, date, time, notes, status, is_deleted) VALUES (?, ?, ?, ?, ?, ?, 0)",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_picker.value, time_picker.value, notes_input.value, status_dropdown.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table(table)

    def load_appointment_to_edit(appointment_id):
        nonlocal selected_appointment_id
        selected_appointment_id = appointment_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
            appointment = cursor.fetchone()
        if appointment:
            patient_dropdown.value = str(appointment[1])
            doctor_dropdown.value = str(appointment[2])
            date_picker.value = appointment[3]
            time_picker.value = appointment[4]
            notes_input.value = appointment[5]
            status_dropdown.value = appointment[6]
            page.update()

    def delete_appointment(appointment_id, table):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET is_deleted = 1 WHERE id = ?", (appointment_id,))
            conn.commit()
        refresh_table(table)

    def clear_inputs():
        nonlocal selected_appointment_id
        selected_appointment_id = None
        patient_dropdown.value = None
        doctor_dropdown.value = None
        date_picker.value = ""
        time_picker.value = ""
        notes_input.value = ""
        status_dropdown.value = "Pending"
        page.update()

    # Inputs
    if not only_table:
        patients = load_patients()
        patient_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
            label="Select a Patient"
        )
        doctors = load_doctors()
        doctor_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(str(doc[0]), text=doc[1]) for doc in doctors],
            label="Select a Doctor"
        )
        date_picker = ft.TextField(label="Date (YYYY-MM-DD)")
        time_picker = ft.TextField(label="Time (HH:MM)")
        notes_input = ft.TextField(label="Notes")
        status_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option("Pending"), ft.dropdown.Option("Completed"), ft.dropdown.Option("Cancelled")],
            label="Status"
        )
        add_button = ft.ElevatedButton("Save", on_click=lambda _: add_appointment(_, table))
        clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    # Tabla
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Notes")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table(table)

    if only_form:
        return ft.Column(
            [
                ft.Text("Register Appointment", size=24, weight="bold"),
                patient_dropdown,
                doctor_dropdown,
                date_picker,
                time_picker,
                notes_input,
                status_dropdown,
                add_button,
                clear_button,
            ]
        )
    elif only_table:
        return ft.Column(
            [
                ft.Text("Scheduled Appointments", size=24, weight="bold"),
                table,
            ]
        )
