import flet as ft
import time
from database.db_config import connect_db

def load_doctors():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        return cursor.fetchall()

def doctors_view(page: ft.Page):
    selected_doctor_id = None
    current_date = time.strftime("%Y-%m-%d")

    # Definir los inputs para el formulario de registro de odontólogos
    nombres_input = ft.TextField(label="Nombres *", width=200)
    apellidos_input = ft.TextField(label="Apellidos *", width=200)
    especialidad_input = ft.TextField(label="Especialidad *", width=200)
    tipo_documento_input = ft.Dropdown(
        label="Tipo Documento",
        width=150,
        options=[
            ft.dropdown.Option("DNI"),
            ft.dropdown.Option("Carné de extranjería")
        ]
    )
    nro_documento_input = ft.TextField(label="Número de Documento", width=150)
    ruc_input = ft.TextField(label="RUC", width=150)
    direccion_input = ft.TextField(label="Dirección", width=250)
    colegiatura_input = ft.TextField(label="Colegiatura", width=150)
    fecha_nacimiento_input = ft.TextField(label="Fecha nacimiento * (YYYY-MM-DD)", width=150)
    telefono_input = ft.TextField(label="Teléfono *", width=150)
    celular_input = ft.TextField(label="Celular", width=150)
    # Para sexo, se utiliza un RadioGroup cuyos controles se envuelven en una Column
    sexo_label = ft.Text("Sexo *", size=14)
    sexo_input = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(label="Masculino", value="Masculino"),
                ft.Radio(label="Femenino", value="Femenino")
            ]
        )
    )
    estado_input = ft.Dropdown(
        label="Estado *",
        width=150,
        options=[ft.dropdown.Option("Activado"), ft.dropdown.Option("Inactivado")]
    )
    correo_input = ft.TextField(label="Correo *", width=250)
    foto_input = ft.TextField(label="Foto (URL)", width=250)
    usuario_input = ft.TextField(label="Usuario *", width=200)
    password_input = ft.TextField(label="Password *", width=200, password=True)

    # DataTable para el listado de odontólogos
    # Se mostrarán: ID, Doctor (nombres + apellidos), Especialidad, Número de Documento,
    # Teléfono, Fecha de registro y Estado
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("F. registro")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    def refresh_table():
        doctors = load_doctors()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(doc[0]))),                          # ID
                    ft.DataCell(ft.Text(f"{doc[1]} {doc[2]}")),                   # Nombres + Apellidos
                    ft.DataCell(ft.Text(doc[3])),                                # Especialidad
                    ft.DataCell(ft.Text(doc[5] or "")),                          # Número de documento (nro_documento) es índice 5
                    ft.DataCell(ft.Text(doc[11])),                               # Teléfono (índice 11)
                    ft.DataCell(ft.Text(doc[9])),                                # Fecha de registro (índice 9)
                    ft.DataCell(ft.Text(doc[14])),                               # Estado (índice 14)
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=doc[0]: load_doctor_to_edit(id)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=doc[0]: delete_doctor(id))
                        ])
                    ),
                ]
            )
            for doc in doctors
        ]
        page.update()

    def add_doctor(e):
        nonlocal selected_doctor_id
        # Validar campos obligatorios
        if not all([
            nombres_input.value, apellidos_input.value, especialidad_input.value,
            fecha_nacimiento_input.value, telefono_input.value, sexo_input.value,
            estado_input.value, correo_input.value, usuario_input.value, password_input.value
        ]):
            page.snack_bar = ft.SnackBar(ft.Text("Todos los campos marcados con * son obligatorios."))
            page.snack_bar.open = True
            page.update()
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_doctor_id:
                cursor.execute(
                    """
                    UPDATE doctors
                    SET nombres = ?, apellidos = ?, especialidad = ?, tipo_documento = ?, nro_documento = ?, ruc = ?,
                        direccion = ?, colegiatura = ?, fecha_nacimiento = ?, telefono = ?, celular = ?, sexo = ?,
                        estado = ?, correo = ?, foto = ?, usuario = ?, password = ?
                    WHERE id = ?
                    """,
                    (
                        nombres_input.value, apellidos_input.value, especialidad_input.value,
                        tipo_documento_input.value, nro_documento_input.value, ruc_input.value,
                        direccion_input.value, colegiatura_input.value, fecha_nacimiento_input.value,
                        telefono_input.value, celular_input.value, sexo_input.value,
                        estado_input.value, correo_input.value, foto_input.value,
                        usuario_input.value, password_input.value,
                        selected_doctor_id
                    )
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO doctors 
                    (nombres, apellidos, especialidad, tipo_documento, nro_documento, ruc, direccion, colegiatura,
                     fecha_registro, fecha_nacimiento, telefono, celular, sexo, estado, correo, foto, usuario, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nombres_input.value, apellidos_input.value, especialidad_input.value,
                        tipo_documento_input.value, nro_documento_input.value, ruc_input.value,
                        direccion_input.value, colegiatura_input.value, current_date,
                        fecha_nacimiento_input.value, telefono_input.value, celular_input.value,
                        sexo_input.value, estado_input.value, correo_input.value, foto_input.value,
                        usuario_input.value, password_input.value
                    )
                )
            conn.commit()
        clear_inputs()
        refresh_table()

    def load_doctor_to_edit(doctor_id):
        nonlocal selected_doctor_id
        selected_doctor_id = doctor_id
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
            doctor = cursor.fetchone()
        if doctor:
            nombres_input.value = doctor[1]
            apellidos_input.value = doctor[2]
            especialidad_input.value = doctor[3]
            tipo_documento_input.value = doctor[4]
            nro_documento_input.value = doctor[5]
            ruc_input.value = doctor[6]
            direccion_input.value = doctor[7]
            colegiatura_input.value = doctor[8]
            # Fecha de registro (doctor[9]) se deja sin editar
            fecha_nacimiento_input.value = doctor[10]
            telefono_input.value = doctor[11]
            celular_input.value = doctor[12]
            sexo_input.value = doctor[13]
            estado_input.value = doctor[14]
            correo_input.value = doctor[15]
            foto_input.value = doctor[16]
            usuario_input.value = doctor[17]
            password_input.value = doctor[18]
            page.update()

    def delete_doctor(doctor_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()
        refresh_table()

    def clear_inputs():
        nonlocal selected_doctor_id
        selected_doctor_id = None
        nombres_input.value = ""
        apellidos_input.value = ""
        especialidad_input.value = ""
        tipo_documento_input.value = ""
        nro_documento_input.value = ""
        ruc_input.value = ""
        direccion_input.value = ""
        colegiatura_input.value = ""
        fecha_nacimiento_input.value = ""
        telefono_input.value = ""
        celular_input.value = ""
        sexo_input.value = ""
        estado_input.value = ""
        correo_input.value = ""
        foto_input.value = ""
        usuario_input.value = ""
        password_input.value = ""
        page.update()

    add_button = ft.ElevatedButton("Guardar", on_click=add_doctor)
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda _: clear_inputs())

    registration_form = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Registrar Odontólogo", size=24, weight="bold"),
                    ft.Text("Fecha registro: " + current_date),
                    ft.Divider(),
                    ft.Row([nombres_input, apellidos_input], spacing=10),
                    ft.Row([especialidad_input, tipo_documento_input, nro_documento_input], spacing=10),
                    ft.Row([ruc_input, direccion_input, colegiatura_input], spacing=10),
                    ft.Row([fecha_nacimiento_input, telefono_input, celular_input], spacing=10),
                    ft.Row([sexo_label, sexo_input, estado_input], spacing=10),
                    ft.Row([correo_input, foto_input], spacing=10),
                    ft.Row([usuario_input, password_input], spacing=10),
                    ft.Row([add_button, clear_button], spacing=10),
                ],
                spacing=10
            ),
            padding=15,
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=8, spread_radius=1, color=ft.Colors.BLACK12)
        )
    )

    table_container = ft.Column(
        controls=[table],
        expand=True,
        spacing=10
    )

    refresh_table()

    return ft.Container(
        content=ft.Column(
            controls=[
                registration_form,
                ft.Divider(height=20),
                ft.Text("Listado de Odontólogos", size=20, weight="bold"),
                table_container,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=20
        ),
        padding=20
    )
