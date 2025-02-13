from models.document_type_model import DocumentTypeModel

class DocumentTypeController:
    def __init__(self):
        self.model = DocumentTypeModel()

    def load_document_types(self):
        """Carga todos los tipos de documentos."""
        return self.model.load_document_types()

    def get_document_type_by_id(self, doc_type_id):
        """Obtiene un tipo de documento por su ID."""
        return self.model.get_document_type_by_id(doc_type_id)

    def add_document_type(self, name):
        """Agrega un nuevo tipo de documento."""
        try:
            self.model.add_document_type(name)
        except ValueError as e:
            raise e

    def update_document_type(self, doc_type_id, name):
        """Actualiza un tipo de documento existente."""
        self.model.update_document_type(doc_type_id, name)

    def delete_document_type(self, doc_type_id):
        """Elimina un tipo de documento."""
        self.model.delete_document_type(doc_type_id)
