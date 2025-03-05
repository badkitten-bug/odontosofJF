from models.diagnostico_model import DiagnosticoModel

class DiagnosticoController:
    def get_diagnosticos(self, historia_id):
        return DiagnosticoModel.get_diagnosticos_by_historia(historia_id)

    def add_diagnostico(self, historia_id, diagnostico, observaciones):
        return DiagnosticoModel.add_diagnostico(historia_id, diagnostico, observaciones)

    def update_diagnostico(self, diagnostico_id, diagnostico, observaciones):
        return DiagnosticoModel.update_diagnostico(diagnostico_id, diagnostico, observaciones)
