import flet as ft
from database.db_config import connect_db

def history_view(page: ft.Page, patient_id):
    selected_history_id = None  # Para almacenar el ID del historial seleccionado para edición

    # Cargar doctores desde la base de datos
    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM doctors")
            return cursor.fetchall()

    # Cargar historial médico desde la base de datos
    def load_history():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT history.id, history.date, history.diagnosis, history.procedure, history.treatment_plan, history.notes, history.attachments, doctors.name
                FROM history
                JOIN doctors ON history.doctor_id = doctors.id
                WHERE history.patient_id = ?
            ''', (patient_id,))
            return cursor.fetchall()

    # Actualizar la tabla de historial médico
    def refresh_table():
        history = load_history()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(entry[0]))),  # ID
                    ft.DataCell(ft.Text(entry[1])),      # Fecha
                    ft.DataCell(ft.Text(entry[2])),      # Diagnóstico
                    ft.DataCell(ft.Text(entry[3])),      # Procedimiento
                    ft.DataCell(ft.Text(entry[4])),      # Plan de tratamiento
                    ft.DataCell(ft.Text(entry[5])),      # Notas
                    ft.DataCell(ft.Text(entry[6])),      # Adjuntos
                    ft.DataCell(ft.Text(entry[7])),      # Nombre del doctor
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.EDIT,
                        on_click=lambda e, id=entry[0]: load_history_to_edit(id)
                    )),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE,
                        on_click=lambda e, id=entry[0]: delete_history(id)
                    )),
                ]
            )
            for entry in history
        ]
        page.update()

    # Cargar una entrada de historial para editar
    def load_history_to_edit(history_id):
        nonlocal selected_history_id
        selected_history_id = history_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT doctor_id, date, diagnosis, procedure, treatment_plan, notes, attachments FROM history WHERE id = ?", (history_id,))
            history_entry = cursor.fetchone()
            if history_entry:
                doctor_dropdown.value = str(history_entry[0])
                date_input.value = history_entry[1]
                diagnosis_input.value = history_entry[2]
                procedure_input.value = history_entry[3]
                treatment_plan_input.value = history_entry[4]
                notes_input.value = history_entry[5]
                attachments_input.value = history_entry[6]
                page.update()

    # Eliminar una entrada de historial
    def delete_history(history_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (history_id,))
            conn.commit()
        refresh_table()

    # Guardar o actualizar una entrada de historial
    def save_history_entry(e):
        try:
            if not doctor_dropdown.value or not date_input.value or not diagnosis_input.value or not procedure_input.value:
                raise ValueError("Todos los campos son obligatorios.")

            with connect_db() as conn:
                cursor = conn.cursor()
                if selected_history_id:
                    cursor.execute(
                        "UPDATE history SET doctor_id = ?, date = ?, diagnosis = ?, procedure = ?, treatment_plan = ?, notes = ?, attachments = ? WHERE id = ?",
                        (int(doctor_dropdown.value), date_input.value, diagnosis_input.value, procedure_input.value, treatment_plan_input.value, notes_input.value, attachments_input.value, selected_history_id)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO history (patient_id, doctor_id, date, diagnosis, procedure, treatment_plan, notes, attachments) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (patient_id, int(doctor_dropdown.value), date_input.value, diagnosis_input.value, procedure_input.value, treatment_plan_input.value, notes_input.value, attachments_input.value)
                    )
                conn.commit()
            clear_inputs()
            refresh_table()
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            page.snack_bar.open = True
            page.update()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ex)}"))
            page.snack_bar.open = True
            page.update()

    # Limpiar los campos del formulario
    def clear_inputs():
        nonlocal selected_history_id
        selected_history_id = None
        doctor_dropdown.value = None
        date_input.value = ""
        diagnosis_input.value = ""
        procedure_input.value = ""
        treatment_plan_input.value = ""
        notes_input.value = ""
        attachments_input.value = ""
        page.update()

    # Controles del formulario
    doctors = load_doctors()
    doctor_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option(str(doc[0]), text=doc[1]) for doc in doctors],
        label="Seleccionar Doctor"
    )
    date_input = ft.TextField(label="Fecha (YYYY-MM-DD)")
    diagnosis_input = ft.TextField(label="Diagnóstico")
    procedure_input = ft.TextField(label="Procedimiento")
    treatment_plan_input = ft.TextField(label="Plan de Tratamiento")
    notes_input = ft.TextField(label="Notas", multiline=True)
    attachments_input = ft.TextField(label="Adjuntos")
    save_button = ft.ElevatedButton("Guardar", on_click=save_history_entry)
    clear_button = ft.ElevatedButton("Limpiar", on_click=clear_inputs)

    # Tabla de historial médico
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Diagnóstico")),
            ft.DataColumn(ft.Text("Procedimiento")),
            ft.DataColumn(ft.Text("Plan de Tratamiento")),
            ft.DataColumn(ft.Text("Notas")),
            ft.DataColumn(ft.Text("Adjuntos")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Eliminar")),
        ],
        rows=[]
    )

    # Cargar datos iniciales
    refresh_table()

    # Retornar la vista
    return ft.Column([
        ft.Text(f"Historial Médico - Paciente ID: {patient_id}", size=24, weight="bold"),
        ft.Row([doctor_dropdown, date_input, diagnosis_input, procedure_input, treatment_plan_input, notes_input, attachments_input]),
        ft.Row([save_button, clear_button]),
        table,
    ])