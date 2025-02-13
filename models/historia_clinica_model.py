from database.db_config import connect_db

class HistoriaClinicaModel:
    """Modelo para la gestión de historias clínicas con lo mejor de ambos modelos."""

    @staticmethod
    def load_historias(start_date=None, end_date=None, patient_name=None):
        """Carga las historias clínicas con filtros opcionales por fecha, paciente y el último doctor asignado."""
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT h.id, h.numero_historia, p.nombres || ' ' || p.apellidos AS paciente,
                    p.edad, p.dni, COALESCE(a.date, 'Sin cita') AS fecha_cita,
                    COALESCE(a.time, 'Sin cita') AS hora_cita, 
                    COALESCE(d.nombres || ' ' || d.apellidos, 'Sin doctor') AS doctor_asignado,
                    COALESCE(s.name, 'Sin cita') AS estado
                FROM historias_clinicas h
                JOIN patients p ON h.paciente_id = p.id
                LEFT JOIN appointments a ON h.paciente_id = a.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.id
                LEFT JOIN appointment_status s ON a.status_id = s.id
                WHERE 1=1
            """
            params = []
            if start_date:
                query += " AND a.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND a.date <= ?"
                params.append(end_date)
            if patient_name:
                query += " AND (p.nombres LIKE ? OR p.apellidos LIKE ?)"
                params.extend([f"%{patient_name}%", f"%{patient_name}%"])

            query += " ORDER BY h.fecha_creacion DESC"
            cursor.execute(query, params)
            return cursor.fetchall()


    @staticmethod
    def get_historia_by_id(historia_id):
        """Obtiene la historia clínica y lista todas sus citas con los doctores que lo atendieron."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.id, h.numero_historia, h.fecha_creacion, h.observaciones,
                    p.id AS paciente_id, p.nombres, p.apellidos, p.edad, p.dni, p.direccion,
                    COALESCE(a.date, 'Sin cita') AS fecha_cita, 
                    COALESCE(a.time, 'Sin cita') AS hora_cita,
                    COALESCE(d.nombres || ' ' || d.apellidos, 'Sin doctor') AS doctor_asignado,
                    COALESCE(s.name, 'Sin cita') AS estado
                FROM historias_clinicas h
                JOIN patients p ON h.paciente_id = p.id
                LEFT JOIN appointments a ON h.paciente_id = a.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.id
                LEFT JOIN appointment_status s ON a.status_id = s.id
                WHERE h.id = ?
                ORDER BY a.date DESC, a.time DESC;
            """, (historia_id,))
            return cursor.fetchall()

    @staticmethod
    def update_historia(historia_id, observaciones, exploracion_fisica, odontograma, diagnostico, evolucion, examenes_auxiliares, tratamientos_realizados, notas, adjuntos):
        """Actualiza la historia clínica con más campos, incluyendo doctor, notas y adjuntos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE historias_clinicas 
                SET observaciones = ?, exploracion_fisica = ?, odontograma = ?, diagnostico = ?, 
                    evolucion = ?, examenes_auxiliares = ?, tratamientos_realizados = ?, 
                    notas = ?, adjuntos = ?
                WHERE id = ?
            """, (observaciones, exploracion_fisica, odontograma, diagnostico, evolucion, examenes_auxiliares, tratamientos_realizados, notas, adjuntos, historia_id))
            conn.commit()

    @staticmethod
    def update_paciente(paciente_id, data):
        """Actualiza los datos del paciente asociados a la historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE patients 
                SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, edad = ?, dni = ?,
                    direccion = ?, sexo = ?, grado_instruccion = ?, estado_civil = ?, correo = ?,
                    pais = ?, departamento = ?, provincia = ?, distrito = ?, observacion = ?
                WHERE id = ?
            """, (*data, paciente_id))
            conn.commit()

    @staticmethod
    def delete_historia(historia_id):
        """Elimina una historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historias_clinicas WHERE id = ?", (historia_id,))
            conn.commit()