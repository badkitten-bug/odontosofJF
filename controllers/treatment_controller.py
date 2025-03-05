from models.treatment_model import TreatmentModel

class TreatmentController:
    def get_treatments(self):
        """Obtiene todos los tratamientos disponibles."""
        return TreatmentModel.get_all_treatments()

    def add_treatment(self, name, description, cost):
        """Agrega un nuevo tratamiento."""
        TreatmentModel.add_treatment(name, description, cost)

    def update_treatment(self, treatment_id, name, description, cost):
        """Actualiza un tratamiento existente."""
        TreatmentModel.update_treatment(treatment_id, name, description, cost)

    def delete_treatment(self, treatment_id):
        """Elimina un tratamiento."""
        TreatmentModel.delete_treatment(treatment_id)

    def get_treatments_by_historia(self, historia_id):
        """Obtiene los tratamientos aplicados a una historia clínica."""
        return TreatmentModel.get_treatments_by_historia(historia_id)

    def apply_treatment(self, historia_id, treatment_id, notes, appointment_id=None):
        TreatmentModel.apply_treatment(historia_id, treatment_id, notes, appointment_id)
