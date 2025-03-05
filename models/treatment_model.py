import sqlite3
from database.db_config import connect_db  # Asegúrate de importar la conexión a la BD

class TreatmentModel:
    @staticmethod
    def get_all_treatments():
        """Obtiene todos los tratamientos disponibles."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, cost FROM treatments")
            return cursor.fetchall()

    @staticmethod
    def get_treatments_by_historia(historia_id):
        """Obtiene los tratamientos aplicados a una historia clínica específica."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT at.id, t.name, t.description, at.notes
                FROM applied_treatments at
                JOIN treatments t ON at.treatment_id = t.id
                WHERE at.historia_id = ?
            """, (historia_id,))
            return cursor.fetchall()

    @staticmethod
    def apply_treatment(historia_id, treatment_id, notes, appointment_id=None):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO applied_treatments (historia_id, treatment_id, notes, appointment_id)
                VALUES (?, ?, ?, ?)
            """, (historia_id, treatment_id, notes, appointment_id))
            conn.commit()
            
    @staticmethod
    def add_treatment(name, description, cost):
        """Agrega un nuevo tratamiento."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO treatments (name, description, cost) VALUES (?, ?, ?)", 
                           (name, description, cost))
            conn.commit()

    @staticmethod
    def update_treatment(treatment_id, name, description, cost):
        """Actualiza un tratamiento existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE treatments SET name=?, description=?, cost=? WHERE id=?", 
                           (name, description, cost, treatment_id))
            conn.commit()

    @staticmethod
    def delete_treatment(treatment_id):
        """Elimina un tratamiento."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM treatments WHERE id=?", (treatment_id,))
            conn.commit()
