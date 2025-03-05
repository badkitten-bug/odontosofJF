import flet as ft
from controllers.odontograma_controller import OdontogramaController

def odontograma_view(page: ft.Page, dynamic_content: ft.Column, menu_controller, historia_id: int):
    controller = OdontogramaController()
    dientes = controller.get_odontograma(historia_id)

    # Diccionario para mapear dientes
    dientes_info = {d[1]: {"condition": d[2], "notes": d[3], "id": d[0]} for d in dientes}

    # Colores según el estado del diente
    colores_dientes = {
        "Sano": ft.Colors.GREEN,
        "Cariado": ft.Colors.RED,
        "Ausente": ft.Colors.GREY_500
    }

    # Diccionario para almacenar los botones de los dientes
    botones_dientes = {}

    # **Función para crear botones representando los dientes**
    def create_diente_button(diente_num):
        estado = dientes_info.get(diente_num, {}).get("condition", "Sano")
        button = ft.TextButton(
            text=f"{diente_num}",
            on_click=lambda e: open_edit_dialog(diente_num),
            width=60,
            height=60,
            style=ft.ButtonStyle(
                bgcolor=colores_dientes.get(estado, ft.Colors.GREY_200)
            )
        )
        botones_dientes[diente_num] = button  # ✅ Ahora el botón se almacena en `botones_dientes`
        return button

    # **Función para abrir el diálogo de edición de un diente**
    def open_edit_dialog(diente_num):
        diente_data = dientes_info.get(diente_num, {})
        diente_id = diente_data.get("id")

        condition_input = ft.Dropdown(
            options=[
                ft.dropdown.Option("Sano"),
                ft.dropdown.Option("Cariado"),
                ft.dropdown.Option("Ausente")
            ],
            value=diente_data.get("condition", "Sano")
        )

        notes_input = ft.TextField(label="Notas", value=diente_data.get("notes", ""))

        def save_diente(e):
            """Guarda los datos del diente en la base de datos y actualiza el color del botón."""
            new_condition = condition_input.value
            new_notes = notes_input.value

            if diente_id:
                controller.update_odontograma(diente_id, new_condition, new_notes)
            else:
                controller.save_odontograma(historia_id, [(diente_num, new_condition, new_notes)])

            # ✅ Verificar si el diente está en `botones_dientes` antes de cambiar el color
            if diente_num in botones_dientes:
                botones_dientes[diente_num].style = ft.ButtonStyle(
                    bgcolor=colores_dientes.get(new_condition, ft.Colors.GREY_200)
                )
                botones_dientes[diente_num].update()
            else:
                print(f"⚠️ Advertencia: Diente {diente_num} no encontrado en botones_dientes.")

            # Mostrar confirmación y cerrar diálogo
            page.snack_bar = ft.SnackBar(ft.Text(f"Diente {diente_num} actualizado."))
            page.snack_bar.open = True
            page.update()
            page.close(dialog)

        # ✅ Crear `AlertDialog` y asignarlo correctamente
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Diente {diente_num}"),
            content=ft.Column([condition_input, notes_input]),
            actions=[
                ft.TextButton("Guardar", on_click=save_diente),
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dialog  # ✅ Asignar el diálogo antes de abrirlo
        page.open(dialog)  # ✅ Ahora se abre correctamente

    # **Crear botones de dientes según el sistema FDI**
    buttons_superior_derecho = [create_diente_button(i) for i in range(18, 10, -1)]
    buttons_superior_izquierdo = [create_diente_button(i) for i in range(21, 29)]
    buttons_inferior_derecho = [create_diente_button(i) for i in range(48, 40, -1)]
    buttons_inferior_izquierdo = [create_diente_button(i) for i in range(31, 39)]

    return ft.Container(
        ft.Column([
            ft.Text("Odontograma", size=24, weight="bold"),

            # 🦷 Dientes Superiores (Orden FDI)
            ft.Row(buttons_superior_derecho, spacing=3),  # Superior Derecho
            ft.Row(buttons_superior_izquierdo, spacing=3),  # Superior Izquierdo

            ft.Text("──────────────────", size=16),  # Separador entre superior e inferior

            # 🦷 Dientes Inferiores (Orden FDI)
            ft.Row(buttons_inferior_derecho, spacing=3),  # Inferior Derecho
            ft.Row(buttons_inferior_izquierdo, spacing=3),  # Inferior Izquierdo

            ft.ElevatedButton("Volver", on_click=lambda e: menu_controller.show_history_detail_view(dynamic_content, historia_id))
        ], spacing=10),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.GREY_300)
    )
