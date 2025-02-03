import flet as ft
from views.patient_view import patients_view
from views.doctor_view import doctors_view
from views.appointment_view import appointments_view
from views.specialty_view import specialty_view
from views.historia_view import historia_view

class MenuController:
    def __init__(self, page: ft.Page):
        self.page = page

    # -------------------------
    # Vistas principales
    # -------------------------
    def show_registro_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Registro", size=20, weight="bold"),
            ft.ElevatedButton("Paciente", on_click=lambda _: self.show_patients_view(dc)),
            ft.ElevatedButton("Odontólogo", on_click=lambda _: self.show_doctors_view(dc))
        ]
        self.page.update()

    def show_patients_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Registro de Pacientes", size=20, weight="bold"),
            patients_view(self.page)
        ]
        self.page.update()

    def show_doctors_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Registro de Odontólogos", size=20, weight="bold"),
            doctors_view(self.page)
        ]
        self.page.update()

    def show_citas_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Citas", size=20, weight="bold"),
            appointments_view(self.page)
        ]
        self.page.update()

    def show_historia_clinica_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Historia Clínica - Movimiento", size=20, weight="bold"),
            historia_view(self.page)
        ]
        self.page.update()

    def show_specialty_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Gestión de Especialidades", size=20, weight="bold"),
            specialty_view(self.page)
        ]
        self.page.update()

    def show_tratamientos_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tratamientos", size=20, weight="bold"),
            ft.ElevatedButton("Registrar", on_click=lambda _: self.treatments_register_view(dc)),
            ft.ElevatedButton("Comprobantes", on_click=lambda _: self.treatments_comprobantes_view(dc))
        ]
        self.page.update()

    def treatments_register_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Registrar Tratamiento", size=20, weight="bold"),
            ft.Text("Formulario para registrar tratamiento...")
        ]
        self.page.update()

    def treatments_comprobantes_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Comprobantes de Tratamientos", size=20, weight="bold"),
            ft.Text("Vista de comprobantes...")
        ]
        self.page.update()

    def show_reportes_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Reportes", size=20, weight="bold"),
            ft.ElevatedButton("Tratamientos Cobrados", on_click=lambda _: self.reportes_tratamientos_cobrados_view(dc))
        ]
        self.page.update()

    def reportes_tratamientos_cobrados_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tratamientos Cobrados", size=20, weight="bold"),
            ft.Text("Vista de tratamientos cobrados...")
        ]
        self.page.update()

    def show_procedimientos_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Procedimientos", size=20, weight="bold"),
            ft.ElevatedButton("Tarifario", on_click=lambda _: self.procedimientos_tarifario_view(dc)),
            ft.ElevatedButton("Diagnóstico", on_click=lambda _: self.procedimientos_diagnostico_view(dc))
        ]
        self.page.update()

    def procedimientos_tarifario_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tarifario", size=20, weight="bold"),
            ft.Text("Vista del tarifario...")
        ]
        self.page.update()

    def procedimientos_diagnostico_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Diagnóstico", size=20, weight="bold"),
            ft.Text("Vista de diagnóstico...")
        ]
        self.page.update()

    def show_mantenimiento_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Mantenimiento", size=20, weight="bold"),
            ft.ElevatedButton("Tipo pago", on_click=lambda _: self.mantenimiento_tipo_pago_view(dc)),
            ft.ElevatedButton("Moneda", on_click=lambda _: self.mantenimiento_moneda_view(dc)),
            ft.ElevatedButton("Banco", on_click=lambda _: self.mantenimiento_banco_view(dc)),
            ft.ElevatedButton("Tipo tarjeta", on_click=lambda _: self.mantenimiento_tipo_tarjeta_view(dc))
        ]
        self.page.update()

    def mantenimiento_tipo_pago_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Pago", size=20, weight="bold"),
            ft.Text("Vista de tipo de pago...")
        ]
        self.page.update()

    def mantenimiento_moneda_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Moneda", size=20, weight="bold"),
            ft.Text("Vista de moneda...")
        ]
        self.page.update()

    def mantenimiento_banco_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Banco", size=20, weight="bold"),
            ft.Text("Vista de banco...")
        ]
        self.page.update()

    def mantenimiento_tipo_tarjeta_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Tarjeta", size=20, weight="bold"),
            ft.Text("Vista de tipo de tarjeta...")
        ]
        self.page.update()

    def show_catalogo_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Catálogo", size=20, weight="bold"),
            ft.ElevatedButton("Unidad medida", on_click=lambda _: self.catalogo_unidad_medida_view(dc)),
            ft.ElevatedButton("Tipo concepto", on_click=lambda _: self.catalogo_tipo_concepto_view(dc)),
            ft.ElevatedButton("Categoría", on_click=lambda _: self.catalogo_categoria_view(dc)),
            ft.ElevatedButton("Especialidad", on_click=lambda _: self.catalogo_especialidad_view(dc)),
            ft.ElevatedButton("Especialidades", on_click=lambda _: self.show_specialty_view(dc)),
            ft.ElevatedButton("Tipo citado", on_click=lambda _: self.catalogo_tipo_citado_view(dc)),
            ft.ElevatedButton("Alergia", on_click=lambda _: self.catalogo_alergia_view(dc))
        ]
        self.page.update()

    def catalogo_unidad_medida_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Unidad de Medida", size=20, weight="bold"),
            ft.Text("Vista de unidad de medida...")
        ]
        self.page.update()

    def catalogo_tipo_concepto_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Concepto", size=20, weight="bold"),
            ft.Text("Vista de tipo de concepto...")
        ]
        self.page.update()

    def catalogo_categoria_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Categoría", size=20, weight="bold"),
            ft.Text("Vista de categoría...")
        ]
        self.page.update()

    def catalogo_especialidad_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Especialidad", size=20, weight="bold"),
            ft.Text("Vista de especialidad...")
        ]
        self.page.update()

    def catalogo_tipo_citado_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Citado", size=20, weight="bold"),
            ft.Text("Vista de tipo de citado...")
        ]
        self.page.update()

    def catalogo_alergia_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Alergia", size=20, weight="bold"),
            ft.Text("Vista de alergia...")
        ]
        self.page.update()

    def show_gestion_usuarios_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Gestión de Usuarios", size=20, weight="bold"),
            ft.ElevatedButton("Usuarios", on_click=lambda _: self.usuarios_view(dc)),
            ft.ElevatedButton("Roles", on_click=lambda _: self.roles_view(dc)),
            ft.ElevatedButton("Permisos", on_click=lambda _: self.permisos_view(dc))
        ]
        self.page.update()

    def usuarios_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Usuarios", size=20, weight="bold"),
            ft.Text("Vista de usuarios...")
        ]
        self.page.update()

    def roles_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Roles", size=20, weight="bold"),
            ft.Text("Vista de roles...")
        ]
        self.page.update()

    def permisos_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Permisos", size=20, weight="bold"),
            ft.Text("Vista de permisos...")
        ]
        self.page.update()

    def show_configuracion_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Configuración", size=20, weight="bold"),
            ft.ElevatedButton("Mi Clínica", on_click=lambda _: self.clinica_view(dc)),
            ft.ElevatedButton("Tipo documento", on_click=lambda _: self.tipo_documento_view(dc))
        ]
        self.page.update()

    def clinica_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Mi Clínica", size=20, weight="bold"),
            ft.Text("Vista de configuración de la clínica...")
        ]
        self.page.update()

    def tipo_documento_view(self, dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo Documento", size=20, weight="bold"),
            ft.Text("Vista de tipos de documento...")
        ]
        self.page.update()

    # -------------------------
    # Vista principal del menú
    # -------------------------
    def show_menu_view(self):
        dynamic_content = ft.Column(
            [ft.Text("Selecciona una opción del menú.", size=20)],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        def update_content(index: int):
            mapping = {
                0: lambda dc: self.show_registro_view(dc),
                1: lambda dc: self.show_citas_view(dc),
                2: lambda dc: self.show_tratamientos_view(dc),
                3: lambda dc: self.show_historia_clinica_view(dc),
                4: lambda dc: self.show_reportes_view(dc),
                5: lambda dc: self.show_procedimientos_view(dc),
                6: lambda dc: self.show_mantenimiento_view(dc),
                7: lambda dc: self.show_catalogo_view(dc),
                8: lambda dc: self.show_gestion_usuarios_view(dc),
                9: lambda dc: self.show_configuracion_view(dc),
            }
            mapping.get(index, lambda dc: dc.controls.append(ft.Text("Opción no implementada", size=20)))(dynamic_content)
            self.page.update()

        rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=120,
            min_extended_width=150,
            leading=ft.FloatingActionButton(icon=ft.Icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(icon=ft.Icons.CREATE, label="Registro"),
                ft.NavigationRailDestination(icon=ft.Icons.EVENT, label="Citas"),
                ft.NavigationRailDestination(icon=ft.Icons.MEDICATION, label="Tratamientos"),
                ft.NavigationRailDestination(icon=ft.Icons.HISTORY, label="Historia"),
                ft.NavigationRailDestination(icon=ft.Icons.PAYMENT, label="Reportes"),
                ft.NavigationRailDestination(icon=ft.Icons.DESCRIPTION, label="Procedimientos"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Mantenimiento"),
                ft.NavigationRailDestination(icon=ft.Icons.CATEGORY, label="Catálogo"),
                ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Gestión"),
                ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Configuración"),
            ],
            on_change=lambda e: update_content(e.control.selected_index),
        )

        self.page.views.append(
            ft.View("/menu", controls=[ft.Row([rail, ft.VerticalDivider(width=1), dynamic_content], expand=True)])
        )
        self.page.update()