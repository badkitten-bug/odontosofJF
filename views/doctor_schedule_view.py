import flet as ft
from controllers.doctor_schedule_controller import DoctorScheduleController
from controllers.doctor_controller import DoctorController  

def doctor_schedule_view(page: ft.Page):
    schedule_controller = DoctorScheduleController()
    doctor_controller = DoctorController()

    doctors = doctor_controller.load_doctors()
    doctor_dropdown = ft.Dropdown(
        label="Seleccionar Doctor",
        options=[ft.dropdown.Option(text=f"{d[1]} {d[2]}", key=d[0]) for d in doctors],
        width=300
    )

    day_dropdown = ft.Dropdown(
        label="Día de la Semana",
        options=[ft.dropdown.Option(day) for day in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]],
        width=200
    )
    start_time_input = ft.TextField(label="Hora de Inicio (HH:MM)", width=150)
    end_time_input = ft.TextField(label="Hora de Fin (HH:MM)", width=150)

    def add_schedule(e):
        if not doctor_dropdown.value or not day_dropdown.value or not start_time_input.value or not end_time_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios", color="red"))
            page.snack_bar.open = True
            return

        schedule_controller.add_schedule(
            doctor_dropdown.value, day_dropdown.value, start_time_input.value, end_time_input.value
        )
        refresh_table()

    def refresh_table():
        if not doctor_dropdown.value:
            return
        schedules = schedule_controller.get_schedules_by_doctor(doctor_dropdown.value)
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(s[1])),
                    ft.DataCell(ft.Text(s[2])),
                    ft.DataCell(ft.Text(s[3])),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.DELETE, on_click=lambda e, id=s[0]: delete_schedule(id))),
                ]
            ) for s in schedules
        ]
        page.update()

    def delete_schedule(schedule_id):
        schedule_controller.delete_schedule(schedule_id)
        refresh_table()

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Día")),
            ft.DataColumn(ft.Text("Hora Inicio")),
            ft.DataColumn(ft.Text("Hora Fin")),
            ft.DataColumn(ft.Text("Opciones")),
        ],
        rows=[]
    )

    doctor_dropdown.on_change = lambda e: refresh_table()

    return ft.Container(
        content=ft.Column([
            ft.Text("Configurar Horarios de Doctores", size=24, weight="bold"),
            ft.Row([doctor_dropdown]),
            ft.Row([day_dropdown, start_time_input, end_time_input]),
            ft.Row([ft.ElevatedButton("Agregar Horario", on_click=add_schedule)]),
            ft.Text("Horarios Asignados:", size=20),
            table
        ]),
        padding=20
    )
