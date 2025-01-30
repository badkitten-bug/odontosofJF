import flet as ft
from database.db_config import connect_db

# inventory.py
def inventory_view(page: ft.Page):
    def load_items():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            return cursor.fetchall()

    def refresh_table():
        items = load_items()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(item[0]))),
                    ft.DataCell(ft.Text(item[1])),
                    ft.DataCell(ft.Text(item[2])),
                    ft.DataCell(ft.Text(str(item[3]))),
                    ft.DataCell(ft.Text(str(item[4]))),
                ]
            )
            for item in items
        ]
        page.update()

    name_input = ft.TextField(label="Name")
    description_input = ft.TextField(label="Description")
    quantity_input = ft.TextField(label="Quantity", keyboard_type=ft.KeyboardType.NUMBER)
    cost_input = ft.TextField(label="Cost", keyboard_type=ft.KeyboardType.NUMBER)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Quantity")),
            ft.DataColumn(ft.Text("Cost")),
        ],
        rows=[]
    )

    refresh_table()

    return ft.Column([
        ft.Text("Inventory Management", size=24, weight="bold"),
        ft.Row([name_input, description_input, quantity_input, cost_input]),
        table,
    ])

# Repeat for payments, prescriptions, feedback, etc., adapting the structure as shown above to each module's requirements.
