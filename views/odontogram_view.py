import flet as ft

def odontogram_view(historia_id):
    """
    Vista para gestionar el odontograma de un paciente.
    """
    return ft.Column([
        ft.Text(f"Odontogram for History {historia_id}", size=20, weight="bold"),
        ft.Text("Visualización interactiva del odontograma pendiente de implementar."),
        ft.ElevatedButton("Guardar Cambios", on_click=lambda e: print(f"Odontograma para {historia_id} guardado"))
    ])
