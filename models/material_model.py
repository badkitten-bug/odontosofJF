# models/material_model.py
from database.db_config import connect_db

class MaterialModel:
    @staticmethod
    def create_table():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    description TEXT,
                    unit_cost REAL NOT NULL,
                    status TEXT DEFAULT 'Activo'
                )
            ''')
            conn.commit()

    @staticmethod
    def get_all():
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materials WHERE status = 'Activo'")
            return cursor.fetchall()

    @staticmethod
    def add_material(data):
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO materials (name, description, unit_cost, status)
                VALUES (?, ?, ?, ?)
            ''', data)
            conn.commit()
