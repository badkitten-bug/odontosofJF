from models.patient import PatientModel

class PatientController:
    def __init__(self):
        self.model = PatientModel()

    def load_patients(self):
        return self.model.load_patients()

    def add_patient(self, data):
        self.model.add_patient(data)

    def update_patient(self, patient_id, data):
        self.model.update_patient(patient_id, data)

    def delete_patient(self, patient_id):
        self.model.delete_patient(patient_id)

    def get_patient_by_id(self, patient_id):
        return self.model.get_patient_by_id(patient_id)
