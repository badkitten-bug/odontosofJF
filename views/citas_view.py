import flet as ft
from controllers.citas_controller import CitasController

def citas_view(page: ft.Page, dynamic_content: ft.Column, menu_controller, paciente_id: int):
    controller = CitasController()
    citas = controller.get_citas(paciente_id)

    estado_dict = {1: "Pendiente", 2: "Completada", 3: "Cancelada"}

    # **Tabla de Citas**
    citas_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Hora")),
            ft.DataColumn(ft.Text("Doctor")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    def create_cita_row(cita):
        """Crea una fila en la tabla de citas."""
        cita_id, fecha, hora_inicio, hora_fin, notas, estado_id, doctor_nombre, doctor_apellido = cita
        estado_text = estado_dict.get(estado_id, "Desconocido")

        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(fecha)),
                ft.DataCell(ft.Text(f"{hora_inicio} - {hora_fin}")),
                ft.DataCell(ft.Text(f"Dr. {doctor_nombre} {doctor_apellido}")),
                ft.DataCell(ft.Text(estado_text)),
                ft.DataCell(ft.Row([
                    ft.IconButton(icon=ft.Icons.EDIT, tooltip="Cambiar Estado", on_click=lambda e: open_edit_dialog(cita_id, estado_id)),
                    ft.IconButton(icon=ft.Icons.REMOVE_RED_EYE, tooltip="Ver Detalles", on_click=lambda e: open_details_dialog(cita_id, fecha, hora_inicio, hora_fin, notas, doctor_nombre, doctor_apellido, estado_text))
                ]))
            ]
        )

    # **Diálogo para cambiar el estado de una cita**
    def open_edit_dialog(cita_id, estado_actual):
        estado_dropdown = ft.Dropdown(
            options=[ft.dropdown.Option("Pendiente"), ft.dropdown.Option("Completada"), ft.dropdown.Option("Cancelada")],
            value=estado_dict.get(estado_actual, "Pendiente")
        )

        def save_estado(e):
            estado_inverse_dict = {"Pendiente": 1, "Completada": 2, "Cancelada": 3}
            nuevo_estado = estado_inverse_dict[estado_dropdown.value]
            controller.update_cita_status(cita_id, nuevo_estado)

            page.snack_bar = ft.SnackBar(ft.Text("Estado de la cita actualizado."))
            page.snack_bar.open = True
            page.update()
            page.close(dialog)

            refresh_citas()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Actualizar Estado de la Cita"),
            content=estado_dropdown,
            actions=[
                ft.TextButton("Guardar", on_click=save_estado),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        page.open(dialog)

    # **Diálogo para ver detalles de una cita**
    def open_details_dialog(cita_id, fecha, hora_inicio, hora_fin, notas, doctor_nombre, doctor_apellido, estado_text):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalles de la Cita"),
            content=ft.Column([
                ft.Text(f"📅 Fecha: {fecha}"),
                ft.Text(f"🕐 Hora: {hora_inicio} - {hora_fin}"),
                ft.Text(f"👨‍⚕️ Doctor: {doctor_nombre} {doctor_apellido}"),
                ft.Text(f"📌 Estado: {estado_text}"),
                ft.Text(f"📝 Notas: {notas}")
            ]),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog
        page.open(dialog)

    # **Actualizar la Tabla de Citas**
    def refresh_citas():
        citas_table.rows.clear()
        for c in controller.get_citas(paciente_id):
            citas_table.rows.append(create_cita_row(c))
        page.update()

    # **Cargar citas en la tabla**
    for c in citas:
        citas_table.rows.append(create_cita_row(c))

    return ft.Container(
        ft.Column([
            ft.Text("Citas del Paciente", size=24, weight="bold"),
            citas_table,
            ft.ElevatedButton("Volver", on_click=lambda e: menu_controller.show_history_detail_view(dynamic_content, paciente_id))
        ], spacing=10),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.GREY_300)
    )
