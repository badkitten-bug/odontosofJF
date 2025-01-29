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

            rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE_BORDER, selected_icon=ft.Icons.FAVORITE, label="First"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
                selected_icon=ft.Icon(ft.Icons.BOOKMARK),
                label="Second",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SETTINGS),
                label_content=ft.Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )
            # Menú Principal
            page.views.append(
                ft.View(
                    "/menu",
                    controls=[
                        ft.Text("Main Menu", size=24, weight="bold"),
                        ft.ElevatedButton("Patients", on_click=lambda _: page.go("/patients")),
                        ft.ElevatedButton("Appointments", on_click=lambda _: page.go("/appointments")),
                        ft.ElevatedButton("Medical History", on_click=lambda _: page.go("/history")),
                        ft.ElevatedButton("Doctors", on_click=lambda _: page.go("/doctors")),
                    ]
                )
            )
        elif page.route == "/appointments":
            # Gestión de Citas
            page.views.append(
                ft.View(
                    "/appointments",
                    controls=[
                        ft.Row(
                            [
                                ft.Column([
                                    ft.Text("Register Appointment", size=20, weight="bold"),
                                    appointments_view(page, only_form=True),
                                ], width=300),
                                ft.Column([
                                    ft.Text("Scheduled Appointments", size=20, weight="bold"),
                                    appointments_view(page, only_table=True),
                                ], expand=True),
                            ]
                        ),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu")),
                    ]
                )
            )
        elif page.route == "/patients":
            # Gestión de Pacientes
            page.views.append(
                ft.View(
                    "/patients",
                    controls=[
                        patients_view(page),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu")),
                    ]
                )
            )
        elif page.route == "/history":
            # Vista inicial para seleccionar un paciente
            patients = load_patients()
            patient_dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(str(pt[0]), text=f"{pt[1]} - {pt[2]}") for pt in patients],
                label="Select a Patient"
            )
            go_to_history_button = ft.ElevatedButton(
                "View Medical History",
                on_click=lambda _: page.go(f"/history/{patient_dropdown.value}")
            )
            page.views.append(
                ft.View(
                    "/history",
                    controls=[
                        ft.Text("Medical History", size=24, weight="bold"),
                        patient_dropdown,
                        go_to_history_button,
                    ]
                )
            )
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
