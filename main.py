import flet as ft
from database.db_config import create_tables
from modules.login import login_view
from controllers.menu_controller import MenuController
from modules.odontogram import odontogram_view

def main(page: ft.Page):
    page.title = "OdontoClinic"

    # Inicializar el controlador del menú
    menu_controller = MenuController(page)

    # -------------------------
    # Vistas de login y rutas básicas
    # -------------------------
    def show_login_view():
        page.views.append(
            ft.View("/", controls=[login_view(page, lambda user: page.go("/menu"))])
        )
        page.update()

    # Vista para odontograma (ruta independiente)
    def show_odontogram_view():
        try:
            patient_id = int(page.route.split("/")[-1])
            page.views.append(
                ft.View(
                    f"/odontogram/{patient_id}",
                    controls=[
                        odontogram_view(page, patient_id),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu"))
                    ]
                )
            )
        except (ValueError, IndexError) as e:
            page.views.append(
                ft.View("/error", controls=[ft.Text(f"Invalid patient ID: {str(e)}", color="red")])
            )
        page.update()

    def show_404_view():
        page.views.append(
            ft.View("/404", controls=[ft.Text("Page not found", size=30, color="red")])
        )
        page.update()

    # -------------------------
    # Manejo de rutas
    # -------------------------
    routes = {
        "/": show_login_view,
        "/menu": menu_controller.show_menu_view,
        "/odontogram": show_odontogram_view,
    }

    def route_change(route):
        page.views.clear()
        handler = routes.get(page.route, show_404_view)
        handler() if callable(handler) else handler
        page.update()

    page.on_route_change = route_change

    # Crear la base de datos (si no existe)
    create_tables()
    page.go("/")

ft.app(target=main)