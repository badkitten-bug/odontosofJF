import flet as ft
from database.db_config import connect_db

# hr.py
def hr_view(page: ft.Page):
    selected_hr_id = None

    def load_hr():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, role, phone, email, hire_date FROM hr")
            return cursor.fetchall()

    def add_hr(e):
        nonlocal selected_hr_id
        if not name_input.value or not role_input.value or not phone_input.value or not email_input.value or not hire_date_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_hr_id:
                cursor.execute(
                    "UPDATE hr SET name = ?, role = ?, phone = ?, email = ?, hire_date = ? WHERE id = ?",
                    (name_input.value, role_input.value, phone_input.value, email_input.value, hire_date_input.value, selected_hr_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO hr (name, role, phone, email, hire_date) VALUES (?, ?, ?, ?, ?)",
                    (name_input.value, role_input.value, phone_input.value, email_input.value, hire_date_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        hr_entries = load_hr()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),  # Name
                    ft.DataCell(ft.Text(entry[2])),  # Role
                    ft.DataCell(ft.Text(entry[3])),  # Phone
                    ft.DataCell(ft.Text(entry[4])),  # Email
                    ft.DataCell(ft.Text(entry[5])),  # Hire Date
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_hr_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_hr(id)
                    )),
                ]
            )
            for entry in hr_entries
        ]
        page.update()

    def load_hr_to_edit(hr_id):
        nonlocal selected_hr_id
        selected_hr_id = hr_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hr WHERE id = ?", (hr_id,))
            hr_entry = cursor.fetchone()
        if hr_entry:
            name_input.value = hr_entry[1]
            role_input.value = hr_entry[2]
            phone_input.value = hr_entry[3]
            email_input.value = hr_entry[4]
            hire_date_input.value = hr_entry[5]
            page.update()

    def delete_hr(hr_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hr WHERE id = ?", (hr_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_hr_id
        selected_hr_id = None
        name_input.value = ""
        role_input.value = ""
        phone_input.value = ""
        email_input.value = ""
        hire_date_input.value = ""
        page.update()

    name_input = ft.TextField(label="Name")
    role_input = ft.TextField(label="Role")
    phone_input = ft.TextField(label="Phone")
    email_input = ft.TextField(label="Email")
    hire_date_input = ft.TextField(label="Hire Date (YYYY-MM-DD)")
    add_button = ft.ElevatedButton("Save", on_click=add_hr)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Role")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Hire Date")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("HR Management", size=24, weight="bold"),
        ft.Row([name_input, role_input, phone_input, email_input, hire_date_input, add_button, clear_button]),
        table,
    ])
