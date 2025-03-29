import db

def add_items(title, description, distance, city, user_id):
    sql = """INSERT INTO items (title, description, distance, city, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, distance, city, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.distance,
                    items.city,
                    users.id user_id,
                    users.username
            FROM items, users
            WHERE items.user_id = users.id
            AND items.id = ? """

    return db.query(sql, [item_id])[0]

def update_items(item_id, title, description, distance, city):
    sql = """UPDATE items SET title = ?,
                            description = ?,
                            distance = ?,
                            city = ?
                        WHERE id = ? """
    db.execute(sql, [title, description, distance, city, item_id])

def delete_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title FROM items
                WHERE title LIKE ? OR description LIKE ?
                ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
