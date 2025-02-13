from models.doctor_model import DoctorModel

class DoctorController:
    def __init__(self):
        self.model = DoctorModel()

    def load_doctors(self):
        return self.model.load_doctors()

    def get_doctor_by_id(self, doctor_id):
        return self.model.get_doctor_by_id(doctor_id)

    def add_doctor(self, data):
        self.model.add_doctor(data)

    def update_doctor(self, doctor_id, data):
        self.model.update_doctor(doctor_id, data)

    def delete_doctor(self, doctor_id):
        self.model.delete_doctor(doctor_id)

    def load_specialties(self):
        return self.model.load_specialties()

    def load_doctor_types(self):
        return self.model.load_doctor_types()

    def load_document_types(self):
        return self.model.load_document_types()