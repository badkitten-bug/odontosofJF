from models.appointment_model import AppointmentModel

class AppointmentController:
    def __init__(self):
        self.model = AppointmentModel()

    def load_patients(self):
        return self.model.load_patients()

    def load_doctors(self):
        return self.model.load_doctors()

    def load_specialties(self):
        return self.model.load_specialties()
    
    def load_appointment_statuses(self):
        return self.model.load_appointment_statuses()

    def load_appointments(self, date=None, doctor_id=None, specialty_id=None, status=None):
        return self.model.load_appointments(date, doctor_id, specialty_id, status)
    
    def load_available_slots(self, date, doctor_id):
        return self.model.load_available_slots(date, doctor_id)

    def create_appointment(self, data):
        self.model.create_appointment(data)

    def save_appointment(self, appointment_id, data):
        if appointment_id:
            self.model.update_appointment(appointment_id, data)
        else:
            self.model.add_appointment(data)

    def get_appointment_by_id(self, appointment_id):
        return self.model.get_appointment_by_id(appointment_id)

    def delete_appointment(self, appointment_id):
        self.model.delete_appointment(appointment_id)
    
    # Nuevo método para cargar doctores por especialidad
    def load_doctors_by_specialty(self, specialty_id):
        return self.model.load_doctors_by_specialty(specialty_id)

    def get_doctor_schedule(self, doctor_id, day_of_week):
        return self.model.get_doctor_schedule(doctor_id, day_of_week)

    def get_booked_slots(self, doctor_id, date):
        return self.model.get_booked_slots(doctor_id, date)
