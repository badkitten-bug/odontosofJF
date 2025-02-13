import flet as ft

def treatments_view(historia_id):
    """
    Vista para gestionar los tratamientos realizados a un paciente.
    """
    return ft.Column([
        ft.Text(f"Tratamientos Realizados para Historia ID: {historia_id}", size=20, weight="bold"),
        ft.TextField(label="Tipo de Tratamiento", width=500),
        ft.TextField(label="Detalles del Tratamiento", multiline=True, width=500),
        ft.ElevatedButton("Guardar Tratamiento", on_click=lambda e: print(f"Tratamiento guardado para {historia_id}"))
    ])
