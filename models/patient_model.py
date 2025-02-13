from database.db_config import connect_db
from datetime import datetime

class PatientModel:
    @staticmethod
    def load_patients():
        """Carga todos los pacientes activos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, p.history_number, p.nombres, p.apellidos, p.edad,
                    dt.name AS tipo_documento, p.nro_documento,
                    el.level AS grado_instruccion, p.hospital_nacimiento,
                    p.direccion, p.telefono, p.fecha_nacimiento,
                    ms.status AS estado_civil, p.afiliado, p.sexo,
                    p.correo, p.observacion, p.fecha_registro, p.estado
                FROM patients p
                LEFT JOIN document_types dt ON p.tipo_documento_id = dt.id
                LEFT JOIN education_levels el ON p.grado_instruccion_id = el.id
                LEFT JOIN marital_status ms ON p.estado_civil_id = ms.id
                WHERE p.is_deleted = 0
            """)
            return cursor.fetchall()
    @staticmethod
    def generate_history_number():
        """Genera un número de historia clínica único en formato HC-00001."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients")
            count = cursor.fetchone()[0] + 1  # El siguiente número disponible
            return f"HC-{str(count).zfill(5)}"

    @staticmethod
    def add_patient(data):
        """Agrega un nuevo paciente y le asigna automáticamente un número de historia clínica."""
        try:
            history_number = PatientModel.generate_history_number()  # Generar número de historia clínica
            
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO patients (
                        history_number, nombres, apellidos, edad, tipo_documento_id, nro_documento,
                        grado_instruccion_id, hospital_nacimiento, direccion, telefono,
                        fecha_nacimiento, estado_civil_id, afiliado, sexo, correo,
                        observacion, fecha_registro, estado
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (history_number, *data))  # Insertar con número de historia clínica
                
                conn.commit()
        except Exception as e:
            print(f"Error al agregar paciente: {e}")
            conn.rollback()

    @staticmethod
    def get_patient_by_id(patient_id):
        """Obtiene un paciente por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, p.history_number, p.nombres, p.apellidos, p.edad,
                    p.tipo_documento_id, p.nro_documento, p.grado_instruccion_id,
                    p.hospital_nacimiento, p.direccion, p.telefono, p.fecha_nacimiento,
                    p.estado_civil_id, p.afiliado, p.sexo, p.correo, p.observacion,
                    p.fecha_registro, p.estado
                FROM patients p
                WHERE p.id = ?
            """, (patient_id,))
            return cursor.fetchone()

    @staticmethod
    def update_patient(patient_id, data):
        """Actualiza un paciente existente."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE patients SET
                        nombres = ?, apellidos = ?, edad = ?, tipo_documento_id = ?, nro_documento = ?,
                        grado_instruccion_id = ?, hospital_nacimiento = ?, direccion = ?, telefono = ?,
                        fecha_nacimiento = ?, estado_civil_id = ?, afiliado = ?, sexo = ?, correo = ?,
                        observacion = ?, fecha_registro = ?, estado = ?
                    WHERE id = ?
                """, (*data, patient_id))
                conn.commit()
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            conn.rollback()

    @staticmethod
    def delete_patient(patient_id):
        """Elimina un paciente (soft delete)."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE patients SET is_deleted = 1 WHERE id = ?", (patient_id,))
                conn.commit()
        except Exception as e:
            print(f"Error al eliminar paciente: {e}")
            conn.rollback()

    @staticmethod
    def load_education_levels():
        """Carga los niveles de educación."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, level FROM education_levels")
            return cursor.fetchall()

    @staticmethod
    def load_marital_statuses():
        """Carga los estados civiles."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, status FROM marital_status")
            return cursor.fetchall()

    @staticmethod
    def load_document_types():
        """Carga los tipos de documento."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM document_types")
            return cursor.fetchall()