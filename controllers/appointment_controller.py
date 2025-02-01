from models.appointment import AppointmentModel

class AppointmentController:
    def __init__(self):
        self.model = AppointmentModel()

    def load_patients(self):
        return self.model.load_patients()

    def load_doctors(self):
        return self.model.load_doctors()

    def load_appointments(self, date=None, doctor_id=None, status=None):
        return self.model.load_appointments(date, doctor_id, status)

    def get_appointment_by_id(self, appointment_id):
        return self.model.get_appointment_by_id(appointment_id)

    def save_appointment(self, appointment_id, data):
        if appointment_id:
            self.model.update_appointment(appointment_id, data)
        else:
            self.model.add_appointment(data)

    def delete_appointment(self, appointment_id):
        self.model.delete_appointment(appointment_id)
