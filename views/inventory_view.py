import flet as ft
from controllers.inventory_controller import InventoryController

def inventory_view(page: ft.Page, dynamic_content: ft.Column, menu_controller):
    controller = InventoryController()

    # **Lista de Inventario**
    def load_inventory():
        inventory_list.rows.clear()
        for item in controller.get_all_items():
            item_id, name, description, category, quantity, unit_price, supplier, status, date_added = item
            inventory_list.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(name)),
                        ft.DataCell(ft.Text(description)),
                        ft.DataCell(ft.Text(category)),
                        ft.DataCell(ft.Text(str(quantity))),
                        ft.DataCell(ft.Text(f"S/{unit_price:.2f}")),
                        ft.DataCell(ft.Text(supplier if supplier else "N/A")),
                        ft.DataCell(ft.Text(status)),
                        ft.DataCell(ft.Text(date_added)),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, on_click=lambda e, i=item_id: open_edit_dialog(i))),
                        ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, i=item_id: open_delete_dialog(i)))
                    ]
                )
            )
        page.update()

    # **Diálogo para agregar o editar producto**
    def open_edit_dialog(item_id=None):
        item_data = None
        if item_id:
            item_data = next((i for i in controller.get_all_items() if i[0] == item_id), None)

        name_field = ft.TextField(label="Nombre", value=item_data[1] if item_data else "")
        description_field = ft.TextField(label="Descripción", value=item_data[2] if item_data else "")
        quantity_field = ft.TextField(label="Cantidad", value=str(item_data[4]) if item_data else "")
        price_field = ft.TextField(label="Precio Unitario", value=str(item_data[5]) if item_data else "")

        def save_item(e):
            if item_id:
                controller.update_item(item_id, name_field.value, description_field.value, 1, int(quantity_field.value), float(price_field.value), None, "Disponible")
            else:
                controller.add_item(name_field.value, description_field.value, 1, int(quantity_field.value), float(price_field.value), None, "Disponible")
            dialog.open = False
            page.update()
            load_inventory()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar / Editar Producto"),
            content=ft.Column([name_field, description_field, quantity_field, price_field]),
            actions=[ft.TextButton("Guardar", on_click=save_item), ft.TextButton("Cancelar", on_click=lambda e: close_dialog())],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        page.open(dialog)

    def close_dialog():
        page.dialog.open = False
        page.update()

    def open_delete_dialog(item_id):
        def confirm_delete(e):
            controller.delete_item(item_id)
            page.dialog.open = False
            page.update()
            load_inventory()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar Producto"),
            content=ft.Text("¿Estás seguro de que deseas eliminar este producto?"),
            actions=[
                ft.TextButton("Eliminar", on_click=confirm_delete),
                ft.TextButton("Cancelar", on_click=lambda e: close_dialog())
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dialog
        page.open(dialog)

    inventory_list = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Cantidad")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Proveedor")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Fecha Agregado")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Eliminar")),
        ],
        rows=[]
    )

    load_inventory()

    return ft.Container(
        ft.Column([
            ft.Text("Gestión de Inventario", size=24, weight="bold"),
            inventory_list,
            ft.ElevatedButton("Agregar Producto", on_click=lambda e: open_edit_dialog()),
            ft.ElevatedButton("Volver", on_click=lambda e: menu_controller.show_menu_view())
        ], spacing=10),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.GREY_300)
    )
