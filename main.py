import flet as ft
from database.db_config import create_tables
from controllers.menu_controller import MenuController

def main(page: ft.Page):
    page.title = "OdontoClinic"
    page.scroll = ft.ScrollMode.AUTO

    # Crear la base de datos si no existe
    create_tables()

    # Inicializar el controlador del menú
    menu_controller = MenuController(page)

    # Configurar el manejo de rutas
    def route_change(route):
        """Manejo dinámico de las rutas en la aplicación."""
        page.views.clear()

        # Ruta del menú principal
        if page.route == "/menu":
            menu_controller.show_menu_view()
        else:
            # Redirigir a la página 404 si la ruta no existe
            page.views.append(
                ft.View(
                    "/404",
                    controls=[ft.Text("Página no encontrada", size=30, color="red")],
                )
            )
        page.update()

    page.on_route_change = route_change

    # Cargar el menú al iniciar
    page.go("/menu")

ft.app(target=main)
