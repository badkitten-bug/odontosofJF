from database.db_config import connect_db

class DoctorModel:
    @staticmethod
    def load_doctors():
        """Carga todos los doctores con sus especialidades."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.nombres, d.apellidos, s.nombre AS especialidad, dt.name AS tipo_documento,
                       d.nro_documento, d.ruc, d.direccion, d.colegiatura, d.fecha_registro, d.fecha_nacimiento,
                       d.celular, d.sexo, d.estado, d.correo, d.foto
                FROM doctors d
                JOIN specialties s ON d.especialidad_id = s.id
                JOIN document_types dt ON d.tipo_documento_id = dt.id
                WHERE d.is_deleted = 0
            """)
            return cursor.fetchall()

    @staticmethod
    def get_doctor_by_id(doctor_id):
        """Obtiene un doctor por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, d.nombres, d.apellidos, d.especialidad_id, d.tipo_documento_id, d.nro_documento,
                       d.ruc, d.direccion, d.colegiatura, d.fecha_registro, d.fecha_nacimiento, d.celular,
                       d.sexo, d.estado, d.correo, d.foto
                FROM doctors d
                WHERE d.id = ? AND d.is_deleted = 0
            """, (doctor_id,))
            return cursor.fetchone()

    @staticmethod
    def add_doctor(data):
        """Agrega un nuevo doctor."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO doctors (
                        nombres, apellidos, especialidad_id, tipo_documento_id, nro_documento, ruc, direccion,
                        colegiatura, fecha_registro, fecha_nacimiento, celular, sexo, estado, correo, foto
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, data)
                conn.commit()
        except Exception as e:
            print(f"Error al agregar doctor: {e}")
            conn.rollback()

    @staticmethod
    def update_doctor(doctor_id, data):
        """Actualiza un doctor existente sin modificar la fecha de registro."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Asegurar que `data` tenga exactamente 14 valores
                if len(data) != 14:
                    raise ValueError(f"Se esperaban 14 valores en `data`, pero se recibieron {len(data)}")
                
                cursor.execute("""
                    UPDATE doctors SET
                        nombres = ?, apellidos = ?, especialidad_id = ?, tipo_documento_id = ?, nro_documento = ?,
                        ruc = ?, direccion = ?, colegiatura = ?, fecha_nacimiento = ?,
                        celular = ?, sexo = ?, estado = ?, correo = ?, foto = ?
                    WHERE id = ?
                """, (*data, doctor_id))  # ✅ 14 valores + ID (15 en total)
                conn.commit()
        except Exception as e:
            print(f"Error al actualizar doctor: {e}")
            conn.rollback()

    @staticmethod
    def delete_doctor(doctor_id):
        """Elimina un doctor (soft delete)."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE doctors SET is_deleted = 1 WHERE id = ?", (doctor_id,))
                conn.commit()
        except Exception as e:
            print(f"Error al eliminar doctor: {e}")
            conn.rollback()
