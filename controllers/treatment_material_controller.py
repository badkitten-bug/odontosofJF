# controllers/treatment_material_controller.py
from models.treatment_material_model import TreatmentMaterialModel

class TreatmentMaterialController:
    def __init__(self):
        self.model = TreatmentMaterialModel()

    def get_materials_by_treatment(self, treatment_id):
        return self.model.get_by_treatment(treatment_id)

    def add_relation(self, treatment_id, material_id, quantity):
        self.model.add_relation((treatment_id, material_id, quantity))
