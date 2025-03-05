import datetime
import flet as ft
from controllers.doctor_controller import DoctorController

class FormInputs:
    def __init__(self, controller):
        specialties = controller.load_specialties()
        document_types = controller.load_document_types()

        self.nombres = ft.TextField(label="Nombres *", width=300, border_radius=10)
        self.apellidos = ft.TextField(label="Apellidos *", width=300, border_radius=10)
        self.especialidad = ft.Dropdown(
            label="Especialidad *",
            width=300,
            options=[ft.dropdown.Option(text=spec[1], key=spec[0]) for spec in specialties],
            border_radius=10,
        )
        self.tipo_documento = ft.Dropdown(
            label="Tipo de Documento *",
            width=200,
            options=[ft.dropdown.Option(text=doc_type[1], key=doc_type[0]) for doc_type in document_types],
            border_radius=10,
        )
        self.nro_documento = ft.TextField(label="Número de Documento *", width=200, border_radius=10)
        self.ruc = ft.TextField(label="RUC", width=200, border_radius=10)
        self.direccion = ft.TextField(label="Dirección", width=400, border_radius=10)
        self.colegiatura = ft.TextField(label="Colegiatura *", width=200, border_radius=10)
        self.fecha_nacimiento = ft.TextField(label="Fecha de Nacimiento", read_only=True, width=200, border_radius=10)
        self.celular = ft.TextField(label="Celular", width=150, keyboard_type="number", border_radius=10)
        self.sexo = ft.Dropdown(
            label="Sexo",
            width=200,
            options=[ft.dropdown.Option("Masculino"), ft.dropdown.Option("Femenino")],
            border_radius=10,
        )
        self.estado = ft.Dropdown(
            label="Estado *",
            width=150,
            options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
            value="Activo",
            border_radius=10,
        )
        self.correo = ft.TextField(label="Correo *", width=250, border_radius=10)
        self.foto = ft.TextField(label="Foto (URL)", width=250, border_radius=10)

    def get_values(self):
        return {
            'nombres': self.nombres.value,
            'apellidos': self.apellidos.value,
            'especialidad': self.especialidad.value,
            'tipo_documento': self.tipo_documento.value,
            'nro_documento': self.nro_documento.value,
            'ruc': self.ruc.value,
            'direccion': self.direccion.value,
            'colegiatura': self.colegiatura.value,
            'fecha_nacimiento': self.fecha_nacimiento.value,
            'celular': self.celular.value,
            'sexo': self.sexo.value,
            'estado': self.estado.value,
            'correo': self.correo.value,
            'foto': self.foto.value,
        }

def create_doctor_table():
    return ft.DataTable(
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

def create_doctor_data(inputs, selected_doctor_id):
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
    
    # Para un nuevo doctor, incluimos la fecha de registro
    if not selected_doctor_id:
        return (
            values['nombres'],                    # nombres
            values['apellidos'],                  # apellidos
            int(values['especialidad']) if values['especialidad'] else None,  # especialidad_id
            int(values['tipo_documento']) if values['tipo_documento'] else None,  # tipo_documento_id
            values['nro_documento'],              # nro_documento
            values['ruc'],                        # ruc
            values['direccion'],                  # direccion
            values['colegiatura'],                # colegiatura
            datetime.datetime.now().strftime("%Y-%m-%d"),  # fecha_registro
            values['fecha_nacimiento'],           # fecha_nacimiento
            values['celular'],                    # celular
            values['sexo'],                       # sexo
            estado,                               # estado
            values['correo'],                     # correo
            values['foto']                        # foto
        )
    # Para actualización, excluimos la fecha de registro
    else:
        return (
            values['nombres'],                    # nombres
            values['apellidos'],                  # apellidos
            int(values['especialidad']) if values['especialidad'] else None,  # especialidad_id
            int(values['tipo_documento']) if values['tipo_documento'] else None,  # tipo_documento_id
            values['nro_documento'],              # nro_documento
            values['ruc'],                        # ruc
            values['direccion'],                  # direccion
            values['colegiatura'],                # colegiatura
            values['fecha_nacimiento'],           # fecha_nacimiento
            values['celular'],                    # celular
            values['sexo'],                       # sexo
            estado,                               # estado
            values['correo'],                     # correo
            values['foto']                        # foto
        )

def handle_doctor_save(inputs, controller, selected_doctor_id, page):
    # Validar campos requeridos
    required_fields = {
        'nombres': inputs.nombres.value,
        'apellidos': inputs.apellidos.value,
        'especialidad': inputs.especialidad.value,
        'tipo_documento': inputs.tipo_documento.value,
        'nro_documento': inputs.nro_documento.value,
        'colegiatura': inputs.colegiatura.value,
        'correo': inputs.correo.value,
    }
    
    # Verificar campos requeridos
    missing_fields = [field for field, value in required_fields.items() if not value]
    if missing_fields:
        show_snack_bar(page, "Error: Los campos marcados con * son obligatorios.", "red")
        return False

    data = create_doctor_data(inputs, selected_doctor_id)
    save_result = save_doctor(data, selected_doctor_id, controller)
    return handle_save_result(save_result, page, selected_doctor_id)

def doctors_view(page: ft.Page):
    controller = DoctorController()
    selected_doctor_id = None
    
    inputs = FormInputs(controller)
    table = create_doctor_table()
    
    # Configurar DatePicker
    def handle_date_change(e):
        if e.data:
            inputs.fecha_nacimiento.value = e.data.split("T")[0]  # Extraer solo "YYYY-MM-DD"
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
        nonlocal selected_doctor_id
        if handle_doctor_save(inputs, controller, selected_doctor_id, page):
            refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
            clear_inputs(inputs, page)
            selected_doctor_id = None
    
    def on_edit(doctor_id):
        nonlocal selected_doctor_id
        selected_doctor_id = doctor_id
        load_doctor_to_edit(doctor_id, inputs, controller, page)
    
    def on_delete(doctor_id):
        confirm_delete(doctor_id, controller, page, table, on_edit=on_edit, on_delete=on_delete)
    
    # Actualizar la tabla con los datos iniciales
    refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
    
    form = create_form(inputs, on_save, fecha_nacimiento_button, page)
    
    return ft.Container(
        content=ft.Column([form, table], spacing=20, expand=True),
        padding=20,
        expand=True,
    )

def create_form(inputs, on_save, fecha_nacimiento_button, page):
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("Registrar Odontólogo", size=24, weight="bold", color="blue"),
                ft.Row([inputs.nombres, inputs.apellidos], spacing=20),
                ft.Row([inputs.especialidad, inputs.tipo_documento, inputs.nro_documento], spacing=20),
                ft.Row([inputs.ruc, inputs.direccion, inputs.colegiatura], spacing=20),
                ft.Row([inputs.fecha_nacimiento, fecha_nacimiento_button], spacing=20),
                ft.Row([inputs.celular, inputs.sexo, inputs.estado], spacing=20),
                ft.Row([inputs.correo, inputs.foto], spacing=20),
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

def refresh_table(table, controller, page, on_edit=None, on_delete=None):
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
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=doc[0]: on_edit(id)) if on_edit else ft.Text(""),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=doc[0]: on_delete(id)) if on_delete else ft.Text(""),
                        ])
                    ),
                ]
            )
            for doc in doctors
        ]
        page.update()
    except Exception as e:
        show_snack_bar(page, f"Error al cargar doctores: {str(e)}", "red")

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

def set_text_fields(inputs, doctor_data):
    nombres, apellidos, nro_documento, ruc, direccion, colegiatura, fecha_nacimiento, celular, correo, foto = doctor_data
    inputs.nombres.value = nombres or ""
    inputs.apellidos.value = apellidos or ""
    inputs.nro_documento.value = nro_documento or ""
    inputs.ruc.value = ruc or ""
    inputs.direccion.value = direccion or ""
    inputs.colegiatura.value = colegiatura or ""
    inputs.fecha_nacimiento.value = fecha_nacimiento or ""
    inputs.celular.value = celular or ""
    inputs.correo.value = correo or ""
    inputs.foto.value = foto or ""

def set_dropdown_by_id(dropdown, value_id):
    if value_id:
        for option in dropdown.options:
            if str(option.key) == str(value_id):
                dropdown.value = str(value_id)
                break

def set_dropdowns(inputs, especialidad_id, tipo_documento_id, sexo, estado):
    set_dropdown_by_id(inputs.especialidad, especialidad_id)
    set_dropdown_by_id(inputs.tipo_documento, tipo_documento_id)
    
    inputs.sexo.value = sexo if sexo in ["Masculino", "Femenino"] else None
    
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

def load_doctor_to_edit(doctor_id, inputs, controller, page):
    try:
        doctor = controller.get_doctor_by_id(doctor_id)
        if not doctor:
            show_snack_bar(page, "Error: Doctor no encontrado.", "red")
            return

        if len(doctor) < 16:
            show_snack_bar(page, "Error: Datos del doctor incompletos.", "red")
            return

        _, nombres, apellidos, especialidad_id, tipo_documento_id, nro_documento, \
        ruc, direccion, colegiatura, _, fecha_nacimiento, celular, \
        sexo, estado, correo, foto = doctor
        
        doctor_text_data = (nombres, apellidos, nro_documento, ruc, direccion, 
                          colegiatura, fecha_nacimiento, celular, correo, foto)
        set_text_fields(inputs, doctor_text_data)
        set_dropdowns(inputs, especialidad_id, tipo_documento_id, sexo, estado)

        page.update()
    except Exception as e:
        print(f"Error al cargar doctor: {str(e)}")
        show_snack_bar(page, f"Error al cargar doctor: {str(e)}", "red")

def execute_delete(doctor_id, controller, page, table, dialog, on_edit=None, on_delete=None):
    result = controller.delete_doctor(doctor_id)
    close_dialog(page, dialog)
    if result == "Success":
        show_snack_bar(page, "Doctor eliminado correctamente.", "green")
        refresh_table(table, controller, page, on_edit=on_edit, on_delete=on_delete)
    else:
        show_snack_bar(page, f"Error al eliminar doctor: {result}", "red")

def confirm_delete(doctor_id, controller, page, table, on_edit=None, on_delete=None):
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar eliminación"),
        content=ft.Text("¿Estás seguro de que deseas eliminar este doctor?"),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: execute_delete(doctor_id, controller, page, table, dlg_modal, on_edit, on_delete)),
            ft.TextButton("No", on_click=lambda e: close_dialog(page, dlg_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.dialog = dlg_modal
    dlg_modal.open = True
    page.update()

def close_dialog(page, dialog):
    page.dialog = dialog
    dialog.open = False
    page.update()

def save_doctor(data, selected_doctor_id, controller):
    if selected_doctor_id:
        return controller.update_doctor(selected_doctor_id, data)
    return controller.add_doctor(data)

def handle_save_result(save_result, page, selected_doctor_id):
    if save_result == "Error: Documento duplicado":
        show_snack_bar(page, "Error: El número de documento ya está registrado.", "red")
        return False
    elif save_result != "Success":
        show_snack_bar(page, f"Error al guardar doctor: {save_result}", "red")
        return False
    
    message = "Doctor actualizado correctamente." if selected_doctor_id else "Doctor registrado correctamente."
    show_snack_bar(page, message, "green")
    return True
