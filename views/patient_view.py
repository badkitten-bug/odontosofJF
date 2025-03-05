import flet as ft
import datetime
from controllers.patient_controller import PatientController

class FormInputs:
    def __init__(self, controller):
        education_levels = controller.load_education_levels()
        marital_statuses = controller.load_marital_statuses()
        document_types = controller.load_document_types()

        self.nombres = ft.TextField(label="Nombres *", width=300, border_radius=10)
        self.apellidos = ft.TextField(label="Apellidos *", width=300, border_radius=10)
        self.documento = ft.TextField(label="DNI *", width=200, border_radius=10)
        self.tipo_documento = ft.Dropdown(
            label="Tipo de Documento *",
            width=200,
            options=[ft.dropdown.Option(text=doc_type[1], key=doc_type[0]) for doc_type in document_types],
            border_radius=10,
        )
        self.grado_instruccion = ft.Dropdown(
            label="Grado de Instrucción *",
            width=300,
            options=[ft.dropdown.Option(text=level[1], key=level[0]) for level in education_levels],
            border_radius=10,
        )
        self.hospital_nacimiento = ft.TextField(label="Lugar de Nacimiento", width=400, border_radius=10)
        self.direccion = ft.TextField(label="Dirección", width=400, border_radius=10)
        self.telefono = ft.TextField(label="Teléfono", width=200, border_radius=10)
        self.alergia = ft.TextField(label="Alergia", width=400, border_radius=10)
        self.fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", read_only=True, width=200, border_radius=10)
        self.edad = ft.TextField(label="Edad", read_only=True, width=100, border_radius=10)
        self.estado_civil = ft.Dropdown(
            label="Estado Civil",
            width=200,
            options=[ft.dropdown.Option(text=status[1], key=status[0]) for status in marital_statuses],
            border_radius=10,
        )
        self.afiliado = ft.Dropdown(
            label="Afiliado *",
            width=200,
            options=[ft.dropdown.Option("Sí"), ft.dropdown.Option("No")],
            border_radius=10,
        )
        self.sexo = ft.Dropdown(
            label="Sexo",
            width=200,
            options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino"), ft.dropdown.Option("Otro")],
            border_radius=10,
        )
        self.correo = ft.TextField(label="Correo Electrónico", width=300, border_radius=10)
        self.observacion = ft.TextField(label="Observación", width=400, multiline=True, min_lines=3, border_radius=10)
        self.estado = ft.Dropdown(
            label="Estado",
            width=200,
            options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
            value="Activo",
            border_radius=10,
        )

    def get_values(self):
        return {
            'nombres': self.nombres.value,
            'apellidos': self.apellidos.value,
            'documento': self.documento.value,
            'tipo_documento': self.tipo_documento.value,
            'grado_instruccion': self.grado_instruccion.value,
            'hospital_nacimiento': self.hospital_nacimiento.value,
            'direccion': self.direccion.value,
            'telefono': self.telefono.value,
            'alergia': self.alergia.value,
            'fecha_nacimiento': self.fecha_nacimiento.value,
            'edad': self.edad.value,
            'estado_civil': self.estado_civil.value,
            'afiliado': self.afiliado.value,
            'sexo': self.sexo.value,
            'correo': self.correo.value,
            'observacion': self.observacion.value,
            'estado': self.estado.value
        }

def create_patient_table():
    return ft.DataTable(
        expand=True,
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

def handle_patient_save(inputs, controller, selected_patient_id, page):
    # Validar campos requeridos
    required_fields = {
        'nombres': inputs.nombres.value,
        'apellidos': inputs.apellidos.value,
        'documento': inputs.documento.value,
        'tipo_documento': inputs.tipo_documento.value,
        'grado_instruccion': inputs.grado_instruccion.value,
        'afiliado': inputs.afiliado.value,
    }
    
    # Verificar que todos los campos requeridos tengan valor
    missing_fields = [field for field, value in required_fields.items() if not value]
    
    if missing_fields:
        show_snack_bar(page, "Error: Los campos marcados con * son obligatorios.", "red")
        return False
        
    data = create_patient_data(inputs)
    save_result = save_patient(data, selected_patient_id, controller)
    return handle_save_result(save_result, page, selected_patient_id)

def patients_view(page: ft.Page):
    controller = PatientController()
    selected_patient_id = None
    
    inputs = FormInputs(controller)
    table = create_patient_table()
    
    # Configurar DatePicker
    def handle_date_change(e):
        if e.data:
            inputs.fecha_nacimiento.value = e.data.split("T")[0]
            fecha_nac = datetime.datetime.strptime(inputs.fecha_nacimiento.value, "%Y-%m-%d")
            edad = datetime.datetime.now().year - fecha_nac.year
            inputs.edad.value = str(edad)
            page.update()

    fecha_nacimiento_picker = ft.DatePicker(
        first_date=datetime.datetime(1900, 1, 1),
        last_date=datetime.datetime(2100, 12, 31),
        on_change=handle_date_change,
    )
    page.overlay.append(fecha_nacimiento_picker)

    fecha_nacimiento_button = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        tooltip="Seleccionar fecha",
        on_click=lambda e: page.open(fecha_nacimiento_picker)
    )
    
    def on_save(e):
        nonlocal selected_patient_id
        if handle_patient_save(inputs, controller, selected_patient_id, page):
            refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
            clear_inputs(inputs, page)
            selected_patient_id = None
            show_snack_bar(page, "Paciente guardado correctamente.", "green")
    
    def on_edit(patient_id):
        nonlocal selected_patient_id
        selected_patient_id = patient_id
        load_patient_to_edit(patient_id, inputs, controller, page)
    
    def on_delete(patient_id):
        confirm_delete(patient_id, controller, page, table, on_edit=on_edit, on_delete=on_delete)
    
    # Crear el formulario
    form = create_form(inputs, on_save, fecha_nacimiento_button, page)
    
    # Crear el contenedor principal con la tabla
    main_content = ft.Column([
        form,
        ft.Container(
            content=ft.Column([
                ft.Text("Lista de Pacientes", size=20, weight="bold", color="blue"),
                ft.Container(
                    content=table,
                    expand=True,
                    border=ft.border.all(1, "lightblue"),
                    border_radius=10,
                    padding=10
                ),
            ], spacing=10),
            expand=True
        )
    ], spacing=20, expand=True)
    
    # Cargar datos iniciales en la tabla
    refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
    
    # Retornar el contenedor principal
    return ft.Container(
        content=main_content,
        padding=20,
        expand=True
    )

def create_form(inputs, on_save, fecha_nacimiento_button, page):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Registrar Paciente", size=24, weight="bold", color="blue"),
                ft.Row([inputs.nombres, inputs.apellidos], spacing=20),
                ft.Row([inputs.tipo_documento, inputs.documento], spacing=20),
                ft.Row([inputs.grado_instruccion, inputs.hospital_nacimiento], spacing=20),
                ft.Row([inputs.direccion, inputs.telefono], spacing=20),
                ft.Row([inputs.fecha_nacimiento, fecha_nacimiento_button, inputs.edad], spacing=20),
                ft.Row([inputs.estado_civil, inputs.afiliado, inputs.sexo], spacing=20),
                ft.Row([inputs.correo], spacing=20),
                ft.Row([inputs.alergia], spacing=20),
                ft.Row([inputs.observacion], spacing=20),
                ft.Row([inputs.estado], spacing=20),
                ft.Row([
                    ft.ElevatedButton("Guardar", on_click=on_save, bgcolor="blue", color="white"),
                    ft.ElevatedButton("Limpiar", on_click=lambda e: clear_inputs(inputs, page), bgcolor="red", color="white")
                ], spacing=20),
            ], spacing=20, expand=True),
            padding=20,
        ),
        elevation=5,
        margin=10,
    )

def create_patient_data(inputs):
    values = inputs.get_values()
    
    # Manejo específico del estado
    estado = values['estado']
    print(f"Estado en el formulario antes de crear data: {estado}")
    print(f"Tipo de dato del estado en el formulario: {type(estado)}")
    
    if not estado or not isinstance(estado, str) or estado.strip() not in ["Activo", "Inactivo"]:
        estado = "Activo"
        print(f"Estado inválido, usando valor por defecto: {estado}")
    else:
        estado = estado.strip()
    
    return (
        values['nombres'],                    # nombres
        values['apellidos'],                  # apellidos
        int(values['edad']) if values['edad'] else 0,  # edad
        int(values['tipo_documento']) if values['tipo_documento'] else None,  # tipo_documento_id
        values['documento'],                  # nro_documento
        None,                                 # history_number (se genera automáticamente)
        int(values['grado_instruccion']) if values['grado_instruccion'] else None,  # grado_instruccion_id
        values['hospital_nacimiento'],        # hospital_nacimiento
        None,                                 # pais
        None,                                 # departamento
        None,                                 # provincia
        None,                                 # distrito
        values['direccion'],                  # direccion
        values['telefono'],                   # telefono
        values['fecha_nacimiento'],           # fecha_nacimiento
        int(values['estado_civil']) if values['estado_civil'] else None,  # estado_civil_id
        values['afiliado'],                   # afiliado
        values['sexo'],                       # sexo
        values['alergia'],                    # alergia
        values['correo'],                     # correo
        values['observacion'],                # observacion
        None,                                 # fecha_registro (se maneja en el backend)
        estado                                # estado
    )

def save_patient(data, selected_patient_id, controller):
    if selected_patient_id:
        return controller.update_patient(selected_patient_id, data)
    return controller.add_patient(data)

def handle_save_result(save_result, page, selected_patient_id):
    if save_result == "Error: Documento duplicado":
        show_snack_bar(page, "Error: El número de documento ya está registrado.", "red")
        return False
    elif save_result != "Success":
        show_snack_bar(page, f"Error al guardar paciente: {save_result}", "red")
        return False
    
    return True  # Ya no mostramos el mensaje aquí, se muestra en on_save

def refresh_table(table, controller, page, on_edit=None, on_delete=None):
    try:
        print("Iniciando refresh_table")  # Debug
        patients = controller.load_patients()
        print(f"Pacientes cargados: {len(patients) if patients else 0}")  # Debug
        
        new_rows = []
        if patients:
            for idx, p in enumerate(patients):
                try:
                    print(f"Datos del paciente {idx + 1}:")  # Debug
                    print(f"Longitud de la tupla: {len(p)}")  # Debug
                    print(f"Valores: {p}")  # Debug
                    
                    # Modificamos la condición para incluir todos los pacientes que no estén explícitamente eliminados
                    is_deleted = p[24] if len(p) > 24 else False
                    if not is_deleted:
                        print(f"Procesando paciente {idx + 1}: {p[2]} {p[3]}")  # Debug
                        row = ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(idx + 1))),
                                ft.DataCell(ft.Text(str(p[1]) if p[1] else "")),
                                ft.DataCell(ft.Text(f"{p[2] or ''} {p[3] or ''}")),
                                ft.DataCell(ft.Text(str(p[4]) if p[4] else "")),
                                ft.DataCell(ft.Text(str(p[6]) if p[6] else "")),
                                ft.DataCell(ft.Text(str(p[9]) if p[9] else "")),
                                ft.DataCell(ft.Text(str(p[17]) if p[17] else "")),
                                ft.DataCell(ft.Text(str(p[18]) if p[18] else "")),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            tooltip="Editar",
                                            on_click=lambda e, id=p[0]: on_edit(id)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Eliminar",
                                            on_click=lambda e, id=p[0]: on_delete(id)
                                        ),
                                    ])
                                ),
                            ]
                        )
                        new_rows.append(row)
                    else:
                        print(f"Paciente {idx + 1} está eliminado, saltando...")  # Debug
                except Exception as row_error:
                    print(f"Error al procesar fila {idx}: {str(row_error)}")  # Debug
                    continue
        
        print(f"Filas creadas: {len(new_rows)}")  # Debug
        table.rows = new_rows
        page.update()
        print("Tabla actualizada")  # Debug
        
    except Exception as e:
        print(f"Error al cargar pacientes: {str(e)}")
        show_snack_bar(page, f"Error al cargar pacientes: {str(e)}", "red")

def clear_inputs(inputs, page):
    for field, value in inputs.get_values().items():
        if hasattr(inputs, field):
            field_obj = getattr(inputs, field)
            if isinstance(field_obj, ft.Dropdown):
                field_obj.value = "Activo" if field == "estado" else None
            else:
                field_obj.value = ""
    page.update()

def show_snack_bar(page, message, color="red"):
    page.snack_bar = ft.SnackBar(
        content=ft.Text(message, color="white"),
        bgcolor=color,
        action="Cerrar",
        action_color="white",
        show_close_icon=True,
    )
    page.snack_bar.open = True
    page.update()

def set_text_fields(inputs, patient_data):
    nombres, apellidos, nro_documento, hospital_nacimiento, direccion, telefono, fecha_nacimiento, edad, alergia, correo, observacion = patient_data
    inputs.nombres.value = nombres or ""
    inputs.apellidos.value = apellidos or ""
    inputs.documento.value = nro_documento or ""
    inputs.hospital_nacimiento.value = hospital_nacimiento or ""
    inputs.direccion.value = direccion or ""
    inputs.telefono.value = telefono or ""
    inputs.fecha_nacimiento.value = fecha_nacimiento or ""
    inputs.edad.value = str(edad) if edad else ""
    inputs.alergia.value = alergia or ""
    inputs.correo.value = correo or ""
    inputs.observacion.value = observacion or ""

def set_dropdown_by_id(dropdown, value_id):
    if value_id:
        for option in dropdown.options:
            if str(option.key) == str(value_id):
                dropdown.value = str(value_id)
                break

def set_dropdowns(inputs, tipo_documento_id, grado_instruccion_id, estado_civil_id, afiliado, sexo, estado):
    set_dropdown_by_id(inputs.tipo_documento, tipo_documento_id)
    set_dropdown_by_id(inputs.grado_instruccion, grado_instruccion_id)
    set_dropdown_by_id(inputs.estado_civil, estado_civil_id)
    
    inputs.afiliado.value = "Sí" if afiliado and afiliado.lower() == "sí" else "No"
    inputs.sexo.value = sexo if sexo in ["Masculino", "Femenino", "Otro"] else None
    
    # Manejo específico del estado
    print(f"Estado recibido en set_dropdowns: {estado}")
    print(f"Tipo de dato del estado recibido: {type(estado)}")
    
    # Asegurar que el estado tenga un valor válido
    if estado and isinstance(estado, str) and estado.strip() in ["Activo", "Inactivo"]:
        inputs.estado.value = estado.strip()
        print(f"Estado establecido desde BD: {inputs.estado.value}")
    else:
        inputs.estado.value = "Activo"
        print(f"Estado establecido por defecto: {inputs.estado.value}")

def load_patient_to_edit(patient_id, inputs, controller, page):
    try:
        patient = controller.get_patient_by_id(patient_id)
        if not patient:
            show_snack_bar(page, "Error: Paciente no encontrado.", "red")
            return

        if len(patient) < 24:
            show_snack_bar(page, "Error: Datos del paciente incompletos.", "red")
            return

        _, _, nombres, apellidos, edad, tipo_documento_id, nro_documento, \
        grado_instruccion_id, hospital_nacimiento, _, _, _, _, direccion, \
        telefono, fecha_nacimiento, estado_civil_id, afiliado, sexo, alergia, \
        correo, observacion, _, estado = patient
        
        patient_text_data = (nombres, apellidos, nro_documento, hospital_nacimiento, 
                           direccion, telefono, fecha_nacimiento, edad, alergia, 
                           correo, observacion)
        set_text_fields(inputs, patient_text_data)
        set_dropdowns(inputs, tipo_documento_id, grado_instruccion_id, 
                     estado_civil_id, afiliado, sexo, estado)

        page.update()
    except Exception as e:
        print(f"Error al cargar paciente: {str(e)}")
        show_snack_bar(page, f"Error al cargar paciente: {str(e)}", "red")

def execute_delete(patient_id, controller, page, table, dialog, on_edit=None, on_delete=None):
    try:
        result = controller.delete_patient(patient_id)
        
        if result == "Success":
            show_snack_bar(page, "Paciente eliminado correctamente.", "green")
            refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
        else:
            show_snack_bar(page, f"Error al eliminar paciente: {result}", "red")
    except Exception as e:
        print(f"Error en execute_delete: {str(e)}")
        show_snack_bar(page, "Error al eliminar el paciente.", "red")

def confirm_delete(patient_id, controller, page, table, on_edit=None, on_delete=None):
    def handle_close(e):
        if e.control.text == "Sí":
            execute_delete(patient_id, controller, page, table, dlg_modal, on_edit, on_delete)
        page.close(dlg_modal)

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este paciente?"),
        actions=[
            ft.TextButton("Sí", on_click=handle_close),
            ft.TextButton("No", on_click=handle_close),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    page.open(dlg_modal)  # Usar page.open() en lugar de asignar a page.dialog

def close_dialog(page, dialog):
    page.dialog = dialog
    dialog.open = False
    page.update()