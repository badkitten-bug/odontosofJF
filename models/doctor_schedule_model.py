from database.db_config import connect_db

class DoctorScheduleModel:
    """Manejo de los horarios de los doctores."""

    @staticmethod
    def add_schedule(doctor_id, day_of_week, start_time, end_time):
        """Agrega un horario a un doctor."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO doctor_schedules (doctor_id, day_of_week, start_time, end_time)
                VALUES (?, ?, ?, ?)
            """, (doctor_id, day_of_week, start_time, end_time))
            conn.commit()

    @staticmethod
    def get_schedules_by_doctor(doctor_id):
        """Obtiene todos los horarios de un doctor."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, day_of_week, start_time, end_time
                FROM doctor_schedules WHERE doctor_id = ?
                ORDER BY day_of_week
            """, (doctor_id,))
            return cursor.fetchall()

    @staticmethod
    def delete_schedule(schedule_id):
        """Elimina un horario de un doctor."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM doctor_schedules WHERE id = ?", (schedule_id,))
            conn.commit()
