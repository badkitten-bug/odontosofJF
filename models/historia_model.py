from database.db_config import connect_db

class HistoriaModel:
    @staticmethod
    def load_historias():
        """Carga todas las historias clínicas con información de pacientes."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.id, h.numero_historia, p.nombres, p.apellidos, p.documento, h.fecha_creacion
                FROM historias_clinicas h
                JOIN patients p ON h.paciente_id = p.id
            """)
            return cursor.fetchall()

    @staticmethod
    def add_historia(paciente_id, numero_historia, fecha_creacion, observaciones):
        """Agrega una nueva historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historias_clinicas (paciente_id, numero_historia, fecha_creacion, observaciones)
                VALUES (?, ?, ?, ?)
            """, (paciente_id, numero_historia, fecha_creacion, observaciones))
            conn.commit()

    @staticmethod
    def update_historia(historia_id, observaciones):
        """Actualiza una historia clínica existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE historias_clinicas SET observaciones = ? WHERE id = ?
            """, (observaciones, historia_id))
            conn.commit()

    @staticmethod
    def delete_historia(historia_id):
        """Elimina una historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM historias_clinicas WHERE id = ?", (historia_id,))
            conn.commit()