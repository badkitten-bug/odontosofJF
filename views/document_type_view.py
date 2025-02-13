import flet as ft
from controllers.document_type_controller import DocumentTypeController

def document_type_view(page: ft.Page):
    controller = DocumentTypeController()
    selected_doc_type_id = None

    # Componentes de la interfaz
    name_input = ft.TextField(label="Nombre del Tipo de Documento", width=300)
    save_button = ft.ElevatedButton("Guardar", on_click=lambda e: save_document_type(e))
    clear_button = ft.ElevatedButton("Limpiar", on_click=lambda e: clear_inputs())

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    def refresh_table():
        """Actualiza la tabla con los tipos de documentos actuales."""
        document_types = controller.load_document_types()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(doc[0]))),  # ID
                    ft.DataCell(ft.Text(doc[1])),       # Nombre
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, id=doc[0]: load_document_type_to_edit(id)),
                            ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=doc[0]: delete_document_type(id))
                        ])
                    ),
                ]
            )
            for doc in document_types
        ]
        page.update()

    def load_document_type_to_edit(doc_type_id):
        """Carga un tipo de documento para editar."""
        nonlocal selected_doc_type_id
        selected_doc_type_id = doc_type_id
        doc_type = controller.get_document_type_by_id(doc_type_id)
        if doc_type:
            name_input.value = doc_type[1]
            page.update()

    def delete_document_type(doc_type_id):
        """Elimina un tipo de documento."""
        controller.delete_document_type(doc_type_id)
        refresh_table()

    def save_document_type(e):
        """Guarda un nuevo tipo de documento o actualiza uno existente."""
        nonlocal selected_doc_type_id
        try:
            if not name_input.value:
                raise ValueError("El nombre del tipo de documento es obligatorio.")

            if selected_doc_type_id:
                controller.update_document_type(selected_doc_type_id, name_input.value)
            else:
                controller.add_document_type(name_input.value)

            clear_inputs()
            refresh_table()
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(ft.Text(str(ve)))
            page.snack_bar.open = True
            page.update()

    def clear_inputs():
        """Limpia los campos de entrada."""
        nonlocal selected_doc_type_id
        selected_doc_type_id = None
        name_input.value = ""
        page.update()

    # Cargar datos iniciales
    refresh_table()

    return ft.Column([
        ft.Text("Gestión de Tipos de Documento", size=24, weight="bold"),
        ft.Row([name_input, save_button, clear_button], spacing=10),
        table,
    ])
