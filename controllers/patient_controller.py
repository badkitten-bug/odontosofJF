from models.patient_model import PatientModel
from models.historia_clinica_model import HistoriaClinicaModel


class PatientController:
    def __init__(self):
        self.model = PatientModel()

    def load_patients(self):
        return self.model.load_patients()

    def get_patient_by_id(self, patient_id):
        return self.model.get_patient_by_id(patient_id)

    def add_patient(self, data):
            """Crea un paciente y su historia clínica asociada."""
            patient_id = self.model.add_patient(data)
            if patient_id:
                HistoriaClinicaModel.create_history_for_patient(patient_id)
            return patient_id

    def update_patient(self, patient_id, data):
        self.model.update_patient(patient_id, data)

    def delete_patient(self, patient_id):
        self.model.delete_patient(patient_id)

    def load_education_levels(self):
        return self.model.load_education_levels()

    def load_marital_statuses(self):
        return self.model.load_marital_statuses()

    def load_document_types(self):
        return self.model.load_document_types()