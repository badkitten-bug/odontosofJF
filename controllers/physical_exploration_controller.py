from models.physical_exploration_model import ExploracionFisicaModel

class ExploracionFisicaController:
    def get_exploracion(self, historia_id):
        return ExploracionFisicaModel.get_exploracion_by_historia_id(historia_id)

    def create_exploracion(self, historia_id, data):
        return ExploracionFisicaModel.create_exploracion(historia_id, *data)

    def update_exploracion(self, exploracion_id, data):
        return ExploracionFisicaModel.update_exploracion(exploracion_id, *data)

    def delete_exploracion(self, exploracion_id):
        return ExploracionFisicaModel.delete_exploracion(exploracion_id)
