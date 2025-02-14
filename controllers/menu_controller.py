import flet as ft
from views.patient_view import patients_view
from views.doctor_view import doctors_view
from views.appointment_schedule_view import appointment_schedule_view
from views.appointment_management_view import appointment_management_view
from views.specialty_view import specialty_view
from views.treatment_materials_view import treatment_materials_view
from views.history_management_view import history_management_view  # Corrección de importación

class MenuController:
    def __init__(self, page: ft.Page):
        self.page = page

    def show_menu_view(self):
        """Vista principal del menú lateral con contenido dinámico."""

        dynamic_content = ft.Column(
            [ft.Text("Selecciona una opción del menú.", size=20)],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        def update_content(index: int):
            mapping = {
                0: lambda: self.show_patients_view(dynamic_content),
                1: lambda: self.show_doctors_view(dynamic_content),
                2: lambda: self.show_appointments_menu(dynamic_content),
                3: lambda: self.show_treatments_view(dynamic_content),
                4: lambda: self.show_history_management_view(dynamic_content),  # Uso de la vista corregida
                5: lambda: self.show_catalogs_view(dynamic_content),
            }

            action = mapping.get(index, lambda: dynamic_content.controls.append(ft.Text("Opción no implementada")))
            action()
            self.page.update()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=72,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Pacientes"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Odontólogos"),
                ft.NavigationRailDestination(icon=ft.Icons.EVENT, label="Citas"),
                ft.NavigationRailDestination(icon=ft.Icons.MEDICATION, label="Tratamientos"),
                ft.NavigationRailDestination(icon=ft.Icons.HISTORY, label="Historias Clínicas"),
                ft.NavigationRailDestination(icon=ft.Icons.CATEGORY, label="Catálogos"),
            ],
            on_change=lambda e: update_content(e.control.selected_index),
        )

        self.page.views.append(
            ft.View(
                "/menu",
                controls=[ft.Row([rail, ft.VerticalDivider(width=1), dynamic_content], expand=True)],
            )
        )
        self.page.update()

    def show_patients_view(self, dynamic_content: ft.Column):
        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Pacientes", size=20, weight="bold"))
        dynamic_content.controls.append(patients_view(self.page))
        self.page.update()

    def show_doctors_view(self, dynamic_content: ft.Column):
        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Odontólogos", size=20, weight="bold"))
        dynamic_content.controls.append(doctors_view(self.page))
        self.page.update()

    def show_appointments_menu(self, dynamic_content: ft.Column):
        def load_schedule_view():
            dynamic_content.controls.clear()
            dynamic_content.controls.append(ft.Text("Agendar Citas", size=20, weight="bold"))
            dynamic_content.controls.append(appointment_schedule_view(self.page))
            self.page.update()

        def load_management_view():
            dynamic_content.controls.clear()
            dynamic_content.controls.append(ft.Text("Gestión de Citas", size=20, weight="bold"))
            dynamic_content.controls.append(appointment_management_view(self.page))
            self.page.update()

        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Opciones de Citas", size=20, weight="bold"))
        dynamic_content.controls.append(ft.ElevatedButton("Agendar Citas", on_click=lambda _: load_schedule_view()))
        dynamic_content.controls.append(ft.ElevatedButton("Gestionar Citas", on_click=lambda _: load_management_view()))
        self.page.update()

    def show_treatments_view(self, dynamic_content: ft.Column):
        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Gestión de Tratamientos", size=20, weight="bold"))
        dynamic_content.controls.append(treatment_materials_view(self.page))
        self.page.update()

    def show_history_management_view(self, dynamic_content: ft.Column):
        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Historias Clínicas", size=20, weight="bold"))
        dynamic_content.controls.append(history_management_view(self.page))
        self.page.update()

    def show_catalogs_view(self, dynamic_content: ft.Column):
        def load_specialties():
            dynamic_content.controls.clear()
            dynamic_content.controls.append(ft.Text("Gestión de Especialidades", size=20, weight="bold"))
            dynamic_content.controls.append(specialty_view(self.page))
            self.page.update()

        def load_treatments():
            dynamic_content.controls.clear()
            dynamic_content.controls.append(ft.Text("Gestión de Tratamientos", size=20, weight="bold"))
            dynamic_content.controls.append(treatment_materials_view(self.page))
            self.page.update()
        
        def load_doctor_schedules():
            dynamic_content.controls.clear()
            dynamic_content.controls.append(ft.Text("Gestión de Horarios de Doctores", size=20, weight="bold"))
            from views.doctor_schedule_view import doctor_schedule_view
            dynamic_content.controls.append(doctor_schedule_view(self.page))
            self.page.update()

        dynamic_content.controls.clear()
        dynamic_content.controls.append(ft.Text("Opciones de Catálogos", size=20, weight="bold"))
        dynamic_content.controls.append(ft.ElevatedButton("Gestión de Especialidades", on_click=lambda _: load_specialties()))
        dynamic_content.controls.append(ft.ElevatedButton("Gestión de Tratamientos", on_click=lambda _: load_treatments()))
        dynamic_content.controls.append(ft.ElevatedButton("Gestión de Horarios de Doctores", on_click=lambda _: load_doctor_schedules()))
        self.page.update()