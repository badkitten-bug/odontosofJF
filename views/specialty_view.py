import flet as ft
from controllers.specialty_controller import SpecialtyController

def specialty_view(page: ft.Page):
    controller = SpecialtyController()
    selected_specialty_id = None

    # Componentes de la interfaz
    nombre_input = ft.TextField(label="Especialidad", width=300)
    descripcion_input = ft.TextField(label="Descripción", width=300)
    estado_input = ft.Dropdown(
        label="Estado",
        width=150,
        options=[ft.dropdown.Option("Activo"), ft.dropdown.Option("Inactivo")],
        value="Activo"
    )
    save_button = ft.ElevatedButton("Guardar", on_click=lambda e: save_specialty(e))
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda e: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def refresh_table():
        """Actualiza la tabla con las especialidades actuales."""
        specialties = controller.load_specialties()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(sp[0]))),  # ID
                    ft.DataCell(ft.Text(sp[1])),       # Nombre
                    ft.DataCell(ft.Text(sp[2])),       # Descripción
                    ft.DataCell(ft.Text(sp[3])),       # Estado
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=sp[0]: load_specialty_to_edit(id)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=sp[0]: delete_specialty(id))
                        ])
                    ),
                ]
            )
            for sp in specialties
        ]
        page.update()

    def load_specialty_to_edit(specialty_id):
        """Carga una especialidad para editar."""
        nonlocal selected_specialty_id
        selected_specialty_id = specialty_id
        specialty = controller.model.get_specialty_by_id(specialty_id)
        if specialty:
            nombre_input.value = specialty[1]  # Nombre
            descripcion_input.value = specialty[2]  # Descripción
            estado_input.value = specialty[3]  # Estado
            page.update()

    def delete_specialty(specialty_id):
        """Elimina una especialidad."""
        controller.delete_specialty(specialty_id)
        refresh_table()

    def save_specialty(e):
        """Guarda una nueva especialidad o actualiza una existente."""
        nonlocal selected_specialty_id
        try:
            if not nombre_input.value or not descripcion_input.value:
                raise ValueError("El nombre y la descripción son obligatorios.")

            if selected_specialty_id:
                controller.update_specialty(selected_specialty_id, nombre_input.value, descripcion_input.value, estado_input.value)
            else:
                controller.add_specialty(nombre_input.value, descripcion_input.value, estado_input.value)

            clear_inputs()
            refresh_table()
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            page.snack_bar.open = True
            page.update()

    def clear_inputs():
        """Limpia los campos de entrada."""
        nonlocal selected_specialty_id
        selected_specialty_id = None
        nombre_input.value = ""
        descripcion_input.value = ""
        estado_input.value = "Activo"
        page.update()

    # Cargar datos iniciales
    refresh_table()

    return ft.Column([
        ft.Text("Gestión de Especialidades", size=24, weight="bold"),
        ft.Row([nombre_input, descripcion_input, estado_input, save_button, clear_button], spacing=10),
        table,
    ])