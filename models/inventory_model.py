import sqlite3
from database.db_config import connect_db

class InventoryModel:
    @staticmethod
    def get_all_items():
        """Obtiene todos los productos del inventario."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.id, i.name, i.description, c.name AS category, i.quantity, 
                       i.unit_price, s.name AS supplier, i.status, i.date_added
                FROM inventory i
                LEFT JOIN inventory_categories c ON i.category_id = c.id
                LEFT JOIN suppliers s ON i.supplier_id = s.id
                ORDER BY i.date_added DESC;
            """)
            return cursor.fetchall()

    @staticmethod
    def add_item(name, description, category_id, quantity, unit_price, supplier_id, status):
        """Agrega un nuevo producto al inventario."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (name, description, category_id, quantity, unit_price, supplier_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, description, category_id, quantity, unit_price, supplier_id, status))
            conn.commit()

    @staticmethod
    def update_item(item_id, name, description, category_id, quantity, unit_price, supplier_id, status):
        """Actualiza un producto del inventario."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inventory 
                SET name=?, description=?, category_id=?, quantity=?, unit_price=?, supplier_id=?, status=? 
                WHERE id=?
            """, (name, description, category_id, quantity, unit_price, supplier_id, status, item_id))
            conn.commit()

    @staticmethod
    def delete_item(item_id):
        """Elimina un producto del inventario."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
            conn.commit()
