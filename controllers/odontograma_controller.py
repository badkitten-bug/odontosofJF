from models.odontograma_model import OdontogramaModel

class OdontogramaController:
    def get_odontograma(self, historia_id):
        return OdontogramaModel.get_odontograma(historia_id)

    def save_odontograma(self, historia_id, dientes_data):
        return OdontogramaModel.save_odontograma(historia_id, dientes_data)

    def update_odontograma(self, odontograma_id, condition, notes):
        return OdontogramaModel.update_odontograma(odontograma_id, condition, notes)
