import flet as ft

def diagnostic_view(historia_id):
    """
    Vista para gestionar los diagnósticos de una historia clínica.
    """
    return ft.Column([
        ft.Text(f"Diagnóstico para Historia ID: {historia_id}", size=20, weight="bold"),
        ft.TextField(label="Diagnóstico Principal", multiline=True, width=500),
        ft.TextField(label="Observaciones", multiline=True, width=500),
        ft.ElevatedButton("Guardar Diagnóstico", on_click=lambda e: print(f"Diagnóstico guardado para {historia_id}"))
    ])
