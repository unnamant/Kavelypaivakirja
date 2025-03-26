import db

def add_items(title, description, distance, city, user_id):
    sql = """INSERT INTO items (title, description, distance, city, user_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, distance, city, user_id])
