import db
from werkzeug.security import check_password_hash, generate_password_hash

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ? "
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_item(user_id):
    sql = "SELECT id, title FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
            return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
            return user_id
    return None

def delete_user(user_id):
    sql = "DELETE FROM comments WHERE user_id = ?"
    db.execute(sql, [user_id])
    sql = "SELECT id FROM items WHERE user_id = ?"
    items = db.query(sql, [user_id])
    for item in items:
        sql = "DELETE FROM item_classes WHERE item_id = ?"
        db.execute(sql, [item["id"]])
        sql = "DELETE FROM images WHERE item_id = ?"
        db.execute(sql, [item["id"]])
        sql = "DELETE FROM comments WHERE item_id = ?"
        db.execute(sql, [item["id"]])

    sql = "DELETE FROM items WHERE user_id = ?"
    db.execute(sql, [user_id])
    sql = "DELETE FROM users WHERE id = ?"
    db.execute(sql, [user_id])
