import flet as ft
import datetime
from controllers.patient_controller import PatientController

def patients_view(page: ft.Page):
    controller = PatientController()
    selected_patient_id = None
    current_date = datetime.datetime.today().strftime("%Y-%m-%d")

    # Cargar opciones de las tablas normalizadas
    education_levels = controller.load_education_levels()
    marital_statuses = controller.load_marital_statuses()
    document_types = controller.load_document_types()

    # Inputs del formulario
    nombres_input = ft.TextField(label="Nombres *", width=200)
    apellidos_input = ft.TextField(label="Apellidos *", width=200)
    documento_input = ft.TextField(label="DNI *", width=150)
    tipo_documento_input = ft.Dropdown(
        label="Tipo de Documento *",
        width=150,
        options=[ft.dropdown.Option(text=doc_type[1], key=doc_type[0]) for doc_type in document_types],
    )
    grado_instruccion_input = ft.Dropdown(
        label="Grado de Instrucción *",
        width=200,
        options=[ft.dropdown.Option(text=level[1], key=level[0]) for level in education_levels],
    )
    hospital_nacimiento_input = ft.TextField(label="Hospital de Nacimiento", width=250)
    direccion_input = ft.TextField(label="Dirección", width=250)
    telefono_input = ft.TextField(label="Teléfono", width=150)
    fecha_nacimiento_picker = ft.TextField(label="Fecha de Nacimiento", read_only=True, width=150)
    edad_input = ft.TextField(label="Edad", read_only=True, width=100)
    estado_civil_input = ft.Dropdown(
        label="Estado Civil",
        width=150,
        options=[ft.dropdown.Option(text=status[1], key=status[0]) for status in marital_statuses],
    )
    afiliado_input = ft.Dropdown(
        label="Afiliado *",
        width=150,
        options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
    )
    sexo_input = ft.Dropdown(
        label="Sexo",
        width=150,
        options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
    )
    correo_input = ft.TextField(label="Correo Electrónico", width=200)
    observacion_input = ft.TextField(label="Observación", width=250, multiline=True)
    estado_input = ft.Dropdown(
        label="Estado",
        width=150,
        options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
    )

    # Botón para abrir el DatePicker
    def open_date_picker(e):
        page.open(date_picker)

    def set_date(e):
        fecha_nacimiento_picker.value = e.control.value.strftime("%Y-%m-%d")
        edad_input.value = str(datetime.datetime.now().year - e.control.value.year)
        page.update()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(1900, 1, 1),
        last_date=datetime.datetime(2050, 12, 31),
        on_change=set_date,
    )

    fecha_nacimiento_button = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH, on_click=open_date_picker
    )

    # Tabla de pacientes
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("N°")),
            ft.DataColumn(ft.Text("Historia Clínica")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("F. Registro")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[],
    )

    def refresh_table():
        patients = controller.load_patients()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(idx + 1))),
                    ft.DataCell(ft.Text(p[1])),
                    ft.DataCell(ft.Text(f"{p[2]} {p[3]}")),
                    ft.DataCell(ft.Text(str(p[4]))),
                    ft.DataCell(ft.Text(p[6])),
                    ft.DataCell(ft.Text(p[9])),
                    ft.DataCell(ft.Text(p[17])),
                    ft.DataCell(ft.Text(p[18])),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=p[0]: load_patient_to_edit(id)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=p[0]: delete_patient(id)),
                        ])
                    ),
                ]
            )
            for idx, p in enumerate(patients)
        ]
        page.update()

    def add_patient(e):
        nonlocal selected_patient_id
        if not all([
            nombres_input.value, apellidos_input.value, documento_input.value,
            fecha_nacimiento_picker.value, estado_input.value,
            grado_instruccion_input.value, afiliado_input.value
        ]):
            page.snack_bar = ft.SnackBar(ft.Text("Completa los campos obligatorios.", color="red"))
            page.snack_bar.open = True
            return

        data = (
            nombres_input.value, apellidos_input.value, int(edad_input.value),
            tipo_documento_input.key, documento_input.value,
            grado_instruccion_input.key, hospital_nacimiento_input.value,
            direccion_input.value, telefono_input.value, fecha_nacimiento_picker.value,
            estado_civil_input.key, afiliado_input.value, sexo_input.value,
            correo_input.value, observacion_input.value, current_date, estado_input.value
        )

        if selected_patient_id:
            controller.update_patient(selected_patient_id, data)
        else:
            controller.add_patient(data)

        clear_inputs()
        refresh_table()

    def load_patient_to_edit(patient_id):
        nonlocal selected_patient_id
        selected_patient_id = patient_id
        patient = controller.get_patient_by_id(patient_id)
        if patient:
            nombres_input.value = patient[2]
            apellidos_input.value = patient[3]
            tipo_documento_input.key = patient[5]
            documento_input.value = patient[6]
            grado_instruccion_input.key = patient[7]
            hospital_nacimiento_input.value = patient[8]
            direccion_input.value = patient[9]
            telefono_input.value = patient[10]
            fecha_nacimiento_picker.value = patient[11]
            edad_input.value = str(patient[4])
            estado_civil_input.key = patient[12]
            afiliado_input.value = patient[13]
            sexo_input.value = patient[14]
            correo_input.value = patient[15]
            observacion_input.value = patient[16]
            estado_input.value = patient[18]
            page.update()

    def delete_patient(patient_id):
        controller.delete_patient(patient_id)
        refresh_table()

    def clear_inputs():
        nonlocal selected_patient_id
        selected_patient_id = None
        nombres_input.value = ""
        apellidos_input.value = ""
        documento_input.value = ""
        tipo_documento_input.key = ""
        grado_instruccion_input.key = ""
        hospital_nacimiento_input.value = ""
        direccion_input.value = ""
        telefono_input.value = ""
        fecha_nacimiento_picker.value = ""
        edad_input.value = ""
        estado_civil_input.key = ""
        afiliado_input.value = ""
        sexo_input.value = ""
        correo_input.value = ""
        observacion_input.value = ""
        estado_input.value = ""
        page.update()

    add_button = ft.ElevatedButton("Guardar", on_click=add_patient)
    clear_button = ft.ElevatedButton("Limpiar", on_click=clear_inputs)

    form = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Registrar Paciente", size=24, weight="bold"),
                ft.Row([nombres_input, apellidos_input]),
                ft.Row([tipo_documento_input, documento_input]),
                ft.Row([grado_instruccion_input, hospital_nacimiento_input]),
                ft.Row([direccion_input, telefono_input]),
                ft.Row([fecha_nacimiento_picker, fecha_nacimiento_button, edad_input]),
                ft.Row([estado_civil_input, afiliado_input, sexo_input]),
                ft.Row([correo_input]),
                ft.Row([observacion_input]),
                ft.Row([estado_input]),
                ft.Row([add_button, clear_button]),
            ]),
        )
    )

    refresh_table()

    return ft.Container(content=ft.Column([form, table]), padding=20)