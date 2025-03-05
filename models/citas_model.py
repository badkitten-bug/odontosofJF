from database.db_config import connect_db

class CitasModel:
    @staticmethod
    def get_citas_by_paciente(paciente_id):
        """Obtiene todas las citas de un paciente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.date, c.first_time, c.end_time, c.notes, c.status_id, d.nombres, d.apellidos 
                FROM appointments c
                JOIN doctors d ON c.doctor_id = d.id
                WHERE c.patient_id = ?
                ORDER BY c.date DESC
            """, (paciente_id,))
            return cursor.fetchall()

    @staticmethod
    def update_cita_status(cita_id, new_status):
        """Actualiza el estado de una cita."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointments 
                SET status_id = ? 
                WHERE id = ?
            """, (new_status, cita_id))
            conn.commit()
