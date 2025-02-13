from database.db_config import connect_db

class DocumentTypeModel:
    @staticmethod
    def load_document_types():
        """Carga todos los tipos de documentos."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM document_types")
            return cursor.fetchall()

    @staticmethod
    def get_document_type_by_id(doc_type_id):
        """Obtiene un tipo de documento por su ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM document_types WHERE id = ?", (doc_type_id,))
            return cursor.fetchone()

    @staticmethod
    def add_document_type(name):
        """Agrega un nuevo tipo de documento."""
        with connect_db() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO document_types (name) VALUES (?)", (name,))
                conn.commit()
            except Exception as e:
                raise ValueError(f"Error al agregar el tipo de documento: {e}")

    @staticmethod
    def update_document_type(doc_type_id, name):
        """Actualiza un tipo de documento existente."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE document_types SET name = ? WHERE id = ?", (name, doc_type_id))
            conn.commit()

    @staticmethod
    def delete_document_type(doc_type_id):
        """Elimina un tipo de documento."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM document_types WHERE id = ?", (doc_type_id,))
            conn.commit()
