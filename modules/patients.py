import flet as ft
import time
from database.db_config import connect_db

def load_patients():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE is_deleted = 0")
        return cursor.fetchall()

def patients_view(page: ft.Page):
    selected_patient_id = None
    current_date = time.strftime("%Y-%m-%d")

    # Definir los inputs del formulario de registro
    nombres_input = ft.TextField(label="Nombres *", width=200)
    apellidos_input = ft.TextField(label="Apellidos *", width=200)
    edad_input = ft.TextField(label="Edad *", width=80)
    grado_instruccion_input = ft.Dropdown(
        label="Grado Instrucción *",
        width=150,
        options=[
            ft.dropdown.Option("Primaria"),
            ft.dropdown.Option("Secundaria"),
            ft.dropdown.Option("Universitaria")
        ]
    )
    hospital_nacimiento_input = ft.TextField(label="Hospital de nacimiento *", width=200)
    pais_input = ft.Dropdown(
        label="País *",
        width=150,
        options=[ft.dropdown.Option("Perú"), ft.dropdown.Option("Otro")]
    )
    departamento_input = ft.Dropdown(
        label="Departamento *",
        width=150,
        options=[ft.dropdown.Option("Lima"), ft.dropdown.Option("Cusco"), ft.dropdown.Option("Arequipa")]
    )
    provincia_input = ft.Dropdown(label="Provincia", width=150, options=[ft.dropdown.Option("Provincia 1")])
    distrito_input = ft.Dropdown(label="Distrito", width=150, options=[ft.dropdown.Option("Distrito 1")])
    direccion_input = ft.TextField(label="Dirección *", width=250)
    documento_input = ft.TextField(label="Documento *", width=150)
    telefono_input = ft.TextField(label="Teléfono *", width=150)
    fecha_nacimiento_input = ft.TextField(label="Fecha nacimiento * (YYYY-MM-DD)", width=150)
    estado_civil_input = ft.Dropdown(
        label="Estado civil",
        width=150,
        options=[ft.dropdown.Option("Soltero(a)"), ft.dropdown.Option("Casado(a)"), ft.dropdown.Option("Divorciado(a)")]
    )
    afiliado_input = ft.Dropdown(
        label="Afiliado",
        width=150,
        options=[ft.dropdown.Option("Afiliado"), ft.dropdown.Option("No Afiliado")]
    )
    sexo_label = ft.Text("Sexo *", size=14)
    sexo_input = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(label="Masculino", value="Masculino"),
            ft.Radio(label="Femenino", value="Femenino")
        ])
    )
    estado_input = ft.Dropdown(
        label="Estado *",
        width=150,
        options=[ft.dropdown.Option("Activado"), ft.dropdown.Option("Inactivado")]
    )
    alergia_input = ft.TextField(label="Alergia", width=200)
    correo_input = ft.TextField(label="Correo *", width=250)
    observacion_input = ft.TextField(label="Observación", multiline=True, width=300, height=100)

    # DataTable para el listado de pacientes
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("N°")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Documento")),
            ft.DataColumn(ft.Text("Dirección")),
            ft.DataColumn(ft.Text("F. registro")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    def refresh_table():
        patients = load_patients()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(pt[0]))),                          # ID
                    ft.DataCell(ft.Text(f"{pt[1]} {pt[2]}")),                   # Nombres + Apellidos
                    ft.DataCell(ft.Text(str(pt[3]))),                           # Edad
                    ft.DataCell(ft.Text(pt[11])),                               # Documento
                    ft.DataCell(ft.Text(pt[10])),                               # Dirección
                    ft.DataCell(ft.Text(pt[13])),                               # Fecha registro
                    ft.DataCell(ft.Text(pt[18])),                               # Estado
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=pt[0]: load_patient_to_edit(id)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=pt[0]: delete_patient(id))
                        ])
                    ),
                ]
            )
            for pt in patients
        ]
        page.update()

    def add_patient(e):
        nonlocal selected_patient_id
        if not all([
            nombres_input.value, apellidos_input.value, edad_input.value,
            grado_instruccion_input.value, hospital_nacimiento_input.value,
            pais_input.value, departamento_input.value, direccion_input.value,
            documento_input.value, telefono_input.value, fecha_nacimiento_input.value,
            sexo_input.value, estado_input.value, correo_input.value
        ]):
            page.snack_bar = ft.SnackBar(ft.Text("Todos los campos marcados con * son obligatorios."))
            page.snack_bar.open = True
            page.update()
            return

        with connect_db() as conn:
            cursor = conn.cursor()
            if selected_patient_id:
                cursor.execute(
                    """
                    UPDATE patients 
                    SET nombres = ?, apellidos = ?, edad = ?, grado_instruccion = ?, hospital_nacimiento = ?,
                        pais = ?, departamento = ?, provincia = ?, distrito = ?, direccion = ?, documento = ?,
                        telefono = ?, fecha_nacimiento = ?, sexo = ?, estado = ?, alergia = ?, correo = ?, observacion = ?
                    WHERE id = ?
                    """,
                    (
                        nombres_input.value, apellidos_input.value, edad_input.value, grado_instruccion_input.value,
                        hospital_nacimiento_input.value, pais_input.value, departamento_input.value,
                        provincia_input.value, distrito_input.value, direccion_input.value, documento_input.value,
                        telefono_input.value, fecha_nacimiento_input.value, sexo_input.value, estado_input.value,
                        alergia_input.value, correo_input.value, observacion_input.value,
                        selected_patient_id
                    )
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO patients 
                    (nombres, apellidos, edad, grado_instruccion, hospital_nacimiento, pais, departamento, provincia, distrito, 
                     direccion, documento, telefono, fecha_registro, fecha_nacimiento, estado_civil, afiliado, sexo, estado, alergia, correo, observacion)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        nombres_input.value, apellidos_input.value, edad_input.value, grado_instruccion_input.value,
                        hospital_nacimiento_input.value, pais_input.value, departamento_input.value, provincia_input.value,
                        distrito_input.value, direccion_input.value, documento_input.value, telefono_input.value,
                        current_date, fecha_nacimiento_input.value, "", "",  # estado_civil y afiliado se dejan vacíos si no se usan
                        sexo_input.value, estado_input.value, alergia_input.value, correo_input.value, observacion_input.value
                    )
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
            nombres_input.value = patient[1]
            apellidos_input.value = patient[2]
            edad_input.value = str(patient[3])
            grado_instruccion_input.value = patient[4]
            hospital_nacimiento_input.value = patient[5]
            pais_input.value = patient[6]
            departamento_input.value = patient[7]
            provincia_input.value = patient[8]
            distrito_input.value = patient[9]
            direccion_input.value = patient[10]
            documento_input.value = patient[11]
            telefono_input.value = patient[12]
            fecha_nacimiento_input.value = patient[14]
            sexo_input.value = patient[17]
            estado_input.value = patient[18]
            alergia_input.value = patient[19]
            correo_input.value = patient[20]
            observacion_input.value = patient[21]
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
        nombres_input.value = ""
        apellidos_input.value = ""
        edad_input.value = ""
        grado_instruccion_input.value = ""
        hospital_nacimiento_input.value = ""
        pais_input.value = ""
        departamento_input.value = ""
        provincia_input.value = ""
        distrito_input.value = ""
        direccion_input.value = ""
        documento_input.value = ""
        telefono_input.value = ""
        fecha_nacimiento_input.value = ""
        sexo_input.value = ""
        estado_input.value = ""
        alergia_input.value = ""
        correo_input.value = ""
        observacion_input.value = ""
        page.update()

    add_button = ft.ElevatedButton("Guardar", on_click=add_patient)
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda _: clear_inputs())

    registration_form = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Registrar Paciente", size=24, weight="bold"),
                    ft.Text("Fecha registro: " + current_date),
                    ft.Divider(),
                    ft.Row([nombres_input, apellidos_input], spacing=10),
                    ft.Row([edad_input, grado_instruccion_input], spacing=10),
                    ft.Row([hospital_nacimiento_input, pais_input, departamento_input], spacing=10),
                    ft.Row([provincia_input, distrito_input], spacing=10),
                    ft.Row([direccion_input, documento_input], spacing=10),
                    ft.Row([telefono_input, fecha_nacimiento_input], spacing=10),
                    ft.Row([estado_civil_input, afiliado_input], spacing=10),
                    ft.Row([sexo_label, sexo_input, estado_input], spacing=10),
                    ft.Row([alergia_input, correo_input], spacing=10),
                    observacion_input,
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
                ft.Text("Listado de Pacientes", size=20, weight="bold"),
                table_container,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=20
        ),
        padding=20
    )