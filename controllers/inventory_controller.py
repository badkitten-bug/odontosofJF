from models.inventory_model import InventoryModel

class InventoryController:
    def get_all_items(self):
        """Obtiene todos los productos del inventario."""
        return InventoryModel.get_all_items()

    def add_item(self, name, description, category_id, quantity, unit_price, supplier_id, status):
        """Añade un nuevo producto."""
        InventoryModel.add_item(name, description, category_id, quantity, unit_price, supplier_id, status)

    def update_item(self, item_id, name, description, category_id, quantity, unit_price, supplier_id, status):
        """Actualiza un producto."""
        InventoryModel.update_item(item_id, name, description, category_id, quantity, unit_price, supplier_id, status)

    def delete_item(self, item_id):
        """Elimina un producto del inventario."""
        InventoryModel.delete_item(item_id)
