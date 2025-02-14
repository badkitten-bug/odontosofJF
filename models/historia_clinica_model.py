from database.db_config import connect_db

def parse_time(time_str):
    """Intenta analizar un string de hora usando varios formatos."""
    from datetime import datetime
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Time data {time_str!r} does not match expected formats")

class HistoriaClinicaModel:
    """Modelo para la gestión de historias clínicas."""

    @staticmethod
    def load_historias(start_date=None, end_date=None, patient_name=None):
        """Carga historias clínicas con filtros opcionales."""
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT h.id, 
                       p.history_number, 
                       p.nombres || ' ' || p.apellidos AS paciente,
                       p.edad, 
                       p.nro_documento AS dni, 
                       COALESCE(a.date, 'Sin cita') AS fecha_cita,
                       COALESCE(a.first_time, 'Sin cita') AS hora_cita, 
                       COALESCE(s.name, 'Sin cita') AS estado
                FROM historias_clinicas h
                JOIN patients p ON h.paciente_id = p.id
                LEFT JOIN appointments a ON h.paciente_id = a.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.id
                LEFT JOIN appointment_status s ON a.status_id = s.id
                WHERE 1=1
            """
            params = []
            if start_date and end_date:
                query += " AND a.date BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            elif start_date:
                query += " AND a.date >= ?"
                params.append(start_date)
            elif end_date:
                query += " AND a.date <= ?"
                params.append(end_date)

            if patient_name:
                query += " AND (p.nombres LIKE ? OR p.apellidos LIKE ?)"
                params.extend([f"%{patient_name}%", f"%{patient_name}%"])

            query += " ORDER BY h.id DESC"
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_historia_by_id(historia_id):
        """
        Obtiene la historia clínica y sus datos asociados.
        Ahora se usa p.history_number en lugar de h.numero_historia y a.first_time en lugar de a.time.
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.id, 
                       p.history_number, 
                       h.fecha_creacion, 
                       h.observaciones,
                       p.id AS paciente_id, 
                       p.nombres, 
                       p.apellidos, 
                       p.edad, 
                       p.nro_documento, 
                       p.direccion,
                       COALESCE(a.date, 'Sin cita') AS fecha_cita, 
                       COALESCE(a.first_time, 'Sin cita') AS hora_cita,
                       COALESCE(d.nombres || ' ' || d.apellidos, 'Sin doctor') AS doctor_asignado,
                       COALESCE(s.name, 'Sin cita') AS estado
                FROM historias_clinicas h
                JOIN patients p ON h.paciente_id = p.id
                LEFT JOIN appointments a ON h.paciente_id = a.patient_id
                LEFT JOIN doctors d ON a.doctor_id = d.id
                LEFT JOIN appointment_status s ON a.status_id = s.id
                WHERE h.id = ?
                ORDER BY a.date DESC, a.first_time DESC;
            """, (historia_id,))
            return cursor.fetchall()

    @staticmethod
    def get_historias_clinicas(self, fecha_desde=None, fecha_hasta=None, nombre_paciente=None):
        query = '''
            SELECT hc.id, p.nombres || ' ' || p.apellidos AS paciente, p.edad, p.nro_documento AS dni, 
                   a.date AS fecha_cita, a.first_time AS hora_cita, a.status_id
            FROM historia_clinica hc
            JOIN patients p ON hc.patient_id = p.id
            JOIN appointments a ON p.id = a.patient_id
        '''
        filters = []
        params = []

        if fecha_desde:
            filters.append("a.date >= ?")
            params.append(fecha_desde)

        if fecha_hasta:
            filters.append("a.date <= ?")
            params.append(fecha_hasta)

        if nombre_paciente:
            filters.append("(p.nombres LIKE ? OR p.apellidos LIKE ?)")
            params.extend([f"%{nombre_paciente}%", f"%{nombre_paciente}%"])

        if filters:
            query += " WHERE " + " AND ".join(filters)

        query += " ORDER BY a.date DESC"

        import sqlite3
        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        return results

    @staticmethod
    def update_historia(historia_id, observaciones, exploracion_fisica, odontograma, diagnostico, evolucion, examenes_auxiliares, tratamientos_realizados, notas, adjuntos):
        """Actualiza la historia clínica con más campos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE historias_clinicas 
                SET observaciones = ?, exploracion_fisica = ?, odontograma = ?, diagnostico = ?, 
                    evolucion = ?, examenes_auxiliares = ?, tratamientos_detalle = ?, 
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
                SET nombres = ?, apellidos = ?, fecha_nacimiento = ?, edad = ?, nro_documento = ?,
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

    @staticmethod
    def create_history_for_patient(patient_id):
        """Crea un registro en la tabla historias_clinicas para el paciente dado."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historias_clinicas (paciente_id, fecha_creacion, observaciones)
                VALUES (?, CURRENT_TIMESTAMP, '')
            """, (patient_id,))
            conn.commit()