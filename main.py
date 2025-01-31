import flet as ft
from database.db_config import create_tables
from modules.login import login_view
from modules.appointments import appointments_view
from modules.patients import patients_view, load_patients
from modules.history import history_view
from modules.doctors import doctors_view
from modules.inventory import inventory_view
from modules.payments import payments_view
from modules.odontogram import odontogram_view
from modules.insurance import insurance_view
from modules.prescriptions import prescriptions_view
from modules.invoices import invoices_view
from modules.feedback import feedback_view
from modules.doctor_schedules import doctor_schedules_view
from modules.hr import hr_view

def main(page: ft.Page):
    page.title = "OdontoClinic"

    def show_login_view():
        page.views.append(
            ft.View("/", controls=[login_view(page, lambda user: page.go("/menu"))])
        )

    def show_menu_view():
        dynamic_content = ft.Column([ft.Text("Selecciona una opción del menú.")], expand=True, scroll=ft.ScrollMode.AUTO)

        def update_content(index):
            if index == 2:  # Medical History
                setup_medical_history_view(dynamic_content)
            elif index == 6:  # Odontogram
                setup_odontogram_view(dynamic_content)
            else:
                setup_general_view(dynamic_content, index)
            page.update()

        rail = create_navigation_rail(update_content)

        page.views.append(
            ft.View(
                "/menu",
                controls=[
                    ft.Row([
                        rail,
                        ft.VerticalDivider(width=1),
                        dynamic_content,
                    ], expand=True),
                ]
            )
        )
        page.update()

    def setup_medical_history_view(dynamic_content):
        try:
            patients = load_patients()
            patient_dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(str(pt[0]), text=pt[1]) for pt in patients],
                label="Select a Patient"
            )
            dynamic_content.controls = [
                ft.Text("Medical History", size=20, weight="bold"),
                patient_dropdown,
                ft.ElevatedButton(
                    "View Medical History",
                    on_click=lambda _: page.go(f"/history/{patient_dropdown.value}") if patient_dropdown.value else None
                ),
            ]
        except Exception as e:
            dynamic_content.controls = [ft.Text(f"Error loading patients: {str(e)}", color="red")]

    def setup_odontogram_view(dynamic_content):
        try:
            patients = load_patients()
            patient_dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(str(pt[0]), text=pt[1]) for pt in patients],
                label="Select a Patient"
            )
            dynamic_content.controls = [
                ft.Text("Odontogram", size=20, weight="bold"),
                patient_dropdown,
                ft.ElevatedButton(
                    "View Odontogram",
                    on_click=lambda _: page.go(f"/odontogram/{patient_dropdown.value}") if patient_dropdown.value else None
                ),
            ]
        except Exception as e:
            dynamic_content.controls = [ft.Text(f"Error loading patients: {str(e)}", color="red")]

    def setup_general_view(dynamic_content, index):
        views = [
            ("Appointments", appointments_view(page)),
            ("Patients", patients_view(page)),
            ("Medical History", history_view(page, None)),
            ("Doctors", doctors_view(page)),
            ("Inventory", inventory_view(page)),
            ("Payments & Invoices", ft.Column([payments_view(page), invoices_view(page)])),
            ("Odontogram", odontogram_view(page, None)),
            ("Insurance", insurance_view(page)),
            ("Prescriptions", prescriptions_view(page)),
            ("Patient Feedback", feedback_view(page)),
            ("Doctor Schedules", doctor_schedules_view(page)),
            ("HR Management", hr_view(page)),
        ]
        dynamic_content.controls = [
            ft.Text(views[index][0], size=20, weight="bold"),
            views[index][1]
        ]

    def create_navigation_rail(update_content):
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=100,
            leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.EVENT, label="Appointments"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Patients"),
                ft.NavigationRailDestination(icon=ft.Icons.HISTORY, label="History"),
                ft.NavigationRailDestination(icon=ft.Icons.LOCAL_HOSPITAL, label="Doctors"),
                ft.NavigationRailDestination(icon=ft.Icons.INVENTORY, label="Inventory"),
                ft.NavigationRailDestination(icon=ft.Icons.PAYMENT, label="Payments & Invoices"),
                ft.NavigationRailDestination(icon=ft.Icons.MEDICAL_SERVICES, label="Odontogram"),
                ft.NavigationRailDestination(icon=ft.Icons.SECURITY, label="Insurance"),
                ft.NavigationRailDestination(icon=ft.Icons.MEDICATION, label="Prescriptions"),
                ft.NavigationRailDestination(icon=ft.Icons.STAR, label="Feedback"),
                ft.NavigationRailDestination(icon=ft.Icons.SCHEDULE, label="Doctor Schedules"),
                ft.NavigationRailDestination(icon=ft.Icons.WORK, label="HR Management"),
            ],
            on_change=lambda e: update_content(e.control.selected_index),
        )

    def show_odontogram_view():
        try:
            patient_id = int(page.route.split("/")[-1])
            page.views.append(
                ft.View(
                    f"/odontogram/{patient_id}",
                    controls=[
                        odontogram_view(page, patient_id),
                        ft.ElevatedButton("Back to Menu", on_click=lambda _: page.go("/menu")),
                    ]
                )
            )
        except (ValueError, IndexError) as e:
            page.views.append(
                ft.View(
                    "/error",
                    controls=[ft.Text(f"Invalid patient ID: {str(e)}", color="red")]
                )
            )

    def show_404_view():
        page.views.append(
            ft.View(
                "/404",
                controls=[ft.Text("Page not found", size=30, color="red")]
            )
        )

    # Definir el diccionario de rutas después de que todas las funciones estén definidas
    routes = {
        "/": show_login_view,
        "/menu": show_menu_view,
        "/odontogram": show_odontogram_view,
    }

    def route_change(route):
        page.views.clear()
        handler = routes.get(page.route, show_404_view)  # Manejo de rutas no válidas
        handler()
        page.update()

    page.on_route_change = route_change
    create_tables()
    page.go("/")

ft.app(target=main)