import flet as ft
from database.db_config import connect_db

def history_view(page: ft.Page, patient_id):
    def load_history():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT history.id, history.date, history.diagnosis, history.procedure, history.notes, doctors.name
                FROM history
                JOIN doctors ON history.doctor_id = doctors.id
                WHERE history.patient_id = ?
            ''', (patient_id,))
            return cursor.fetchall()

    def add_history_entry(e):
        if not doctor_dropdown.value or not date_input.value or not diagnosis_input.value or not procedure_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO history (patient_id, doctor_id, date, diagnosis, procedure, notes, attachments)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (patient_id, int(doctor_dropdown.value), date_input.value, diagnosis_input.value, procedure_input.value, notes_input.value, "No files")
            )
            conn.commit()
        refresh_table()
        clear_inputs()

    def refresh_table():
        history = load_history()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),      # Date
                    ft.DataCell(ft.Text(entry[2])),      # Diagnosis
                    ft.DataCell(ft.Text(entry[3])),      # Procedure
                    ft.DataCell(ft.Text(entry[4])),      # Notes
                    ft.DataCell(ft.Text(entry[5])),      # Doctor Name
                ]
            )
            for entry in history
        ]
        page.update()

    def clear_inputs():
        doctor_dropdown.value = None
        date_input.value = ""
        diagnosis_input.value = ""
        procedure_input.value = ""
        notes_input.value = ""
        page.update()

    # Cargar doctores
    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM doctors")
            return cursor.fetchall()

    doctors = load_doctors()

    # Inputs
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=doc[1]) for doc in doctors],
        label="Select Doctor"
    )
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    diagnosis_input = ft.TextField(label="Diagnosis")
    procedure_input = ft.TextField(label="Procedure")
    notes_input = ft.TextField(label="Notes")
    add_button = ft.ElevatedButton("Add Entry", on_click=add_history_entry)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    # Tabla
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Diagnosis")),
            ft.DataColumn(ft.Text("Procedure")),
            ft.DataColumn(ft.Text("Notes")),
            ft.DataColumn(ft.Text("Doctor")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column(
        [
            ft.Text(f"Medical History for Patient ID: {patient_id}", size=24, weight="bold"),
            ft.Row([doctor_dropdown, date_input, diagnosis_input, procedure_input, notes_input]),
            ft.Row([add_button, clear_button]),
            table,
        ]
    )
