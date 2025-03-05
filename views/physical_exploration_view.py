import flet as ft
from controllers.physical_exploration_controller import ExploracionFisicaController

def physical_exploration_view(page: ft.Page, historia_id: int, show_previous_view_callback):
    controller = ExploracionFisicaController()
    exploracion = controller.get_exploracion(historia_id)

    # Crear los campos, precargando valores si existen
    enfermedad_actual_input = ft.TextField(label="Enfermedad Actual", value=exploracion[2] if exploracion else "")
    tiempo_enfermedad_input = ft.TextField(label="Tiempo de Enfermedad", value=exploracion[3] if exploracion else "")
    motivo_consulta_input = ft.TextField(label="Motivo de Consulta", value=exploracion[4] if exploracion else "")
    signos_sintomas_input = ft.TextField(label="Signos y Síntomas", value=exploracion[5] if exploracion else "")
    antecedentes_personales_input = ft.TextField(label="Antecedentes Personales", value=exploracion[6] if exploracion else "")
    antecedentes_familiares_input = ft.TextField(label="Antecedentes Familiares", value=exploracion[7] if exploracion else "")
    medicamento_actual_input = ft.TextField(label="Medicamento Actual", value=exploracion[8] if exploracion else "")
    motivo_uso_medicamento_input = ft.TextField(label="Motivo de Uso de Medicamento", value=exploracion[9] if exploracion else "")
    dosis_medicamento_input = ft.TextField(label="Dosis de Medicamento", value=exploracion[10] if exploracion else "")
    tratamiento_ortodoncia_input = ft.TextField(label="Tratamiento de Ortodoncia", value=exploracion[11] if exploracion else "")
    alergico_medicamento_input = ft.TextField(label="¿Alérgico a Medicamento?", value=exploracion[12] if exploracion else "")
    hospitalizado_input = ft.TextField(label="Hospitalizado", value=exploracion[13] if exploracion else "")
    transtorno_nervioso_input = ft.TextField(label="Trastorno Nervioso", value=exploracion[14] if exploracion else "")
    enfermedades_padecidas_input = ft.TextField(label="Enfermedades Padecidas", value=exploracion[15] if exploracion else "")
    cepilla_dientes_input = ft.TextField(label="Cepilla Dientes", value=exploracion[16] if exploracion else "")
    presion_arterial_input = ft.TextField(label="Presión Arterial", value=exploracion[17] if exploracion else "")

    def save_exploracion(e):
        data = [
            enfermedad_actual_input.value,
            tiempo_enfermedad_input.value,
            motivo_consulta_input.value,
            signos_sintomas_input.value,
            antecedentes_personales_input.value,
            antecedentes_familiares_input.value,
            medicamento_actual_input.value,
            motivo_uso_medicamento_input.value,
            dosis_medicamento_input.value,
            tratamiento_ortodoncia_input.value,
            alergico_medicamento_input.value,
            hospitalizado_input.value,
            transtorno_nervioso_input.value,
            enfermedades_padecidas_input.value,
            cepilla_dientes_input.value,
            presion_arterial_input.value
        ]
        if exploracion:
            controller.update_exploracion(exploracion[0], data)
            action = "actualizada"
        else:
            controller.create_exploracion(historia_id, data)
            action = "creada"

        # Crear y mostrar el AlertDialog
        dialog = ft.AlertDialog(
            title=ft.Text("Información Guardada"),
            content=ft.Text(f"Exploración física {action} correctamente para la historia {historia_id}."),
            actions=[ft.TextButton("OK", on_click=lambda e: page.close(dialog))]
        )
        page.dialog = dialog
        page.open(dialog)
        page.update()

    # ✅ Cerrar el diálogo y regresar a la vista anterior
    def close_and_go_back(dialog):
        dialog.open = False
        page.update()
        show_previous_view_callback()  # ✅ REGRESAR A `history_detail_view`


    return ft.Container(
        ft.Column([
            ft.Text("Exploración Física", size=24, weight="bold"),
            enfermedad_actual_input,
            tiempo_enfermedad_input,
            motivo_consulta_input,
            signos_sintomas_input,
            antecedentes_personales_input,
            antecedentes_familiares_input,
            medicamento_actual_input,
            motivo_uso_medicamento_input,
            dosis_medicamento_input,
            tratamiento_ortodoncia_input,
            alergico_medicamento_input,
            hospitalizado_input,
            transtorno_nervioso_input,
            enfermedades_padecidas_input,
            cepilla_dientes_input,
            presion_arterial_input,
            ft.Row([
                ft.ElevatedButton("Guardar", on_click=save_exploracion),
                ft.ElevatedButton("Volver", on_click=lambda e: show_previous_view_callback())
            ], spacing=10)
        ], spacing=10, scroll=ft.ScrollMode.AUTO),
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=5,
        shadow=ft.BoxShadow(blur_radius=5, spread_radius=1, color=ft.Colors.GREY_300)
    )