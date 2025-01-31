import flet as ft
from database.db_config import connect_db

# doctors.py
def doctors_view(page: ft.Page):
    selected_doctor_id = None

    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctors")
            return cursor.fetchall()

    def refresh_table():
        doctors = load_doctors()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(doc[0]))),  # ID
                    ft.DataCell(ft.Text(doc[1])),      # Name
                    ft.DataCell(ft.Text(doc[2])),      # Specialty
                    ft.DataCell(ft.Text(doc[3])),      # Phone
                    ft.DataCell(ft.Text(doc[4])),      # Email
                    ft.DataCell(ft.Text(doc[5])),      # Schedule
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=doc[0]: load_doctor_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=doc[0]: delete_doctor(id)
                    )),
                ]
            )
            for doc in doctors
        ]
        page.update()

    def add_doctor(e):
        nonlocal selected_doctor_id
        if not all([name_input.value, specialty_input.value, phone_input.value, email_input.value, schedule_input.value]):
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_doctor_id:
                cursor.execute(
                    "UPDATE doctors SET name = ?, specialty = ?, phone = ?, email = ?, schedule = ? WHERE id = ?",
                    (
                        name_input.value, specialty_input.value, phone_input.value, email_input.value, schedule_input.value, selected_doctor_id
                    )
                )
            else:
                cursor.execute(
                    "INSERT INTO doctors (name, specialty, phone, email, schedule) VALUES (?, ?, ?, ?, ?)",
                    (
                        name_input.value, specialty_input.value, phone_input.value, email_input.value, schedule_input.value
                    )
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def load_doctor_to_edit(doctor_id):
        nonlocal selected_doctor_id
        selected_doctor_id = doctor_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
            doctor = cursor.fetchone()
        if doctor:
            name_input.value = doctor[1]
            specialty_input.value = doctor[2]
            phone_input.value = doctor[3]
            email_input.value = doctor[4]
            schedule_input.value = doctor[5]
            page.update()

    def delete_doctor(doctor_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_doctor_id
        selected_doctor_id = None
        name_input.value = ""
        specialty_input.value = ""
        phone_input.value = ""
        email_input.value = ""
        schedule_input.value = ""
        page.update()

    # Inputs
    name_input = ft.TextField(label="Doctor Name")
    specialty_input = ft.TextField(label="Specialty")
    phone_input = ft.TextField(label="Phone")
    email_input = ft.TextField(label="Email")
    schedule_input = ft.TextField(label="Schedule")
    add_button = ft.ElevatedButton("Save", on_click=add_doctor)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    # Tabla
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Specialty")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Schedule")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Doctors Management", size=24, weight="bold"),
        ft.Row([name_input, specialty_input, phone_input, email_input, schedule_input, add_button, clear_button]),
        table,
    ])
