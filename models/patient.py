from database.db_config import connect_db

class PatientModel:
    @staticmethod
    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE is_deleted = 0")
            return cursor.fetchall()

    @staticmethod
    def add_patient(data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO patients 
                (nombres, apellidos, edad, grado_instruccion, hospital_nacimiento, pais, departamento, provincia, distrito, 
                 direccion, documento, telefono, fecha_registro, fecha_nacimiento, estado_civil, afiliado, sexo, estado, alergia, correo, observacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                data
            )
            conn.commit()

    @staticmethod
    def update_patient(patient_id, data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE patients 
                SET nombres = ?, apellidos = ?, edad = ?, grado_instruccion = ?, hospital_nacimiento = ?,
                    pais = ?, departamento = ?, provincia = ?, distrito = ?, direccion = ?, documento = ?,
                    telefono = ?, fecha_nacimiento = ?, sexo = ?, estado = ?, alergia = ?, correo = ?, observacion = ?
                WHERE id = ?
                """,
                (*data, patient_id)
            )
            conn.commit()

    @staticmethod
    def delete_patient(patient_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE patients SET is_deleted = 1 WHERE id = ?", (patient_id,))
            conn.commit()

    @staticmethod
    def get_patient_by_id(patient_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
            return cursor.fetchone()
