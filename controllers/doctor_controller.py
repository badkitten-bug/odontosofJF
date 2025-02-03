from models.doctor import DoctorModel

class DoctorController:
    def __init__(self):
        self.model = DoctorModel()

    def load_doctors(self):
        """Carga todos los doctores."""
        return self.model.load_doctors()

    def get_doctor_by_id(self, doctor_id):
        """Obtiene un doctor por su ID."""
        return self.model.get_doctor_by_id(doctor_id)

    def add_doctor(self, data):
        """Agrega un nuevo doctor."""
        self.model.add_doctor(data)

    def update_doctor(self, doctor_id, data):
        """Actualiza un doctor existente."""
        self.model.update_doctor(doctor_id, data)

    def delete_doctor(self, doctor_id):
        """Elimina un doctor."""
        self.model.delete_doctor(doctor_id)