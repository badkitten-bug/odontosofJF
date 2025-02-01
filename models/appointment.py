from database.db_config import connect_db

class AppointmentModel:
    @staticmethod
    def load_patients():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombres || ' ' || apellidos AS name, history_number FROM patients WHERE is_deleted = 0"
            )
            return cursor.fetchall()

    @staticmethod
    def load_doctors():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombres || ' ' || apellidos AS name, especialidad FROM doctors")
            return cursor.fetchall()

    @staticmethod
    def load_appointments(date=None, doctor_id=None, status=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            query = '''
                SELECT appointments.id, patients.name, doctors.name, appointments.date, appointments.time, 
                       appointments.duration, appointments.notes, appointments.status
                FROM appointments
                JOIN patients ON appointments.patient_id = patients.id
                JOIN doctors ON appointments.doctor_id = doctors.id
                WHERE appointments.is_deleted = 0
            '''
            params = []
            if date:
                query += " AND appointments.date = ?"
                params.append(date)
            if doctor_id:
                query += " AND appointments.doctor_id = ?"
                params.append(doctor_id)
            if status:
                query += " AND appointments.status = ?"
                params.append(status)
            cursor.execute(query, params)
            return cursor.fetchall()

    @staticmethod
    def get_appointment_by_id(appointment_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT patient_id, doctor_id, date, time, duration, notes, status FROM appointments WHERE id = ?",
                (appointment_id,)
            )
            return cursor.fetchone()

    @staticmethod
    def add_appointment(data):
        """
        data: tuple con los siguientes elementos:
              (patient_id, doctor_id, date, time, duration, notes, status)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO appointments (patient_id, doctor_id, date, time, duration, notes, status, is_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                data
            )
            conn.commit()

    @staticmethod
    def update_appointment(appointment_id, data):
        """
        data: tuple con los siguientes elementos:
              (patient_id, doctor_id, date, time, duration, notes, status)
        """
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE appointments SET patient_id = ?, doctor_id = ?, date = ?, time = ?, duration = ?, notes = ?, status = ? WHERE id = ?",
                (*data, appointment_id)
            )
            conn.commit()

    @staticmethod
    def delete_appointment(appointment_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET is_deleted = 1 WHERE id = ?", (appointment_id,))
            conn.commit()
