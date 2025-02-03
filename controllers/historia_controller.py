from models.historia_model import HistoriaModel

class HistoriaController:
    def __init__(self):
        self.model = HistoriaModel()

    def load_historias(self):
        """Carga todas las historias clínicas."""
        return self.model.load_historias()

    def add_historia(self, paciente_id, numero_historia, fecha_creacion, observaciones):
        """Agrega una nueva historia clínica."""
        self.model.add_historia(paciente_id, numero_historia, fecha_creacion, observaciones)

    def update_historia(self, historia_id, observaciones):
        """Actualiza una historia clínica existente."""
        self.model.update_historia(historia_id, observaciones)

    def delete_historia(self, historia_id):
        """Elimina una historia clínica."""
        self.model.delete_historia(historia_id)