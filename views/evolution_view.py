import flet as ft

def evolution_view(historia_id):
    """
    Vista para gestionar la evolución clínica de un paciente.
    """
    return ft.Column([
        ft.Text(f"Evolución para Historia ID: {historia_id}", size=20, weight="bold"),
        ft.TextField(label="Detalle de Evolución", multiline=True, width=500, height=150),
        ft.ElevatedButton("Guardar Evolución", on_click=lambda e: print(f"Evolución guardada para {historia_id}"))
    ])
