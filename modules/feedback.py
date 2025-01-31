import flet as ft
from database.db_config import connect_db

# feedback.py
def feedback_view(page: ft.Page):
    selected_feedback_id = None

    def load_feedback():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT feedback.id, patients.name, doctors.name, feedback.date, feedback.rating, feedback.comments
                FROM feedback
                JOIN patients ON feedback.patient_id = patients.id
                JOIN doctors ON feedback.doctor_id = doctors.id
            ''')
            return cursor.fetchall()

    def add_feedback(e):
        nonlocal selected_feedback_id
        if not patient_dropdown.value or not doctor_dropdown.value or not date_input.value or not rating_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_feedback_id:
                cursor.execute(
                    "UPDATE feedback SET patient_id = ?, doctor_id = ?, date = ?, rating = ?, comments = ? WHERE id = ?",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_input.value, int(rating_input.value), comments_input.value, selected_feedback_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO feedback (patient_id, doctor_id, date, rating, comments) VALUES (?, ?, ?, ?, ?)",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_input.value, int(rating_input.value), comments_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        feedback_entries = load_feedback()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),  # Patient Name
                    ft.DataCell(ft.Text(entry[2])),  # Doctor Name
                    ft.DataCell(ft.Text(entry[3])),  # Date
                    ft.DataCell(ft.Text(str(entry[4]))),  # Rating
                    ft.DataCell(ft.Text(entry[5])),  # Comments
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_feedback_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_feedback(id)
                    )),
                ]
            )
            for entry in feedback_entries
        ]
        page.update()

    def load_feedback_to_edit(feedback_id):
        nonlocal selected_feedback_id
        selected_feedback_id = feedback_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM feedback WHERE id = ?", (feedback_id,))
            feedback_entry = cursor.fetchone()
        if feedback_entry:
            patient_dropdown.value = str(feedback_entry[1])
            doctor_dropdown.value = str(feedback_entry[2])
            date_input.value = feedback_entry[3]
            rating_input.value = str(feedback_entry[4])
            comments_input.value = feedback_entry[5]
            page.update()

    def delete_feedback(feedback_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feedback WHERE id = ?", (feedback_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_feedback_id
        selected_feedback_id = None
        patient_dropdown.value = None
        doctor_dropdown.value = None
        date_input.value = ""
        rating_input.value = ""
        comments_input.value = ""
        page.update()

    patients = [(str(p[0]), p[1]) for p in load_feedback()]
    doctors = [(str(d[0]), d[1]) for d in load_feedback()]

    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(pid, text=name) for pid, name in patients],
        label="Select Patient"
    )
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(did, text=name) for did, name in doctors],
        label="Select Doctor"
    )
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    rating_input = ft.TextField(label="Rating (1-5)", keyboard_type=ft.KeyboardType.NUMBER)
    comments_input = ft.TextField(label="Comments")
    add_button = ft.ElevatedButton("Save", on_click=add_feedback)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Rating")),
            ft.DataColumn(ft.Text("Comments")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Patient Feedback", size=24, weight="bold"),
        ft.Row([patient_dropdown, doctor_dropdown, date_input, rating_input, comments_input, add_button, clear_button]),
        table,
    ])
