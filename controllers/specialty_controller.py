from models.specialty_model import SpecialtyModel

class SpecialtyController:
    def __init__(self):
        self.model = SpecialtyModel()

    def load_specialties(self):
        """Carga todas las especialidades."""
        return self.model.load_specialties()

    def add_specialty(self, nombre, descripcion, estado="Activo"):
        """Agrega una nueva especialidad."""
        try:
            self.model.add_specialty(nombre, descripcion, estado)
        except ValueError as ve:
            raise ve  # Re-raise the exception to handle it in the UI

    def update_specialty(self, specialty_id, nombre, descripcion, estado):
        """Actualiza una especialidad existente."""
        self.model.update_specialty(specialty_id, nombre, descripcion, estado)

    def delete_specialty(self, specialty_id):
        """Elimina una especialidad."""
        self.model.delete_specialty(specialty_id)