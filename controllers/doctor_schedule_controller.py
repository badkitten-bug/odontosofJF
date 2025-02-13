from models.doctor_schedule_model import DoctorScheduleModel

class DoctorScheduleController:
    """Controlador para gestionar los horarios de los doctores."""

    def __init__(self):
        self.model = DoctorScheduleModel()

    def add_schedule(self, doctor_id, day_of_week, start_time, end_time):
        """Agrega un horario para un doctor."""
        self.model.add_schedule(doctor_id, day_of_week, start_time, end_time)

    def get_schedules_by_doctor(self, doctor_id):
        """Obtiene los horarios de un doctor."""
        return self.model.get_schedules_by_doctor(doctor_id)

    def delete_schedule(self, schedule_id):
        """Elimina un horario."""
        self.model.delete_schedule(schedule_id)
