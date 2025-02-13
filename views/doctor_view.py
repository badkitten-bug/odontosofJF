import datetime
import flet as ft
from controllers.doctor_controller import DoctorController
from controllers.specialty_controller import SpecialtyController
from controllers.document_type_controller import DocumentTypeController


def doctors_view(page: ft.Page):
    controller = DoctorController()
    specialty_controller = SpecialtyController()
    document_type_controller = DocumentTypeController()
    selected_doctor_id = None

    # Cargar opciones de las tablas
    specialties = specialty_controller.load_specialties()
    document_types = document_type_controller.load_document_types()

    # Inputs del formulario
    nombres_input = ft.TextField(label="Nombres *", width=200)
    apellidos_input = ft.TextField(label="Apellidos *", width=200)
    especialidad_input = ft.Dropdown(
        label="Especialidad *",
        width=200,
        options=[ft.dropdown.Option(str(sp[0]), text=sp[1]) for sp in specialties],
    )
    tipo_documento_input = ft.Dropdown(
        label="Tipo Documento *",
        width=150,
        options=[ft.dropdown.Option(str(dt[0]), text=dt[1]) for dt in document_types],
    )
    nro_documento_input = ft.TextField(label="Número de Documento *", width=150, keyboard_type="number")
    ruc_input = ft.TextField(label="RUC", width=150)
    direccion_input = ft.TextField(label="Dirección", width=250)
    colegiatura_input = ft.TextField(label="Colegiatura", width=150)
    fecha_nacimiento_input = ft.TextField(label="Fecha nacimiento *", width=200, read_only=True)

    # Manejar DatePicker
    def handle_date_change(e):
        """Maneja el evento del DatePicker."""
        if e.data:
            fecha_nacimiento_input.value = e.data.split("T")[0]  # Extraer solo "YYYY-MM-DD"
            page.update()

    fecha_nacimiento_picker = ft.DatePicker(
        first_date=datetime.date(1900, 1, 1),
        last_date=datetime.date(2100, 12, 31),
        on_change=handle_date_change,
    )

    fecha_nacimiento_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.Icons.CALENDAR_MONTH,
        on_click=lambda e: page.open(fecha_nacimiento_picker),
    )

    celular_input = ft.TextField(label="Celular", width=150, keyboard_type="number")
    sexo_input = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(label="Masculino", value="Masculino"),
                ft.Radio(label="Femenino", value="Femenino"),
            ]
        )
    )
    estado_input = ft.Dropdown(
        label="Estado *",
        width=150,
        options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
    )
    correo_input = ft.TextField(label="Correo *", width=250)
    foto_input = ft.TextField(label="Foto (URL)", width=250)

    # DataTable para el listado de doctores
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Celular")),
            ft.DataColumn(ft.Text("F. registro")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[],
    )

    def refresh_table():
        """Actualiza la tabla con los doctores actuales."""
        try:
            doctors = controller.load_doctors()
            table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(doc[0]))),  # ID
                        ft.DataCell(ft.Text(f"{doc[1]} {doc[2]}")),  # Nombre completo
                        ft.DataCell(ft.Text(doc[3])),  # Especialidad
                        ft.DataCell(ft.Text(doc[5])),  # Número de documento
                        ft.DataCell(ft.Text(doc[11])),  # Celular
                        ft.DataCell(ft.Text(doc[9])),  # Fecha de registro
                        ft.DataCell(ft.Text(doc[13])),  # Estado
                        ft.DataCell(
                            ft.Row(
                                [
                                    ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e: load_doctor_to_edit(doc[0])),
                                    ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e: delete_doctor(doc[0])),
                                ]
                            )
                        ),
                    ]
                )
                for doc in doctors
            ]
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al cargar doctores: {str(e)}"))
            page.snack_bar.open = True
        page.update()

    def add_doctor(e):
        """Guarda un nuevo doctor."""
        nonlocal selected_doctor_id
        try:
            data = (
                    nombres_input.value,
                    apellidos_input.value,
                    int(especialidad_input.value),
                    int(tipo_documento_input.value),
                    nro_documento_input.value,
                    ruc_input.value,
                    direccion_input.value,
                    colegiatura_input.value,
                    fecha_nacimiento_input.value,
                    celular_input.value,
                    sexo_input.value,
                    estado_input.value,
                    correo_input.value,
                    foto_input.value,
                )
            if selected_doctor_id:
                controller.update_doctor(selected_doctor_id, data)
            else:
                data = (
                    nombres_input.value, apellidos_input.value, int(especialidad_input.value), int(tipo_documento_input.value),
                    nro_documento_input.value, ruc_input.value, direccion_input.value, colegiatura_input.value,
                    datetime.date.today().strftime("%Y-%m-%d"),  # 🔹 Asegurar que la fecha de registro está en la posición correcta
                    fecha_nacimiento_input.value, celular_input.value, sexo_input.value,
                    estado_input.value, correo_input.value, foto_input.value
                )
                controller.add_doctor(data)
            clear_inputs()  # Limpia los inputs después de actualizar
            refresh_table()  # 🔹 Actualiza la tabla inmediatamente después de editar
            page.update()  # 🔹 Fuerza la actualización de la UI
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al guardar doctor: {str(ex)}"))
            page.snack_bar.open = True
        page.update()

    def load_doctor_to_edit(doctor_id):
        """Carga los datos de un doctor existente para editar."""
        nonlocal selected_doctor_id
        selected_doctor_id = doctor_id
        doctor = controller.get_doctor_by_id(doctor_id)
        if doctor:
            nombres_input.value = doctor[1]
            apellidos_input.value = doctor[2]
            especialidad_input.value = str(doctor[3])
            tipo_documento_input.value = str(doctor[4])
            nro_documento_input.value = doctor[5]
            ruc_input.value = doctor[6]
            direccion_input.value = doctor[7]
            colegiatura_input.value = doctor[8]
            fecha_nacimiento_input.value = doctor[10]
            celular_input.value = doctor[11]
            sexo_input.value = doctor[12]
            estado_input.value = doctor[13]
            correo_input.value = doctor[14]
            foto_input.value = doctor[15]
            page.update()

    def delete_doctor(doctor_id):
        """Elimina un doctor (soft delete)."""
        controller.delete_doctor(doctor_id)
        refresh_table()

    def clear_inputs():
        """Limpia los campos del formulario."""
        nonlocal selected_doctor_id
        selected_doctor_id = None
        for input_field in [
            nombres_input,
            apellidos_input,
            especialidad_input,
            tipo_documento_input,
            nro_documento_input,
            ruc_input,
            direccion_input,
            colegiatura_input,
            fecha_nacimiento_input,
            celular_input,
            correo_input,
            foto_input,
        ]:
            input_field.value = ""
        sexo_input.value = ""
        estado_input.value = ""
        page.update()

    add_button = ft.ElevatedButton("Guardar", on_click=add_doctor)
    clear_button = ft.ElevatedButton("Limpiar", on_click=clear_inputs)

    # Formulario
    registration_form = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Registrar Odontólogo", size=24, weight="bold"),
                    ft.Divider(),
                    ft.Row([nombres_input, apellidos_input], spacing=10),
                    ft.Row([especialidad_input, tipo_documento_input, nro_documento_input], spacing=10),
                    ft.Row([ruc_input, direccion_input, colegiatura_input], spacing=10),
                    ft.Row([fecha_nacimiento_input, fecha_nacimiento_button], spacing=10),
                    ft.Row([celular_input, sexo_input, estado_input], spacing=10),
                    ft.Row([correo_input, foto_input], spacing=10),
                    ft.Row([add_button, clear_button], spacing=10),
                ],
                spacing=10
            )
        )
    )

    refresh_table()

    return ft.Column(controls=[registration_form, table])
