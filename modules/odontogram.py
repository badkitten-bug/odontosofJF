import flet as ft
from database.db_config import connect_db

# odontogram.py
def odontogram_view(page: ft.Page, patient_id):
    selected_odontogram_id = None

    def load_odontogram():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, tooth_number, condition, notes, date
                FROM odontogram
                WHERE patient_id = ?
            ''', (patient_id,))
            return cursor.fetchall()

    def add_odontogram_entry(e):
        nonlocal selected_odontogram_id
        if not tooth_number_input.value or not condition_input.value or not date_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Tooth Number, Condition, and Date are required."))
            page.snack_bar.open = True
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_odontogram_id:
                cursor.execute(
                    "UPDATE odontogram SET tooth_number = ?, condition = ?, notes = ?, date = ? WHERE id = ?",
                    (int(tooth_number_input.value), condition_input.value, notes_input.value, date_input.value, selected_odontogram_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO odontogram (patient_id, tooth_number, condition, notes, date) VALUES (?, ?, ?, ?, ?)",
                    (patient_id, int(tooth_number_input.value), condition_input.value, notes_input.value, date_input.value)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def refresh_table():
        odontogram_entries = load_odontogram()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(str(entry[1]))),  # Tooth Number
                    ft.DataCell(ft.Text(entry[2])),  # Condition
                    ft.DataCell(ft.Text(entry[3])),  # Notes
                    ft.DataCell(ft.Text(entry[4])),  # Date
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_odontogram_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_odontogram(id)
                    )),
                ]
            )
            for entry in odontogram_entries
        ]
        page.update()

    def load_odontogram_to_edit(odontogram_id):
        nonlocal selected_odontogram_id
        selected_odontogram_id = odontogram_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM odontogram WHERE id = ?", (odontogram_id,))
            odontogram_entry = cursor.fetchone()
        if odontogram_entry:
            tooth_number_input.value = str(odontogram_entry[1])
            condition_input.value = odontogram_entry[2]
            notes_input.value = odontogram_entry[3]
            date_input.value = odontogram_entry[4]
            page.update()

    def delete_odontogram(odontogram_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM odontogram WHERE id = ?", (odontogram_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_odontogram_id
        selected_odontogram_id = None
        tooth_number_input.value = ""
        condition_input.value = ""
        notes_input.value = ""
        date_input.value = ""
        page.update()

    tooth_number_input = ft.TextField(label="Tooth Number", keyboard_type=ft.KeyboardType.NUMBER)
    condition_input = ft.TextField(label="Condition")
    notes_input = ft.TextField(label="Notes")
    date_input = ft.TextField(label="Date (YYYY-MM-DD)")
    add_button = ft.ElevatedButton("Save", on_click=add_odontogram_entry)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tooth Number")),
            ft.DataColumn(ft.Text("Condition")),
            ft.DataColumn(ft.Text("Notes")),
            ft.DataColumn(ft.Text("Date")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text(f"Odontogram for Patient ID: {patient_id}", size=24, weight="bold"),
        ft.Row([tooth_number_input, condition_input, notes_input, date_input, add_button, clear_button]),
        table,
    ])
