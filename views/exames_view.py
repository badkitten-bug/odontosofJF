import flet as ft

def exames_view(historia_id):
    """
    Vista para gestionar exámenes auxiliares y placas.
    """
    return ft.Column([
        ft.Text(f"Exámenes Auxiliares para Historia ID: {historia_id}", size=20, weight="bold"),
        ft.TextField(label="Tipo de Examen", width=500),
        ft.TextField(label="Resultados", multiline=True, width=500),
        ft.TextField(label="Observaciones", multiline=True, width=500),
        ft.ElevatedButton("Guardar Exámenes", on_click=lambda e: print(f"Exámenes guardados para {historia_id}"))
    ])
