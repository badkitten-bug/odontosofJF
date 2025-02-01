from database.db_config import connect_db

class DoctorModel:
    @staticmethod
    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctors")
            return cursor.fetchall()

    @staticmethod
    def add_doctor(data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO doctors 
                (nombres, apellidos, especialidad, tipo_documento, nro_documento, ruc, direccion, colegiatura,
                 fecha_registro, fecha_nacimiento, telefono, celular, sexo, estado, correo, foto, usuario, password)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                data
            )
            conn.commit()

    @staticmethod
    def update_doctor(doctor_id, data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE doctors
                SET nombres = ?, apellidos = ?, especialidad = ?, tipo_documento = ?, nro_documento = ?, ruc = ?,
                    direccion = ?, colegiatura = ?, fecha_nacimiento = ?, telefono = ?, celular = ?, sexo = ?,
                    estado = ?, correo = ?, foto = ?, usuario = ?, password = ?
                WHERE id = ?
                """,
                (*data, doctor_id)
            )
            conn.commit()

    @staticmethod
    def delete_doctor(doctor_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()

    @staticmethod
    def get_doctor_by_id(doctor_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
            return cursor.fetchone()
