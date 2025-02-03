import flet as ft
from controllers.historia_controller import HistoriaController

def historia_view(page: ft.Page):
    controller = HistoriaController()
    selected_historia_id = None

    # Componentes de la interfaz
    numero_historia_input = ft.TextField(label="Número de Historia *", width=200)
    fecha_creacion_input = ft.TextField(label="Fecha de Creación * (YYYY-MM-DD)", width=200)
    observaciones_input = ft.TextField(label="Observaciones", width=300, multiline=True)

    # DataTable para el listado de historias clínicas
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Número de Historia")),
            ft.DataColumn(ft.Text("Paciente")),
            ft.DataColumn(ft.Text("DNI")),
            ft.DataColumn(ft.Text("Fecha Creación")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    def refresh_table():
        """Actualiza la tabla con las historias clínicas actuales."""
        historias = controller.load_historias()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(h[0]))),  # ID
                    ft.DataCell(ft.Text(h[1])),       # Número de Historia
                    ft.DataCell(ft.Text(f"{h[2]} {h[3]}")),  # Paciente
                    ft.DataCell(ft.Text(h[4])),       # DNI
                    ft.DataCell(ft.Text(h[5])),       # Fecha Creación
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e, id=h[0]: load_historia_to_edit(id)),
                            ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, id=h[0]: delete_historia(id))
                        ])
                    ),
                ]
            )
            for h in historias
        ]
        page.update()

    def add_historia(e):
        """Guarda una nueva historia clínica."""
        nonlocal selected_historia_id
        try:
            if not all([numero_historia_input.value, fecha_creacion_input.value]):
                raise ValueError("Todos los campos marcados con * son obligatorios.")

            # Aquí debes agregar la lógica para guardar la historia clínica en la base de datos
            print("Historia clínica guardada:", numero_historia_input.value, fecha_creacion_input.value, observaciones_input.value)

            # Limpiar los campos después de guardar
            clear_inputs()
            refresh_table()
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            page.snack_bar.open = True
            page.update()

    def load_historia_to_edit(historia_id):
        """Carga una historia clínica para editar."""
        nonlocal selected_historia_id
        selected_historia_id = historia_id
        # Aquí debes cargar los datos de la historia clínica y llenar los campos del formulario
        pass

    def delete_historia(historia_id):
        """Elimina una historia clínica."""
        controller.delete_historia(historia_id)
        refresh_table()

    def clear_inputs():
        """Limpia los campos de entrada."""
        nonlocal selected_historia_id
        selected_historia_id = None
        numero_historia_input.value = ""
        fecha_creacion_input.value = ""
        observaciones_input.value = ""
        page.update()

    add_button = ft.ElevatedButton("Guardar", on_click=add_historia)
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda e: clear_inputs())

    registration_form = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Historia Odontológica", size=24, weight="bold"),
                    ft.Divider(),
                    ft.Row([numero_historia_input, fecha_creacion_input], spacing=10),
                    ft.Row([observaciones_input], spacing=10),
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
                ft.Text("Listado de Historias Clínicas", size=20, weight="bold"),
                table_container,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=20
        ),
        padding=20
    )