# models/treatment_model.py
from database.db_config import connect_db

class TreatmentModel:
    @staticmethod
    def create_table():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tratamientos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    historia_id INTEGER NOT NULL,
                    tratamiento TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    costo REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (historia_id) REFERENCES historias(id)
                )
            ''')
            conn.commit()

    @staticmethod
    def get_all():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tratamientos WHERE status = 'Activo'")
            return cursor.fetchall()

    @staticmethod
    def add_treatment(data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tratamientos (historia_id, tratamiento, descripcion, costo, fecha, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', data)
            conn.commit()