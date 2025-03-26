import db

def add_items(title, description, distance, city, user_id):
    sql = """INSERT INTO items (title, description, distance, city, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, distance, city, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"

    return db.query(sql)

def get_item(item_id):
    sql = """SELECT items.title,
                    items.description,
                    items.distance,
                    items.city,
                    users.username
            FROM items, users
            WHERE items.user_id = users.id
            AND items.id = ? """

    return db.query(sql, [item_id])[0]
