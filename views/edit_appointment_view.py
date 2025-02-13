import flet as ft
from controllers.appointment_controller import AppointmentController

def edit_appointment_view(page: ft.Page, appointment_id, refresh_table):
    controller = AppointmentController()
    appointment_data = controller.get_appointment_by_id(appointment_id)

    if not appointment_data:
        page.snack_bar = ft.SnackBar(content=ft.Text("⚠️ Error: No se pudo cargar la cita.", color="red"))
        page.snack_bar.open = True
        page.update()
        return

    # Extraer los datos de la cita
    appointment_id, patient_id, doctor_id, date, time, duration, notes, status_id, status = appointment_data

    print(f"📌 Cargando cita ID: {appointment_id} | Estado actual: {status}")  # Debug

    # 📌 Campos del formulario
    date_field = ft.TextField(label="Fecha", value=date, expand=True)
    time_field = ft.TextField(label="Hora", value=time, expand=True)
    duration_field = ft.TextField(label="Duración (minutos)", value=str(duration), expand=True)
    notes_field = ft.TextField(label="Notas", value=notes, expand=True, multiline=True)

    # 📌 Dropdowns para paciente, doctor y estado
    patient_dropdown = ft.Dropdown(
        label="Paciente",
        options=[ft.dropdown.Option(str(p[0]), text=p[1]) for p in controller.load_patients()],
        value=str(patient_id),
        expand=True
    )

    doctor_dropdown = ft.Dropdown(
        label="Doctor",
        options=[ft.dropdown.Option(str(d[0]), text=d[1]) for d in controller.load_doctors()],
        value=str(doctor_id),
        expand=True
    )

    # 📌 Obtener la lista de estados
    statuses = controller.load_appointment_statuses()

    # 📌 Buscar el ID correspondiente al estado actual
    status_id = next((str(st[0]) for st in statuses if st[1] == status), None)
    if status_id is None:
        print(f"⚠️ Advertencia: No se encontró un estado coincidente para {status}")
        status_id = str(statuses[0][0])  # Selecciona el primer estado como predeterminado

    status_dropdown = ft.Dropdown(
        label="Estado",
        options=[ft.dropdown.Option(str(st[0]), text=st[1]) for st in statuses],
        value=status_id,
        expand=True
    )

    # ✅ Guardar cambios con validaciones
    def save_changes(e):
        if not all([patient_dropdown.value, doctor_dropdown.value, date_field.value, time_field.value, status_dropdown.value]):
            page.snack_bar = ft.SnackBar(content=ft.Text("⚠️ Todos los campos son obligatorios.", color="red"))
            page.snack_bar.open = True
            page.update()
            return

        updated_data = (
            patient_dropdown.value,
            doctor_dropdown.value,
            date_field.value,
            time_field.value,
            duration_field.value,
            notes_field.value,
            status_dropdown.value,
        )

        print(f"✅ Guardando cambios: {updated_data}")  # Debug
        controller.save_appointment(appointment_id, updated_data)
        page.snack_bar = ft.SnackBar(content=ft.Text("✅ Cita actualizada correctamente.", color="green"))
        page.snack_bar.open = True
        refresh_table()  # Refrescar la tabla
        page.close(edit_dialog)  # ✅ Cierra el diálogo correctamente
        page.update()

    # 📌 Diálogo de edición con `modal=True`
    edit_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("📝 Editar Cita"),
        content=ft.Column([
            patient_dropdown,
            doctor_dropdown,
            date_field,
            time_field,
            duration_field,
            notes_field,
            status_dropdown,
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(edit_dialog)),  # ✅ Cierra correctamente
            ft.ElevatedButton("Guardar", on_click=save_changes, bgcolor="blue"),
        ],
    )

    # 📌 Usar `page.open(dialogo)` en lugar de `dialogo.open = True`
    print("✅ Abriendo el formulario de edición...")  # Debug
    page.open(edit_dialog)
    page.update()
