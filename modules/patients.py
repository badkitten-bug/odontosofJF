import flet as ft
import time  # Importar el módulo time
from database.db_config import connect_db

# Función para cargar pacientes
def load_patients():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE is_deleted = 0")  # Borrado lógico
        return cursor.fetchall()

def patients_view(page: ft.Page):
    selected_patient_id = None

    def refresh_table():
        patients = load_patients()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pt[0]))),  # ID
                    ft.DataCell(ft.Text(pt[1])),      # Name
                    ft.DataCell(ft.Text(str(pt[2]))), # Age
                    ft.DataCell(ft.Text(pt[3])),      # Phone
                    ft.DataCell(ft.Text(pt[4])),      # Address
                    ft.DataCell(ft.Text(pt[5])),      # History Number
                    ft.DataCell(ft.IconButton(
                        icon=ft.icons.EDIT,
                        on_click=lambda e, id=pt[0]: load_patient_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, id=pt[0]: delete_patient(id)
                    )),
                ]
            )
            for pt in patients
        ]
        page.update()

    def add_patient(e):
        nonlocal selected_patient_id
        if not name_input.value or not age_input.value or not phone_input.value or not address_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("All fields are required."))
            page.snack_bar.open = True
            return

        history_number = f"HC{int(time.time())}"  # Generar número único de HC

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_patient_id:
                cursor.execute(
                    "UPDATE patients SET name = ?, age = ?, phone = ?, address = ?, history_number = ? WHERE id = ?",
                    (name_input.value, age_input.value, phone_input.value, address_input.value, history_number, selected_patient_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO patients (name, age, phone, address, history_number) VALUES (?, ?, ?, ?, ?)",
                    (name_input.value, age_input.value, phone_input.value, address_input.value, history_number)
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def load_patient_to_edit(patient_id):
        nonlocal selected_patient_id
        selected_patient_id = patient_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            patient = cursor.fetchone()
        if patient:
            name_input.value = patient[1]
            age_input.value = str(patient[2])
            phone_input.value = patient[3]
            address_input.value = patient[4]
            page.update()

    def delete_patient(patient_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE patients SET is_deleted = 1 WHERE id = ?", (patient_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_patient_id
        selected_patient_id = None
        name_input.value = ""
        age_input.value = ""
        phone_input.value = ""
        address_input.value = ""
        page.update()

    # Inputs
    name_input = ft.TextField(label="Name")
    age_input = ft.TextField(label="Age")
    phone_input = ft.TextField(label="Phone")
    address_input = ft.TextField(label="Address")
    add_button = ft.ElevatedButton("Save", on_click=add_patient)
    clear_button = ft.ElevatedButton("Clear", on_click=lambda _: clear_inputs())

    # Tabla
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Age")),
            ft.DataColumn(ft.Text("Phone")),
            ft.DataColumn(ft.Text("Address")),
            ft.DataColumn(ft.Text("History Number")),
            ft.DataColumn(ft.Text("Edit")),
            ft.DataColumn(ft.Text("Delete")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column(
        [
            ft.Text("Patients Management", size=24, weight="bold"),
            ft.Row([name_input, age_input, phone_input, address_input, add_button, clear_button]),
            table,
        ]
    )
