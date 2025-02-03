import flet as ft
from database.db_config import connect_db
from datetime import datetime, timedelta

def appointments_view(page: ft.Page):
    selected_appointment_id = None  # Para almacenar el ID de la cita seleccionada para edición

    # Cargar pacientes desde la base de datos
    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, history_number FROM patients WHERE is_deleted = 0")
            return cursor.fetchall()

    # Cargar doctores desde la base de datos
    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, specialty FROM doctors")
            return cursor.fetchall()

    # Cargar citas desde la base de datos
    def load_appointments(date=None, doctor_id=None, status=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT appointments.id, patients.name, doctors.name, appointments.date, appointments.time, 
                       appointments.duration, appointments.notes, appointments.status
                FROM appointments
                JOIN patients ON appointments.patient_id = patients.id
                JOIN doctors ON appointments.doctor_id = doctors.id
                WHERE appointments.is_deleted = 0
            '''
            params = []
            if date:
                query += " AND appointments.date = ?"
                params.append(date)
            if doctor_id:
                query += " AND appointments.doctor_id = ?"
                params.append(doctor_id)
            if status:
                query += " AND appointments.status = ?"
                params.append(status)
            cursor.execute(query, params)
            return cursor.fetchall()

    # Actualizar la tabla de citas
    def refresh_table(date=None, doctor_id=None, status=None):
        appointments = load_appointments(date, doctor_id, status)
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(appt[0]))),  # ID
                    ft.DataCell(ft.Text(appt[1])),  # Nombre del paciente
                    ft.DataCell(ft.Text(appt[2])),  # Nombre del doctor
                    ft.DataCell(ft.Text(appt[3])),  # Fecha
                    ft.DataCell(ft.Text(appt[4])),  # Hora
                    ft.DataCell(ft.Text(str(appt[5]))),  # Duración
                    ft.DataCell(ft.Text(appt[6])),  # Notas
                    ft.DataCell(ft.Text(appt[7])),  # Estado
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

    # Cargar una cita para editar
    def load_appointment_to_edit(appointment_id):
        nonlocal selected_appointment_id
        selected_appointment_id = appointment_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT patient_id, doctor_id, date, time, duration, notes, status FROM appointments WHERE id = ?", (appointment_id,))
            appointment = cursor.fetchone()
            if appointment:
                patient_dropdown.value = str(appointment[0])
                doctor_dropdown.value = str(appointment[1])
                date_picker.value = appointment[2]
                time_picker.value = appointment[3]
                duration_input.value = str(appointment[4])
                notes_input.value = appointment[5]
                status_dropdown.value = appointment[6]
                page.update()

    # Eliminar una cita (borrado lógico)
    def delete_appointment(appointment_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET is_deleted = 1 WHERE id = ?", (appointment_id,))
            conn.commit()
        refresh_table()

    # Guardar o actualizar una cita
    def save_appointment(e):
        try:
            if not patient_dropdown.value or not doctor_dropdown.value:
                raise ValueError("Seleccione un paciente y un doctor.")
            if not date_picker.value or not time_picker.value or not duration_input.value:
                raise ValueError("Complete la fecha, hora y duración.")

            with connect_db() as conn:
                cursor = conn.cursor()
                if selected_appointment_id:
                    cursor.execute(
                        "UPDATE appointments SET patient_id = ?, doctor_id = ?, date = ?, time = ?, duration = ?, notes = ?, status = ? WHERE id = ?",
                        (int(patient_dropdown.value), int(doctor_dropdown.value), date_picker.value, time_picker.value, int(duration_input.value), notes_input.value, status_dropdown.value, selected_appointment_id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO appointments (patient_id, doctor_id, date, time, duration, notes, status, is_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                        (int(patient_dropdown.value), int(doctor_dropdown.value), date_picker.value, time_picker.value, int(duration_input.value), notes_input.value, status_dropdown.value)
                    )
                conn.commit()
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

    # Limpiar los campos del formulario
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

    # Controles del formulario
    patients = load_patients()
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
        label="Seleccionar Paciente"
    )
    doctors = load_doctors()
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
    save_button = ft.ElevatedButton("Guardar", on_click=save_appointment)
    clear_button = ft.ElevatedButton("Limpiar", on_click=clear_inputs)

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

    # Cargar datos iniciales
    refresh_table()

    # Retornar la vista
    return ft.Column([
        ft.Text("Gestión de Citas", size=24, weight="bold"),
        ft.Row([patient_dropdown, doctor_dropdown, date_picker, time_picker, duration_input, notes_input, status_dropdown, save_button, clear_button]),
        table,
    ])