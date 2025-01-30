import flet as ft
from database.db_config import connect_db

# invoices.py
def invoices_view(page: ft.Page):
    selected_invoice_id = None

    def load_invoices():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT invoices.id, patients.name, invoices.date, invoices.total_amount, invoices.status
                FROM invoices
                JOIN patients ON invoices.patient_id = patients.id
            ''')
            return cursor.fetchall()

    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM patients")
            return cursor.fetchall()

    def add_invoice(e):
        nonlocal selected_invoice_id
        if not patient_dropdown.value or not date_input.value or not total_amount_input.value or not status_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_invoice_id:
                cursor.execute(
                    "UPDATE invoices SET patient_id = ?, date = ?, total_amount = ?, status = ? WHERE id = ?",
                    (int(patient_dropdown.value), date_input.value, float(total_amount_input.value), status_dropdown.value, selected_invoice_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO invoices (patient_id, date, total_amount, status) VALUES (?, ?, ?, ?)",
                    (int(patient_dropdown.value), date_input.value, float(total_amount_input.value), status_dropdown.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        invoice_entries = load_invoices()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),  # Patient Name
                    ft.DataCell(ft.Text(entry[2])),  # Date
                    ft.DataCell(ft.Text(f"${entry[3]:.2f}")),  # Total Amount
                    ft.DataCell(ft.Text(entry[4])),  # Status
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_invoice_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_invoice(id)
                    )),
                ]
            )
            for entry in invoice_entries
        ]
        page.update()

    def load_invoice_to_edit(invoice_id):
        nonlocal selected_invoice_id
        selected_invoice_id = invoice_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
            invoice_entry = cursor.fetchone()
        if invoice_entry:
            patient_dropdown.value = str(invoice_entry[1])
            date_input.value = invoice_entry[2]
            total_amount_input.value = str(invoice_entry[3])
            status_dropdown.value = invoice_entry[4]
            page.update()

    def delete_invoice(invoice_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_invoice_id
        selected_invoice_id = None
        patient_dropdown.value = None
        date_input.value = ""
        total_amount_input.value = ""
        status_dropdown.value = "Pending"
        page.update()

    patients = load_patients()
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pid[0]), text=pid[1]) for pid in patients],
        label="Select Patient"
    )
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    total_amount_input = ft.TextField(label="Total Amount", keyboard_type=ft.KeyboardType.NUMBER)
    status_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Pending"), ft.dropdown.Option("Paid"), ft.dropdown.Option("Cancelled")],
        label="Status"
    )
    add_button = ft.ElevatedButton("Save", on_click=add_invoice)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Total Amount")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Invoices Management", size=24, weight="bold"),
        ft.Row([patient_dropdown, date_input, total_amount_input, status_dropdown, add_button, clear_button]),
        table,
    ])
