import flet as ft

def quotes_view(historia_id):
    """
    Vista para mostrar las citas relacionadas con una historia clínica.
    """
    # Simular datos de citas (esto debe ser reemplazado por datos reales desde el controlador)
    citas = [
        {"id": 1, "fecha": "2023-07-01", "hora": "10:00 AM", "estado": "Completada"},
        {"id": 2, "fecha": "2023-08-15", "hora": "02:00 PM", "estado": "Pendiente"},
    ]

    # Tabla para mostrar citas
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cita["id"]))),
                    ft.DataCell(ft.Text(cita["fecha"])),
                    ft.DataCell(ft.Text(cita["hora"])),
                    ft.DataCell(ft.Text(cita["estado"])),
                ]
            )
            for cita in citas
        ],
    )

    return ft.Column([
        ft.Text(f"Citas para Historia ID: {historia_id}", size=20, weight="bold"),
        table,
        ft.ElevatedButton("Agregar Nueva Cita", on_click=lambda e: print(f"Agregar nueva cita para historia {historia_id}")),
    ])
