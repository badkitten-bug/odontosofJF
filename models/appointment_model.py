from database.db_config import connect_db

class AppointmentModel:
    @staticmethod
    def load_patients():
        """Carga la lista de pacientes activos con su historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nombres || ' ' || p.apellidos AS name, h.numero_historia
                FROM patients p
                LEFT JOIN historias_clinicas h ON p.id = h.paciente_id
                WHERE p.is_deleted = 0
            """)
            return cursor.fetchall()

    @staticmethod
    def load_doctors():
        """Carga la lista de doctores con su especialidad."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id,
                       d.nombres || ' ' || d.apellidos AS name,
                       s.nombre AS especialidad
                FROM doctors d
                LEFT JOIN specialties s ON d.especialidad_id = s.id
            """)
            return cursor.fetchall()

    @staticmethod
    def load_specialties():
        """Carga todas las especialidades activas desde la base de datos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM specialties WHERE estado = 'Activo'")
            return cursor.fetchall()
    
    @staticmethod
    def load_appointment_statuses():
        """Carga los estados de las citas desde la base de datos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM appointment_status")
            return cursor.fetchall()

    @staticmethod
    def load_appointments(date=None, doctor_id=None, specialty_id=None, status=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
            SELECT a.id, p.nombres || ' ' || p.apellidos AS paciente, 
                d.nombres || ' ' || d.apellidos AS doctor, 
                a.date, a.time, 
                TIME(a.time, '+' || a.duration || ' minutes') AS end_time,  -- Calcula la hora de fin
                a.notes, s.name AS status
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            JOIN doctors d ON a.doctor_id = d.id
            JOIN appointment_status s ON a.status_id = s.id
            WHERE a.is_deleted = 0
            """
            params = []
            if date:
                query += " AND a.date = ?"
                params.append(date)
            if doctor_id:
                query += " AND a.doctor_id = ?"
                params.append(doctor_id)
            if status:
                query += " AND a.status_id = ?"
                params.append(status)

            query += " ORDER BY a.date, a.time"
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Obtiene una cita por su ID con el ID y nombre del estado."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.patient_id, a.doctor_id, a.date, a.time, a.duration, 
                       a.notes, s.id AS status_id, s.name AS status
                FROM appointments a
                JOIN appointment_status s ON a.status_id = s.id
                WHERE a.id = ?
            """, (appointment_id,))
            return cursor.fetchone()

    @staticmethod
    def add_appointment(data):
        """
        Agrega una nueva cita.
        data: tuple con los siguientes elementos:
              (patient_id, doctor_id, date, time, duration, notes, status_id)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, date, time, duration, notes, status_id, is_deleted) 
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, data)
            conn.commit()

    @staticmethod
    def update_appointment(appointment_id, data):
        """
        Actualiza una cita existente.
        data: tuple con los siguientes elementos:
              (patient_id, doctor_id, date, time, duration, notes, status_id)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointments 
                SET patient_id = ?, doctor_id = ?, date = ?, time = ?, duration = ?, notes = ?, status_id = ? 
                WHERE id = ?
            """, (*data, appointment_id))
            conn.commit()

    @staticmethod
    def delete_appointment(appointment_id):
        """Elimina una cita (marcándola como eliminada)."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET is_deleted = 1 WHERE id = ?", (appointment_id,))
            conn.commit()

    @staticmethod
    def create_appointment(data):
        """Crea una nueva cita."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, date, time, duration, notes, status_id, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, data)
            conn.commit()

    @staticmethod
    def load_available_slots(date, doctor_id):
        """Carga los horarios disponibles para un doctor en una fecha específica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
            SELECT ds.start_time
            FROM doctor_schedules ds
            WHERE ds.doctor_id = ? 
            AND ds.day_of_week = (SELECT CASE strftime('%w', ?) 
                                    WHEN '0' THEN 'Domingo' 
                                    WHEN '1' THEN 'Lunes' 
                                    WHEN '2' THEN 'Martes' 
                                    WHEN '3' THEN 'Miercoles' 
                                    WHEN '4' THEN 'Jueves' 
                                    WHEN '5' THEN 'Viernes' 
                                    WHEN '6' THEN 'Sabado' END)
            EXCEPT
            SELECT a.time FROM appointments a WHERE a.doctor_id = ? AND a.date = ? AND a.is_deleted = 0;
            """
            cursor.execute(query, (doctor_id, date, doctor_id, date))
            return cursor.fetchall()