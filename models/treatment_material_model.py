# models/treatment_material_model.py
from database.db_config import connect_db

class TreatmentMaterialModel:
    @staticmethod
    def create_table():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS treatment_materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    treatment_id INTEGER NOT NULL,
                    material_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (treatment_id) REFERENCES treatments(id),
                    FOREIGN KEY (material_id) REFERENCES materials(id)
                )
            ''')
            conn.commit()

    @staticmethod
    def get_by_treatment(treatment_id):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.name, tm.quantity
                FROM treatment_materials tm
                JOIN materials m ON tm.material_id = m.id
                WHERE tm.treatment_id = ?
            ''', (treatment_id,))
            return cursor.fetchall()

    @staticmethod
    def add_relation(data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO treatment_materials (treatment_id, material_id, quantity)
                VALUES (?, ?, ?)
            ''', data)
            conn.commit()
