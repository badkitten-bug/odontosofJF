import flet as ft
from database.db_config import create_tables
from modules.login import login_view
from modules.appointments import appointments_view
from modules.patients import patients_view, load_patients  # Importar load_patients
from modules.history import history_view
from modules.doctors import doctors_view

def main(page: ft.Page):
    page.title = "OdontoClinic"

    # Función para manejar cambios de ruta
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            # Vista de Login
            page.views.append(
                ft.View(
                    "/",
                    controls=[login_view(page, lambda user: page.go("/menu"))]
                )
            )
        elif page.route == "/menu":
            # Contenido dinámico de la columna derecha
            dynamic_content = ft.Column([ft.Text("Selecciona una opción del menú.")], expand=True)

            # Menú desplegable para Configuration
            config_menu = ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Subopción 1", on_click=lambda _: print("Subopción 1 seleccionada")),
                    ft.PopupMenuItem(text="Subopción 2", on_click=lambda _: print("Subopción 2 seleccionada")),
                ],
                offset=ft.Offset(1, 0),  # Desplazar el menú hacia la derecha
            )
            
            # Función para actualizar el contenido dinámico
            def update_content(index):
                if index == 0:
                    appointments_form = appointments_view(page, only_form=True)
                    appointments_table = appointments_view(page, only_table=True)
                    dynamic_content.controls = [
                        ft.Text("Appointments", size=20, weight="bold"),
                        ft.Column(
                            [
                                appointments_form,
                                appointments_table,
                            ],
                            scroll=True,  # Habilitar scroll solo en esta vista
                            expand=True,
                        ),
                    ]
                elif index == 1:
                    dynamic_content.controls = [
                        ft.Text("Patients", size=20, weight="bold"),
                        patients_view(page),
                    ]
                elif index == 2:
                    patients = load_patients()
                    patient_dropdown = ft.Dropdown(
                        options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
                        label="Select a Patient"
                    )
                    dynamic_content.controls = [
                        ft.Text("Medical History", size=20, weight="bold"),
                        patient_dropdown,
                        ft.ElevatedButton(
                            "View Medical History",
                            on_click=lambda _: page.go(f"/history/{patient_dropdown.value}")
                        ),
                    ]
                elif index == 3:  # Nueva opción para Doctors
                    dynamic_content.controls = [
                        ft.Text("Doctors", size=20, weight="bold"),
                        ft.ElevatedButton(
                            "Manage Doctors",
                            on_click=lambda _: page.go("/doctors")  # Navegar a la vista de Doctors
                        ),
                    ]
                page.update()  # Actualizar la página después de cambiar el contenido

            rail = ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=100,
                min_extended_width=100,
                leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
                group_alignment=-0.9,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="Appointments"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                        selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                        label="Patients",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.SETTINGS_OUTLINED,
                        selected_icon=ft.Icon(ft.Icons.SETTINGS),
                        label_content=ft.Text("History"),
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.PEOPLE_OUTLINE,  # Icono para Doctors
                        selected_icon=ft.Icon(ft.Icons.PEOPLE),
                        label="Doctors",  # Etiqueta para Doctors
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.Icons.SETTINGS_OUTLINED,
                        selected_icon=ft.Icon(ft.Icons.SETTINGS),
                        label_content=config_menu,  # Menú desplegable para Configuration
                    ),
                ],
                on_change=lambda e: update_content(e.control.selected_index),  # Actualizar contenido dinámico
            )

            # Menú Principal
            page.views.append(
                ft.View(
                    "/menu",
                    controls=[
                        ft.Row(
                            [
                                rail,
                                ft.VerticalDivider(width=1),
                                dynamic_content,  # Columna derecha con contenido dinámico
                            ],
                            expand=True,
                        ),
                    ]
                )
            )
            page.update()  # Asegurarse de que la vista se actualice
        elif page.route.startswith("/history/"):
            # Historia Clínica de un Paciente
            patient_id = int(page.route.split("/")[-1])  # Extraer el ID del paciente
            page.views.append(
                ft.View(
                    f"/history/{patient_id}",
                    controls=[
                        history_view(page, patient_id),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu")),
                    ]
                )
            )
        elif page.route == "/doctors":
            # Gestión de Doctores
            page.views.append(
                ft.View(
                    "/doctors",
                    controls=[
                        doctors_view(page),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu")),
                    ]
                )
            )

        page.update()

    page.on_route_change = route_change
    create_tables()
    page.go("/")  # Ruta inicial

ft.app(target=main)