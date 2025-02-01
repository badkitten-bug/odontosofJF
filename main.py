import flet as ft
from database.db_config import create_tables
from modules.login import login_view
# Importa la vista de citas del MVC (ya refactorizado)
from views.appointment_view import appointments_view
from modules.history import history_view
# Importa la vista de odontólogos refactorizada a MVC:
from views.doctor_view import doctors_view
from modules.inventory import inventory_view
from modules.payments import payments_view
from modules.odontogram import odontogram_view
from modules.insurance import insurance_view
from modules.prescriptions import prescriptions_view
from modules.invoices import invoices_view
from modules.feedback import feedback_view
from modules.doctor_schedules import doctor_schedules_view
from modules.hr import hr_view

# Importa la función de vista de pacientes definida en el MVC (views/patient_view.py)
from views.patient_view import patients_view

def main(page: ft.Page):
    page.title = "OdontoClinic"

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
    # Vistas del menú principal y subvistas
    # Cada función recibe "dc" (dynamic_content) para actualizar su contenido.
    # -------------------------
    def show_registro_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Registro", size=20, weight="bold"),
            ft.ElevatedButton("Paciente", on_click=lambda _: show_patients_view(dc)),
            ft.ElevatedButton("Odontólogo", on_click=lambda _: show_doctors_view(dc))
        ]
        page.update()

    def show_patients_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Registro de Pacientes", size=20, weight="bold"),
            patients_view(page)
        ]
        page.update()

    def show_doctors_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Registro de Odontólogos", size=20, weight="bold"),
            doctors_view(page)
        ]
        page.update()

    def show_citas_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Citas", size=20, weight="bold"),
            # Se utiliza la vista de citas refactorizada a MVC
            appointments_view(page)
        ]
        page.update()

    def appointments_register_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Registrar Cita", size=20, weight="bold"),
            ft.Text("Formulario para registrar cita...")
        ]
        page.update()

    def show_tratamientos_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tratamientos", size=20, weight="bold"),
            ft.ElevatedButton("Registrar", on_click=lambda _: treatments_register_view(dc)),
            ft.ElevatedButton("Comprobantes", on_click=lambda _: treatments_comprobantes_view(dc))
        ]
        page.update()

    def treatments_register_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Registrar Tratamiento", size=20, weight="bold"),
            ft.Text("Formulario para registrar tratamiento...")
        ]
        page.update()

    def treatments_comprobantes_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Comprobantes de Tratamientos", size=20, weight="bold"),
            ft.Text("Vista de comprobantes...")
        ]
        page.update()

    def show_historia_clinica_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Historia Clínica - Movimiento", size=20, weight="bold"),
            ft.Text("Vista de movimiento de la historia clínica...")
        ]
        page.update()

    def show_reportes_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Reportes", size=20, weight="bold"),
            ft.ElevatedButton("Tratamientos Cobrados", on_click=lambda _: reportes_tratamientos_cobrados_view(dc))
        ]
        page.update()

    def reportes_tratamientos_cobrados_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tratamientos Cobrados", size=20, weight="bold"),
            ft.Text("Vista de tratamientos cobrados...")
        ]
        page.update()

    def show_procedimientos_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Procedimientos", size=20, weight="bold"),
            ft.ElevatedButton("Tarifario", on_click=lambda _: procedimientos_tarifario_view(dc)),
            ft.ElevatedButton("Diagnóstico", on_click=lambda _: procedimientos_diagnostico_view(dc))
        ]
        page.update()

    def procedimientos_tarifario_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tarifario", size=20, weight="bold"),
            ft.Text("Vista del tarifario...")
        ]
        page.update()

    def procedimientos_diagnostico_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Diagnóstico", size=20, weight="bold"),
            ft.Text("Vista de diagnóstico...")
        ]
        page.update()

    def show_mantenimiento_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Mantenimiento", size=20, weight="bold"),
            ft.ElevatedButton("Tipo pago", on_click=lambda _: mantenimiento_tipo_pago_view(dc)),
            ft.ElevatedButton("Moneda", on_click=lambda _: mantenimiento_moneda_view(dc)),
            ft.ElevatedButton("Banco", on_click=lambda _: mantenimiento_banco_view(dc)),
            ft.ElevatedButton("Tipo tarjeta", on_click=lambda _: mantenimiento_tipo_tarjeta_view(dc))
        ]
        page.update()

    def mantenimiento_tipo_pago_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Pago", size=20, weight="bold"),
            ft.Text("Vista de tipo de pago...")
        ]
        page.update()

    def mantenimiento_moneda_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Moneda", size=20, weight="bold"),
            ft.Text("Vista de moneda...")
        ]
        page.update()

    def mantenimiento_banco_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Banco", size=20, weight="bold"),
            ft.Text("Vista de banco...")
        ]
        page.update()

    def mantenimiento_tipo_tarjeta_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Tarjeta", size=20, weight="bold"),
            ft.Text("Vista de tipo de tarjeta...")
        ]
        page.update()

    def show_catalogo_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Catálogo", size=20, weight="bold"),
            ft.ElevatedButton("Unidad medida", on_click=lambda _: catalogo_unidad_medida_view(dc)),
            ft.ElevatedButton("Tipo concepto", on_click=lambda _: catalogo_tipo_concepto_view(dc)),
            ft.ElevatedButton("Categoría", on_click=lambda _: catalogo_categoria_view(dc)),
            ft.ElevatedButton("Especialidad", on_click=lambda _: catalogo_especialidad_view(dc)),
            ft.ElevatedButton("Tipo citado", on_click=lambda _: catalogo_tipo_citado_view(dc)),
            ft.ElevatedButton("Alergia", on_click=lambda _: catalogo_alergia_view(dc))
        ]
        page.update()

    def catalogo_unidad_medida_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Unidad de Medida", size=20, weight="bold"),
            ft.Text("Vista de unidad de medida...")
        ]
        page.update()

    def catalogo_tipo_concepto_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Concepto", size=20, weight="bold"),
            ft.Text("Vista de tipo de concepto...")
        ]
        page.update()

    def catalogo_categoria_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Categoría", size=20, weight="bold"),
            ft.Text("Vista de categoría...")
        ]
        page.update()

    def catalogo_especialidad_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Especialidad", size=20, weight="bold"),
            ft.Text("Vista de especialidad...")
        ]
        page.update()

    def catalogo_tipo_citado_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo de Citado", size=20, weight="bold"),
            ft.Text("Vista de tipo de citado...")
        ]
        page.update()

    def catalogo_alergia_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Alergia", size=20, weight="bold"),
            ft.Text("Vista de alergia...")
        ]
        page.update()

    def show_gestion_usuarios_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Gestión de Usuarios", size=20, weight="bold"),
            ft.ElevatedButton("Usuarios", on_click=lambda _: usuarios_view(dc)),
            ft.ElevatedButton("Roles", on_click=lambda _: roles_view(dc)),
            ft.ElevatedButton("Permisos", on_click=lambda _: permisos_view(dc))
        ]
        page.update()

    def usuarios_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Usuarios", size=20, weight="bold"),
            ft.Text("Vista de usuarios...")
        ]
        page.update()

    def roles_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Roles", size=20, weight="bold"),
            ft.Text("Vista de roles...")
        ]
        page.update()

    def permisos_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Permisos", size=20, weight="bold"),
            ft.Text("Vista de permisos...")
        ]
        page.update()

    def show_configuracion_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Configuración", size=20, weight="bold"),
            ft.ElevatedButton("Mi Clínica", on_click=lambda _: clinica_view(dc)),
            ft.ElevatedButton("Tipo documento", on_click=lambda _: tipo_documento_view(dc))
        ]
        page.update()

    def clinica_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Mi Clínica", size=20, weight="bold"),
            ft.Text("Vista de configuración de la clínica...")
        ]
        page.update()

    def tipo_documento_view(dc: ft.Column):
        dc.controls = [
            ft.Text("Tipo Documento", size=20, weight="bold"),
            ft.Text("Vista de tipos de documento...")
        ]
        page.update()

    # -------------------------
    # Vista principal del menú
    # Se encapsula la actualización del contenido usando un diccionario de funciones.
    # -------------------------
    def show_menu_view():
        dynamic_content = ft.Column(
            [ft.Text("Selecciona una opción del menú.", size=20)],
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        def update_content(index: int):
            mapping = {
                0: show_registro_view,
                1: show_citas_view,
                2: show_tratamientos_view,
                3: show_historia_clinica_view,
                4: show_reportes_view,
                5: show_procedimientos_view,
                6: show_mantenimiento_view,
                7: show_catalogo_view,
                8: show_gestion_usuarios_view,
                9: show_configuracion_view,
            }
            mapping.get(index, lambda dc: dc.controls.append(ft.Text("Opción no implementada", size=20)))(dynamic_content)
            page.update()

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

        page.views.append(
            ft.View("/menu", controls=[ft.Row([rail, ft.VerticalDivider(width=1), dynamic_content], expand=True)])
        )
        page.update()

    # -------------------------
    # Manejo de rutas
    # -------------------------
    routes = {
        "/": show_login_view,
        "/menu": show_menu_view,
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
