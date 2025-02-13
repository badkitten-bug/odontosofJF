from models.historia_clinica_model import HistoriaClinicaModel

class HistoriaController:
    """Controlador para la gestión de historias clínicas"""

    def __init__(self):
        self.model = HistoriaClinicaModel()

    def load_historias(self, start_date=None, end_date=None, patient_name=None):
        """Obtiene todas las historias clínicas con filtros opcionales"""
        return self.model.load_historias(start_date, end_date, patient_name)

    def get_historia(self, historia_id):
        """Obtiene una historia clínica específica para edición"""
        return self.model.get_historia_by_id(historia_id)

    def update_historia(self, historia_id, observaciones, exploracion_fisica, odontograma, diagnostico, evolucion, examenes_auxiliares, tratamientos_realizados, notas, adjuntos):
        """Actualiza una historia clínica con todos sus campos"""
        return self.model.update_historia(historia_id, observaciones, exploracion_fisica, odontograma, diagnostico, evolucion, examenes_auxiliares, tratamientos_realizados, notas, adjuntos)

    def update_paciente(self, paciente_id, data):
        """Actualiza los datos del paciente"""
        return self.model.update_paciente(paciente_id, data)

    def delete_historia(self, historia_id):
        """Elimina una historia clínica"""
        return self.model.delete_historia(historia_id)
