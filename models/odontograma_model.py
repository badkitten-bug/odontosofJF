import sqlite3
from database.db_config import connect_db

class OdontogramaModel:
    @staticmethod
    def get_odontograma(historia_id):
        """Obtiene el odontograma de una historia clínica."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tooth_number, condition, notes FROM odontogram WHERE historia_id = ?", (historia_id,))
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def save_odontograma(historia_id, dientes_data):
        """Guarda los datos del odontograma para una historia clínica."""
        conn = connect_db()
        cursor = conn.cursor()
        for diente, condition, notes in dientes_data:
            cursor.execute(
                "INSERT INTO odontogram (historia_id, tooth_number, condition, notes, date) VALUES (?, ?, ?, ?, datetime('now'))",
                (historia_id, diente, condition, notes)
            )
        conn.commit()
        conn.close()

    @staticmethod
    def update_odontograma(odontograma_id, condition, notes):
        """Actualiza la información de un diente en el odontograma."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE odontogram SET condition = ?, notes = ? WHERE id = ?",
            (condition, notes, odontograma_id)
        )
        conn.commit()
        conn.close()
