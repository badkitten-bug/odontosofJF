from database.db_config import connect_db

class SpecialtyModel:
    @staticmethod
    def load_specialties():
        """Carga todas las especialidades."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, estado FROM specialties")
            return cursor.fetchall()
    @staticmethod
    def load_doctor_specialties():
        """Carga las especialidades asociadas a los doctores."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT d.id, s.nombre 
                FROM doctors d
                JOIN specialties s ON d.especialidad_id = s.id
            """)
            return cursor.fetchall()

    @staticmethod
    def get_specialty_by_id(specialty_id):
        """Obtiene una especialidad por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, estado FROM specialties WHERE id = ?", (specialty_id,))
            return cursor.fetchone()

    @staticmethod
    def add_specialty(nombre, descripcion, estado="Activo"):
        """Agrega una nueva especialidad a la base de datos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            # Check if the specialty already exists
            cursor.execute("SELECT id FROM specialties WHERE nombre = ?", (nombre,))
            existing_specialty = cursor.fetchone()

            if existing_specialty:
                raise ValueError(f"La especialidad '{nombre}' ya existe.")
            
            # Insert the new specialty
            cursor.execute(
                "INSERT INTO specialties (nombre, descripcion, estado) VALUES (?, ?, ?)",
                (nombre, descripcion, estado)
            )
            conn.commit()

    @staticmethod
    def update_specialty(specialty_id, nombre, descripcion, estado):
        """Actualiza una especialidad existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE specialties SET nombre = ?, descripcion = ?, estado = ? WHERE id = ?",
                (nombre, descripcion, estado, specialty_id)
            )
            conn.commit()

    @staticmethod
    def delete_specialty(specialty_id):
        """Elimina una especialidad de la base de datos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM specialties WHERE id = ?", (specialty_id,))
            conn.commit()