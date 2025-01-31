import flet as ft
from database.db_config import connect_db

# prescriptions.py
def prescriptions_view(page: ft.Page):
    selected_prescription_id = None

    def load_prescriptions():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT prescriptions.id, patients.name, doctors.name, prescriptions.date, prescriptions.medication, prescriptions.dosage, prescriptions.instructions
                FROM prescriptions
                JOIN patients ON prescriptions.patient_id = patients.id
                JOIN doctors ON prescriptions.doctor_id = doctors.id
            ''')
            return cursor.fetchall()

    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM patients")
            return cursor.fetchall()

    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM doctors")
            return cursor.fetchall()

    def add_prescription(e):
        nonlocal selected_prescription_id
        if not patient_dropdown.value or not doctor_dropdown.value or not date_input.value or not medication_input.value or not dosage_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_prescription_id:
                cursor.execute(
                    "UPDATE prescriptions SET patient_id = ?, doctor_id = ?, date = ?, medication = ?, dosage = ?, instructions = ? WHERE id = ?",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_input.value, medication_input.value, dosage_input.value, instructions_input.value, selected_prescription_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO prescriptions (patient_id, doctor_id, date, medication, dosage, instructions) VALUES (?, ?, ?, ?, ?, ?)",
                    (int(patient_dropdown.value), int(doctor_dropdown.value), date_input.value, medication_input.value, dosage_input.value, instructions_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        prescription_entries = load_prescriptions()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),  # Patient Name
                    ft.DataCell(ft.Text(entry[2])),  # Doctor Name
                    ft.DataCell(ft.Text(entry[3])),  # Date
                    ft.DataCell(ft.Text(entry[4])),  # Medication
                    ft.DataCell(ft.Text(entry[5])),  # Dosage
                    ft.DataCell(ft.Text(entry[6])),  # Instructions
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_prescription_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_prescription(id)
                    )),
                ]
            )
            for entry in prescription_entries
        ]
        page.update()

    def load_prescription_to_edit(prescription_id):
        nonlocal selected_prescription_id
        selected_prescription_id = prescription_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prescriptions WHERE id = ?", (prescription_id,))
            prescription_entry = cursor.fetchone()
        if prescription_entry:
            patient_dropdown.value = str(prescription_entry[1])
            doctor_dropdown.value = str(prescription_entry[2])
            date_input.value = prescription_entry[3]
            medication_input.value = prescription_entry[4]
            dosage_input.value = prescription_entry[5]
            instructions_input.value = prescription_entry[6]
            page.update()

    def delete_prescription(prescription_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prescriptions WHERE id = ?", (prescription_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_prescription_id
        selected_prescription_id = None
        patient_dropdown.value = None
        doctor_dropdown.value = None
        date_input.value = ""
        medication_input.value = ""
        dosage_input.value = ""
        instructions_input.value = ""
        page.update()

    patients = load_patients()
    doctors = load_doctors()
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pid[0]), text=pid[1]) for pid in patients],
        label="Select Patient"
    )
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(did[0]), text=did[1]) for did in doctors],
        label="Select Doctor"
    )
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    medication_input = ft.TextField(label="Medication")
    dosage_input = ft.TextField(label="Dosage")
    instructions_input = ft.TextField(label="Instructions")
    add_button = ft.ElevatedButton("Save", on_click=add_prescription)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Medication")),
            ft.DataColumn(ft.Text("Dosage")),
            ft.DataColumn(ft.Text("Instructions")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Prescriptions Management", size=24, weight="bold"),
        ft.Row([patient_dropdown, doctor_dropdown, date_input, medication_input, dosage_input, instructions_input, add_button, clear_button]),
        table,
    ])
