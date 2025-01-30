import flet as ft
from database.db_config import connect_db

# doctor_schedules.py
def doctor_schedules_view(page: ft.Page):
    selected_schedule_id = None

    def load_schedules():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, doctor_id, day_of_week, start_time, end_time FROM doctor_schedules")
            return cursor.fetchall()

    def refresh_table():
        schedules = load_schedules()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(sch[0]))),  # ID
                    ft.DataCell(ft.Text(str(sch[1]))),  # Doctor ID
                    ft.DataCell(ft.Text(sch[2])),  # Day
                    ft.DataCell(ft.Text(sch[3])),  # Start Time
                    ft.DataCell(ft.Text(sch[4])),  # End Time
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=sch[0]: load_schedule_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=sch[0]: delete_schedule(id)
                    )),
                ]
            )
            for sch in schedules
        ]
        page.update()

    def add_schedule(e):
        nonlocal selected_schedule_id
        if not doctor_dropdown.value or not day_dropdown.value or not start_time_input.value or not end_time_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_schedule_id:
                cursor.execute(
                    "UPDATE doctor_schedules SET doctor_id = ?, day_of_week = ?, start_time = ?, end_time = ? WHERE id = ?",
                    (int(doctor_dropdown.value), day_dropdown.value, start_time_input.value, end_time_input.value, selected_schedule_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO doctor_schedules (doctor_id, day_of_week, start_time, end_time) VALUES (?, ?, ?, ?)",
                    (int(doctor_dropdown.value), day_dropdown.value, start_time_input.value, end_time_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def load_schedule_to_edit(schedule_id):
        nonlocal selected_schedule_id
        selected_schedule_id = schedule_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctor_schedules WHERE id = ?", (schedule_id,))
            schedule = cursor.fetchone()
        if schedule:
            doctor_dropdown.value = str(schedule[1])
            day_dropdown.value = schedule[2]
            start_time_input.value = schedule[3]
            end_time_input.value = schedule[4]
            page.update()

    def delete_schedule(schedule_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctor_schedules WHERE id = ?", (schedule_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_schedule_id
        selected_schedule_id = None
        doctor_dropdown.value = None
        day_dropdown.value = None
        start_time_input.value = ""
        end_time_input.value = ""
        page.update()

    doctors = [(str(doc[0]), doc[1]) for doc in load_schedules()]
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(did, text=name) for did, name in doctors],
        label="Select a Doctor"
    )
    day_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(day) for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]],
        label="Day of the Week"
    )
    start_time_input = ft.TextField(label="Start Time (HH:MM)")
    end_time_input = ft.TextField(label="End Time (HH:MM)")
    add_button = ft.ElevatedButton("Save", on_click=add_schedule)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Doctor ID")),
            ft.DataColumn(ft.Text("Day")),
            ft.DataColumn(ft.Text("Start Time")),
            ft.DataColumn(ft.Text("End Time")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Doctor Schedules", size=24, weight="bold"),
        ft.Row([doctor_dropdown, day_dropdown, start_time_input, end_time_input, add_button, clear_button]),
        table,
    ])
