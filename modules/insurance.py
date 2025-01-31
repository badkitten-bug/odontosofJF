import flet as ft
from database.db_config import connect_db

# insurance.py
def insurance_view(page: ft.Page):
    selected_insurance_id = None

    def load_insurance():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, patient_id, insurance_company, policy_number, coverage_details FROM insurance")
            return cursor.fetchall()

    def add_insurance(e):
        nonlocal selected_insurance_id
        if not patient_dropdown.value or not company_input.value or not policy_input.value or not coverage_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_insurance_id:
                cursor.execute(
                    "UPDATE insurance SET patient_id = ?, insurance_company = ?, policy_number = ?, coverage_details = ? WHERE id = ?",
                    (int(patient_dropdown.value), company_input.value, policy_input.value, coverage_input.value, selected_insurance_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO insurance (patient_id, insurance_company, policy_number, coverage_details) VALUES (?, ?, ?, ?)",
                    (int(patient_dropdown.value), company_input.value, policy_input.value, coverage_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        insurance_entries = load_insurance()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(str(entry[1]))),  # Patient ID
                    ft.DataCell(ft.Text(entry[2])),  # Insurance Company
                    ft.DataCell(ft.Text(entry[3])),  # Policy Number
                    ft.DataCell(ft.Text(entry[4])),  # Coverage Details
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_insurance_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_insurance(id)
                    )),
                ]
            )
            for entry in insurance_entries
        ]
        page.update()

    def load_insurance_to_edit(insurance_id):
        nonlocal selected_insurance_id
        selected_insurance_id = insurance_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM insurance WHERE id = ?", (insurance_id,))
            insurance_entry = cursor.fetchone()
        if insurance_entry:
            patient_dropdown.value = str(insurance_entry[1])
            company_input.value = insurance_entry[2]
            policy_input.value = insurance_entry[3]
            coverage_input.value = insurance_entry[4]
            page.update()

    def delete_insurance(insurance_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM insurance WHERE id = ?", (insurance_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_insurance_id
        selected_insurance_id = None
        patient_dropdown.value = None
        company_input.value = ""
        policy_input.value = ""
        coverage_input.value = ""
        page.update()

    patients = [(str(p[0]), p[1]) for p in load_insurance()]
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(pid, text=name) for pid, name in patients],
        label="Select Patient"
    )
    company_input = ft.TextField(label="Insurance Company")
    policy_input = ft.TextField(label="Policy Number")
    coverage_input = ft.TextField(label="Coverage Details")
    add_button = ft.ElevatedButton("Save", on_click=add_insurance)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Insurance Company")),
            ft.DataColumn(ft.Text("Policy Number")),
            ft.DataColumn(ft.Text("Coverage Details")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Insurance Management", size=24, weight="bold"),
        ft.Row([patient_dropdown, company_input, policy_input, coverage_input, add_button, clear_button]),
        table,
    ])