import flet as ft
from database.db_config import connect_db

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
                    ft.DataCell(ft.Text(str(doc[0]))),
                    ft.DataCell(ft.Text(doc[1])),
                    ft.DataCell(ft.Text(doc[2])),
                    ft.DataCell(ft.Text(doc[3])),
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
        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_doctor_id:
                cursor.execute(
                    "UPDATE doctors SET name = ?, specialty = ?, phone = ? WHERE id = ?",
                    (name_input.value, specialty_input.value, phone_input.value, selected_doctor_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO doctors (name, specialty, phone) VALUES (?, ?, ?)",
                    (name_input.value, specialty_input.value, phone_input.value)
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
        page.update()

    name_input = ft.TextField(label="Doctor Name")
    specialty_input = ft.TextField(label="Specialty")
    phone_input = ft.TextField(label="Phone")
    add_button = ft.ElevatedButton("Save", on_click=add_doctor)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Specialty")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column(
        [
            ft.Text("Doctors Management", size=24, weight="bold"),
            ft.Row([name_input, specialty_input, phone_input, add_button, clear_button]),
            table,
        ]
    )
