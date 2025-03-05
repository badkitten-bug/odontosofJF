from database.db_config import connect_db
from datetime import datetime

class DoctorModel:
    @staticmethod
    def load_doctors():
        """Carga todos los doctores con sus especialidades."""
        try:
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
                    ORDER BY d.apellidos, d.nombres
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar doctores: {e}")
            return []

    @staticmethod
    def get_doctor_by_id(doctor_id):
        """Obtiene un doctor por su ID."""
        try:
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
        except Exception as e:
            print(f"Error al obtener doctor: {e}")
            return None

    @staticmethod
    def add_doctor(data):
        """Agrega un nuevo doctor."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Verificar documento duplicado
                cursor.execute("SELECT COUNT(*) FROM doctors WHERE nro_documento = ? AND is_deleted = 0", (data[4],))
                if cursor.fetchone()[0] > 0:
                    return "Error: Documento duplicado"

                # Validar estado
                estado = data[12]
                if not estado or estado not in ["Activo", "Inactivo"]:
                    estado = "Activo"

                # Crear lista de valores con estado validado
                valores = list(data)
                valores[12] = estado

                cursor.execute("""
                    INSERT INTO doctors (
                        nombres, apellidos, especialidad_id, tipo_documento_id, nro_documento,
                        ruc, direccion, colegiatura, fecha_registro, fecha_nacimiento,
                        celular, sexo, estado, correo, foto
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(valores))
                conn.commit()
                return "Success"
        except Exception as e:
            print(f"Error al agregar doctor: {e}")
            return str(e)

    @staticmethod
    def update_doctor(doctor_id, data):
        """Actualiza un doctor existente sin modificar la fecha de registro."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Verificar que el doctor existe
                cursor.execute("SELECT estado FROM doctors WHERE id = ?", (doctor_id,))
                result = cursor.fetchone()
                if not result:
                    return "Error: Doctor no encontrado"
                
                current_estado = result[0]
                
                # Validar estado
                estado = data[11]  # Posición del estado en la tupla de actualización
                if not estado or estado not in ["Activo", "Inactivo"]:
                    estado = current_estado if current_estado in ["Activo", "Inactivo"] else "Activo"
                
                # Crear lista de valores con estado validado
                valores = list(data)
                valores[11] = estado
                
                cursor.execute("""
                    UPDATE doctors SET
                        nombres = ?, apellidos = ?, especialidad_id = ?, tipo_documento_id = ?, 
                        nro_documento = ?, ruc = ?, direccion = ?, colegiatura = ?, 
                        fecha_nacimiento = ?, celular = ?, sexo = ?, estado = ?, 
                        correo = ?, foto = ?
                    WHERE id = ?
                """, (*valores, doctor_id))
                conn.commit()
                return "Success"
        except Exception as e:
            print(f"Error al actualizar doctor: {e}")
            return str(e)

    @staticmethod
    def delete_doctor(doctor_id):
        """Elimina un doctor (soft delete)."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE doctors SET is_deleted = 1 WHERE id = ?", (doctor_id,))
                conn.commit()
                return "Success"
        except Exception as e:
            print(f"Error al eliminar doctor: {e}")
            return str(e)

    @staticmethod
    def load_specialties():
        """Carga las especialidades activas."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre FROM specialties WHERE estado = 'Activo'")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar especialidades: {e}")
            return []

    @staticmethod
    def load_doctor_types():
        """Carga los tipos de doctor."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM doctor_types WHERE is_active = 1")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar tipos de doctor: {e}")
            return []

    @staticmethod
    def load_document_types():
        """Carga los tipos de documento."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name FROM document_types")
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al cargar tipos de documento: {e}")
            return []
