from models.citas_model import CitasModel

class CitasController:
    def get_citas(self, paciente_id):
        return CitasModel.get_citas_by_paciente(paciente_id)

    def update_cita_status(self, cita_id, new_status):
        return CitasModel.update_cita_status(cita_id, new_status)
