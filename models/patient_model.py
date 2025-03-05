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
    def get_patient_by_id(patient_id):
        """Obtiene un paciente por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, p.history_number, p.nombres, p.apellidos, p.edad,
                    p.tipo_documento_id, p.nro_documento, p.grado_instruccion_id,
                    p.hospital_nacimiento, p.pais, p.departamento, p.provincia, 
                    p.distrito, p.direccion, p.telefono, p.fecha_nacimiento,
                    p.estado_civil_id, p.afiliado, p.sexo, p.alergia, p.correo, 
                    p.observacion, p.fecha_registro, p.estado
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
                
                # Obtener el history_number y estado actual
                cursor.execute("SELECT history_number, estado FROM patients WHERE id = ?", (patient_id,))
                result = cursor.fetchone()
                current_history = result[0]
                current_estado = result[1]
                
                # Crear nueva tupla de datos reemplazando valores necesarios
                data_list = list(data)
                data_list[5] = current_history  # Posición 5 es history_number
                
                # Depuración del estado
                print(f"Estado actual en BD: {current_estado}")
                print(f"Estado recibido en data: {data_list[22]}")
                print(f"Tipo de dato del estado recibido: {type(data_list[22])}")
                
                # Manejo específico del estado
                estado_final = data_list[22]
                if estado_final is None or estado_final == "" or estado_final not in ["Activo", "Inactivo"]:
                    estado_final = current_estado if current_estado in ["Activo", "Inactivo"] else "Activo"
                    print(f"Estado era inválido, usando valor por defecto: {estado_final}")
                
                # Asegurar que el estado final sea una cadena válida
                estado_final = str(estado_final).strip()
                if estado_final not in ["Activo", "Inactivo"]:
                    estado_final = "Activo"
                
                print(f"Estado final a guardar: {estado_final}")
                
                # Crear los valores de actualización (excluyendo fecha_registro)
                update_values = [
                    data_list[0],  # nombres
                    data_list[1],  # apellidos
                    data_list[2],  # edad
                    data_list[3],  # tipo_documento_id
                    data_list[4],  # nro_documento
                    current_history,  # history_number
                    data_list[6],  # grado_instruccion_id
                    data_list[7],  # hospital_nacimiento
                    data_list[8],  # pais
                    data_list[9],  # departamento
                    data_list[10],  # provincia
                    data_list[11],  # distrito
                    data_list[12],  # direccion
                    data_list[13],  # telefono
                    data_list[14],  # fecha_nacimiento
                    data_list[15],  # estado_civil_id
                    data_list[16],  # afiliado
                    data_list[17],  # sexo
                    data_list[18],  # alergia
                    data_list[19],  # correo
                    data_list[20],  # observacion
                    estado_final    # estado
                ]
                
                cursor.execute("""
                    UPDATE patients SET
                        nombres = ?, apellidos = ?, edad = ?, 
                        tipo_documento_id = ?, nro_documento = ?, history_number = ?,
                        grado_instruccion_id = ?, hospital_nacimiento = ?, 
                        pais = ?, departamento = ?, provincia = ?, distrito = ?,
                        direccion = ?, telefono = ?, fecha_nacimiento = ?,
                        estado_civil_id = ?, afiliado = ?, sexo = ?, 
                        alergia = ?, correo = ?, observacion = ?,
                        estado = ?
                    WHERE id = ?
                """, (*update_values, patient_id))
                
                # Verificar el estado después de la actualización
                cursor.execute("SELECT estado FROM patients WHERE id = ?", (patient_id,))
                estado_actualizado = cursor.fetchone()[0]
                print(f"Estado después de actualizar: {estado_actualizado}")
                
                conn.commit()
                return "Success"
        except Exception as e:
            print(f"Error al actualizar paciente: {e}")
            conn.rollback()
            return str(e)


    @staticmethod
    def delete_patient(patient_id):
        """Elimina un paciente (soft delete)."""
        try:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE patients SET is_deleted = 1 WHERE id = ?", (patient_id,))
                conn.commit()
                return "Success"
        except Exception as e:
            print(f"Error al eliminar paciente: {e}")
            return str(e)

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

    @staticmethod
    def add_patient(data):
        """Agrega un nuevo paciente y le asigna automáticamente un número de historia clínica."""
        try:
            history_number = PatientModel.generate_history_number()
            nro_documento = data[4]  # nro_documento está en la posición 4

            with connect_db() as conn:
                cursor = conn.cursor()

                # Verificar documento duplicado
                cursor.execute("SELECT COUNT(*) FROM patients WHERE nro_documento = ?", (nro_documento,))
                if cursor.fetchone()[0] > 0:
                    print(f"Error: El número de documento '{nro_documento}' ya está registrado.")
                    return "Error: Documento duplicado"

                # Insertar nuevo paciente
                cursor.execute("""
                    INSERT INTO patients (
                        nombres, apellidos, edad, tipo_documento_id, nro_documento,
                        history_number, grado_instruccion_id, hospital_nacimiento,
                        pais, departamento, provincia, distrito,
                        direccion, telefono, fecha_nacimiento,
                        estado_civil_id, afiliado, sexo, alergia,
                        correo, observacion, fecha_registro, estado, is_deleted
                    ) VALUES (
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, 
                        ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?,
                        ?, CURRENT_TIMESTAMP, ?, 0
                    )
                """, (
                    data[0], data[1], data[2], data[3], data[4],  # nombres hasta nro_documento
                    history_number, data[6], data[7], data[8], data[9],  # history_number hasta departamento
                    data[10], data[11], data[12], data[13], data[14],  # provincia hasta fecha_nacimiento
                    data[15], data[16], data[17], data[18], data[19],  # estado_civil hasta correo
                    data[20], data[22]  # observacion, estado
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al agregar paciente: {e}")
            conn.rollback()
            return None
