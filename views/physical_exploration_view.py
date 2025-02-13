import flet as ft

def physical_exploration_view(historia_id):
    """
    Vista para gestionar la exploración física de un paciente.
    """
    return ft.Column([
        ft.Text(f"Exploración Física para Historia ID: {historia_id}", size=20, weight="bold"),
        ft.TextField(label="Motivo de Consulta", multiline=True, width=500),
        ft.TextField(label="Signos y Síntomas", multiline=True, width=500),
        ft.TextField(label="Antecedentes Personales", multiline=True, width=500),
        ft.TextField(label="Antecedentes Familiares", multiline=True, width=500),
        ft.ElevatedButton("Guardar Exploración Física", on_click=lambda e: print(f"Exploración guardada para {historia_id}"))
    ])
