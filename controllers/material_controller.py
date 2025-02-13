# controllers/material_controller.py
from models.material_model import MaterialModel

class MaterialController:
    def __init__(self):
        self.model = MaterialModel()

    def load_materials(self):
        return self.model.get_all()

    def add_material(self, name, description, unit_cost, status="Activo"):
        self.model.add_material((name, description, unit_cost, status))
