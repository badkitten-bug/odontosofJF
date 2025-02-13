# controllers/treatment_controller.py
from models.treatment_model import TreatmentModel

class TreatmentController:
    def __init__(self):
        self.model = TreatmentModel()

    def load_treatments(self):
        return self.model.get_all()

    def add_treatment(self, name, description, cost, category, status="Activo"):
        self.model.add_treatment((name, description, cost, category, status))
