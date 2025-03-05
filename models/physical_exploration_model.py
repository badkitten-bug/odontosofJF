from database.db_config import connect_db

class ExploracionFisicaModel:
    @staticmethod
    def get_exploracion_by_historia_id(historia_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM exploracion_fisica WHERE historia_id = ?
            """, (historia_id,))
            return cursor.fetchone()

    @staticmethod
    def create_exploracion(historia_id, enfermedad_actual, tiempo_enfermedad, motivo_consulta,
                             signos_sintomas, antecedentes_personales, antecedentes_familiares,
                             medicamento_actual, motivo_uso_medicamento, dosis_medicamento,
                             tratamiento_ortodoncia, alergico_medicamento, hospitalizado,
                             transtorno_nervioso, enfermedades_padecidas, cepilla_dientes,
                             presion_arterial):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO exploracion_fisica (
                    historia_id, enfermedad_actual, tiempo_enfermedad, motivo_consulta,
                    signos_sintomas, antecedentes_personales, antecedentes_familiares,
                    medicamento_actual, motivo_uso_medicamento, dosis_medicamento,
                    tratamiento_ortodoncia, alergico_medicamento, hospitalizado,
                    transtorno_nervioso, enfermedades_padecidas, cepilla_dientes,
                    presion_arterial
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (historia_id, enfermedad_actual, tiempo_enfermedad, motivo_consulta,
                  signos_sintomas, antecedentes_personales, antecedentes_familiares,
                  medicamento_actual, motivo_uso_medicamento, dosis_medicamento,
                  tratamiento_ortodoncia, alergico_medicamento, hospitalizado,
                  transtorno_nervioso, enfermedades_padecidas, cepilla_dientes,
                  presion_arterial))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_exploracion(exploracion_id, enfermedad_actual, tiempo_enfermedad, motivo_consulta,
                             signos_sintomas, antecedentes_personales, antecedentes_familiares,
                             medicamento_actual, motivo_uso_medicamento, dosis_medicamento,
                             tratamiento_ortodoncia, alergico_medicamento, hospitalizado,
                             transtorno_nervioso, enfermedades_padecidas, cepilla_dientes,
                             presion_arterial):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE exploracion_fisica 
                SET enfermedad_actual=?, tiempo_enfermedad=?, motivo_consulta=?,
                    signos_sintomas=?, antecedentes_personales=?, antecedentes_familiares=?,
                    medicamento_actual=?, motivo_uso_medicamento=?, dosis_medicamento=?,
                    tratamiento_ortodoncia=?, alergico_medicamento=?, hospitalizado=?,
                    transtorno_nervioso=?, enfermedades_padecidas=?, cepilla_dientes=?,
                    presion_arterial=?
                WHERE id = ?
            """, (enfermedad_actual, tiempo_enfermedad, motivo_consulta,
                  signos_sintomas, antecedentes_personales, antecedentes_familiares,
                  medicamento_actual, motivo_uso_medicamento, dosis_medicamento,
                  tratamiento_ortodoncia, alergico_medicamento, hospitalizado,
                  transtorno_nervioso, enfermedades_padecidas, cepilla_dientes,
                  presion_arterial, exploracion_id))
            conn.commit()

    @staticmethod
    def delete_exploracion(exploracion_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM exploracion_fisica WHERE id = ?", (exploracion_id,))
            conn.commit()
