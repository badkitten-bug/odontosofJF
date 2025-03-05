from database.db_config import connect_db

class DiagnosticoModel:
    @staticmethod
    def get_diagnosticos_by_historia(historia_id):
        """Obtiene los diagnósticos de una historia clínica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, diagnostico, observaciones 
                FROM diagnosticos 
                WHERE historia_id = ?
            """, (historia_id,))
            return cursor.fetchall()

    @staticmethod
    def add_diagnostico(historia_id, diagnostico, observaciones):
        """Agrega un nuevo diagnóstico."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO diagnosticos (historia_id, diagnostico, observaciones) 
                VALUES (?, ?, ?)
            """, (historia_id, diagnostico, observaciones))
            conn.commit()

    @staticmethod
    def update_diagnostico(diagnostico_id, diagnostico, observaciones):
        """Actualiza un diagnóstico existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE diagnosticos 
                SET diagnostico = ?, observaciones = ? 
                WHERE id = ?
            """, (diagnostico, observaciones, diagnostico_id))
            conn.commit()
