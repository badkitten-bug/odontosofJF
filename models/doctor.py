from database.db_config import connect_db

class DoctorModel:
    @staticmethod
    def load_doctors():
        """Carga todos los doctores con sus especialidades."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.nombres, d.apellidos, s.nombre AS especialidad, d.tipo_documento, d.nro_documento,
                       d.ruc, d.direccion, d.colegiatura, d.fecha_registro, d.fecha_nacimiento, d.telefono,
                       d.celular, d.sexo, d.estado, d.correo, d.foto, d.usuario, d.password
                FROM doctors d
                JOIN specialties s ON d.especialidad_id = s.id
            """)
            return cursor.fetchall()

    @staticmethod
    def get_doctor_by_id(doctor_id):
        """Obtiene un doctor por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.nombres, d.apellidos, d.especialidad_id, d.tipo_documento, d.nro_documento,
                       d.ruc, d.direccion, d.colegiatura, d.fecha_registro, d.fecha_nacimiento, d.telefono,
                       d.celular, d.sexo, d.estado, d.correo, d.foto, d.usuario, d.password
                FROM doctors d
                WHERE d.id = ?
            """, (doctor_id,))
            return cursor.fetchone()

    @staticmethod
    def add_doctor(data):
        """Agrega un nuevo doctor."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO doctors (
                    nombres, apellidos, especialidad_id, tipo_documento, nro_documento, ruc, direccion,
                    colegiatura, fecha_registro, fecha_nacimiento, telefono, celular, sexo, estado,
                    correo, foto, usuario, password
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()

    @staticmethod
    def update_doctor(doctor_id, data):
        """Actualiza un doctor existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE doctors SET
                    nombres = ?, apellidos = ?, especialidad_id = ?, tipo_documento = ?, nro_documento = ?,
                    ruc = ?, direccion = ?, colegiatura = ?, fecha_nacimiento = ?, telefono = ?,
                    celular = ?, sexo = ?, estado = ?, correo = ?, foto = ?, usuario = ?, password = ?
                WHERE id = ?
            """, (*data, doctor_id))
            conn.commit()

    @staticmethod
    def delete_doctor(doctor_id):
        """Elimina un doctor."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
            conn.commit()