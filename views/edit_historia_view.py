import flet as ft
from controllers.historia_controller import HistoriaController
from views.physical_exploration_view import physical_exploration_view
from views.odontogram_view import odontogram_view
from views.diagnostic_view import diagnostic_view
from views.evolution_view import evolution_view
from views.exames_view import exames_view
from views.treatments_view import treatments_view
from views.quotes_view import quotes_view  # Para citas
from views.patient_view import patients_view  # Para datos del paciente


def edit_historia_view(page: ft.Page, historia_id, return_to_list):
    controller = HistoriaController()
    historia = controller.get_historia(historia_id)

    if not historia:
        page.snack_bar = ft.SnackBar(ft.Text("Record not found"))
        page.snack_bar.open = True
        page.update()
        return

    # Extract patient and history data
    (
        historia_id, history_number, creation_date, observations,
        patient_id, first_name, last_name, birth_date, age, dni,
        address, gender, occupation, marital_status, email,
        country, department, province, district, patient_observation
    ) = historia

    # -------------------------------
    # 📌 Tabs with Modular Views
    # -------------------------------
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Datos del Paciente", content=patients_view(historia_id)),  # ✅ FIXED
            ft.Tab(text="Exploración Física", content=physical_exploration_view(historia_id)),
            ft.Tab(text="Odontograma", content=odontogram_view(historia_id)),
            ft.Tab(text="Diagnóstico", content=diagnostic_view(historia_id)),
            ft.Tab(text="Evolución", content=evolution_view(historia_id)),
            ft.Tab(text="Exámenes Auxiliares", content=exames_view(historia_id)),
            ft.Tab(text="Tratamientos", content=treatments_view(historia_id)),
            ft.Tab(text="Citas", content=quotes_view(historia_id)),  # ✅ Agregado si necesitas ver citas
        ]
    )

    # -------------------------------
    # 📌 Action Buttons
    # -------------------------------
    def save_changes(e):
        page.snack_bar = ft.SnackBar(ft.Text("Changes saved successfully"))
        page.snack_bar.open = True
        page.update()

    save_button = ft.ElevatedButton("Save Changes", on_click=save_changes)
    back_button = ft.ElevatedButton("Back", on_click=lambda e: return_to_list())

    # -------------------------------
    # 📌 Layout
    # -------------------------------
    return ft.Column([
        ft.Text(f"Edit Clinical History - {history_number}", size=24, weight="bold"),
        ft.Divider(),
        tabs,
        ft.Row([save_button, back_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    ])
