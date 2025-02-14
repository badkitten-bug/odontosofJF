from database.db_config import connect_db
from datetime import datetime

def parse_time(time_str):
    """Intenta analizar un string de hora usando varios formatos."""
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Time data {time_str!r} does not match expected formats")

class AppointmentModel:
    @staticmethod
    def load_patients():
        """Carga la lista de pacientes activos con su historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.nombres || ' ' || p.apellidos AS name, p.history_number
                FROM patients p
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
    def load_doctors_by_specialty(specialty_id):
        """Carga la lista de doctores filtrada por la especialidad seleccionada."""
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT d.id,
                       d.nombres || ' ' || d.apellidos AS name,
                       s.nombre AS especialidad
                FROM doctors d
                LEFT JOIN specialties s ON d.especialidad_id = s.id
                WHERE s.id = ?
            """
            cursor.execute(query, (specialty_id,))
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
            SELECT a.id, 
                   p.nombres || ' ' || p.apellidos AS paciente, 
                   d.nombres || ' ' || d.apellidos AS doctor, 
                   a.date, 
                   a.first_time,
                   TIME(a.first_time, '+' || a.duration || ' minutes') AS computed_end_time,
                   a.notes, 
                   s.name AS status
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

            query += " ORDER BY a.date, a.first_time"
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Obtiene una cita por su ID con el ID y nombre del estado."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.patient_id, a.doctor_id, a.date, a.first_time, a.duration, 
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
              (patient_id, doctor_id, date, first_time, duration, notes, status_id)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO appointments (patient_id, doctor_id, date, first_time, duration, notes, status_id, is_deleted) 
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """, data)
            conn.commit()

    @staticmethod
    def update_appointment(appointment_id, data):
        """
        Actualiza una cita existente.
        data: tuple con los siguientes elementos:
              (patient_id, doctor_id, date, first_time, duration, notes, status_id)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointments 
                SET patient_id = ?, doctor_id = ?, date = ?, first_time = ?, duration = ?, notes = ?, status_id = ? 
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
                INSERT INTO appointments (patient_id, doctor_id, date, first_time, duration, notes, status_id, is_deleted)
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
            SELECT a.first_time FROM appointments a WHERE a.doctor_id = ? AND a.date = ? AND a.is_deleted = 0;
            """
            cursor.execute(query, (doctor_id, date, doctor_id, date))
            return cursor.fetchall()

    @staticmethod
    def get_doctor_schedule(doctor_id, day_of_week):
        """Obtiene el horario del doctor para un día específico."""
        day_map = {
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes",
            6: "Sábado",
            7: "Domingo"
        }
        day_name = day_map.get(day_of_week, "")
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT start_time, end_time 
                FROM doctor_schedules 
                WHERE doctor_id = ? AND day_of_week = ?
                LIMIT 1
            """
            cursor.execute(query, (doctor_id, day_name))
            result = cursor.fetchone()
            if result:
                start_time = parse_time(result[0]) if isinstance(result[0], str) else result[0]
                end_time = parse_time(result[1]) if isinstance(result[1], str) else result[1]
                return {"start_time": start_time, "end_time": end_time}
            return None

    @staticmethod
    def get_booked_slots(doctor_id, date):
        """Obtiene las citas agendadas (slots ya ocupados) para un doctor en una fecha específica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            query = """
                SELECT first_time, TIME(first_time, '+' || duration || ' minutes') AS computed_end_time
                FROM appointments
                WHERE doctor_id = ? AND date = ? AND is_deleted = 0
            """
            cursor.execute(query, (doctor_id, date))
            results = cursor.fetchall()
            booked_slots = []
            for row in results:
                start_time = row[0]
                end_time = row[1]
                if isinstance(start_time, str):
                    start_time = parse_time(start_time)
                if isinstance(end_time, str):
                    end_time = parse_time(end_time)
                booked_slots.append({"start_time": start_time, "end_time": end_time})
            return booked_slots
