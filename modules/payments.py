import flet as ft
from database.db_config import connect_db

# payments.py
def payments_view(page: ft.Page):
    selected_payment_id = None

    def load_payments():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT payments.id, patients.name, payments.date, payments.amount, payments.payment_method, payments.status, payments.notes
                FROM payments
                JOIN patients ON payments.patient_id = patients.id
            ''')
            return cursor.fetchall()

    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM patients")
            return cursor.fetchall()

    def add_payment(e):
        nonlocal selected_payment_id
        if not patient_dropdown.value or not date_input.value or not amount_input.value or not method_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_payment_id:
                cursor.execute(
                    "UPDATE payments SET patient_id = ?, date = ?, amount = ?, payment_method = ?, status = ?, notes = ? WHERE id = ?",
                    (int(patient_dropdown.value), date_input.value, float(amount_input.value), method_dropdown.value, status_dropdown.value, notes_input.value, selected_payment_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO payments (patient_id, date, amount, payment_method, status, notes) VALUES (?, ?, ?, ?, ?, ?)",
                    (int(patient_dropdown.value), date_input.value, float(amount_input.value), method_dropdown.value, status_dropdown.value, notes_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        payment_entries = load_payments()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),  # Patient Name
                    ft.DataCell(ft.Text(entry[2])),  # Date
                    ft.DataCell(ft.Text(f"${entry[3]:.2f}")),  # Amount
                    ft.DataCell(ft.Text(entry[4])),  # Payment Method
                    ft.DataCell(ft.Text(entry[5])),  # Status
                    ft.DataCell(ft.Text(entry[6])),  # Notes
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_payment_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_payment(id)
                    )),
                ]
            )
            for entry in payment_entries
        ]
        page.update()

    def load_payment_to_edit(payment_id):
        nonlocal selected_payment_id
        selected_payment_id = payment_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
            payment_entry = cursor.fetchone()
        if payment_entry:
            patient_dropdown.value = str(payment_entry[1])
            date_input.value = payment_entry[2]
            amount_input.value = str(payment_entry[3])
            method_dropdown.value = payment_entry[4]
            status_dropdown.value = payment_entry[5]
            notes_input.value = payment_entry[6]
            page.update()

    def delete_payment(payment_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_payment_id
        selected_payment_id = None
        patient_dropdown.value = None
        date_input.value = ""
        amount_input.value = ""
        method_dropdown.value = ""
        status_dropdown.value = "Pending"
        notes_input.value = ""
        page.update()

    patients = load_patients()
    patient_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(pid[0]), text=pid[1]) for pid in patients],
        label="Select Patient"
    )
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    amount_input = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER)
    method_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Cash"), ft.dropdown.Option("Credit Card"), ft.dropdown.Option("Insurance")],
        label="Payment Method"
    )
    status_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Pending"), ft.dropdown.Option("Completed"), ft.dropdown.Option("Cancelled")],
        label="Status"
    )
    notes_input = ft.TextField(label="Notes")
    add_button = ft.ElevatedButton("Save", on_click=add_payment)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Patient")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Amount")),
            ft.DataColumn(ft.Text("Payment Method")),
            ft.DataColumn(ft.Text("Status")),
            ft.DataColumn(ft.Text("Notes")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Payments Management", size=24, weight="bold"),
        ft.Row([patient_dropdown, date_input, amount_input, method_dropdown, status_dropdown, notes_input, add_button, clear_button]),
        table,
    ])
