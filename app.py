import re
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import config
import db
import items
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    item = users.get_item(user_id)
    return render_template("show_user.html", user=user, item=item)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_coms(item_id)
    images = items.get_images(item_id)
    return render_template("show_item.html", item=item, classes=classes,
                           comments=comments, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/new_items")
def new_items():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_items.html", classes=classes)

@app.route("/create_items", methods=["POST"])
def create_items():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    distance = request.form["distance"]
    if not re.search("^[1-9][0-9]{0,2}$", distance):
        abort(403)
    city = request.form["city"]
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_items(title, description, distance, city, user_id, classes)

    item_id = db.last_insert_id()

    return redirect("/item/" + str(item_id))

@app.route("/create_com", methods=["POST"])
def create_com():
    require_login()
    check_csrf()

    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    items.add_com(item_id, user_id, description)

    return redirect("/item/" + str(item_id))


@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = items.get_all_classes()
    items.get_classes(item_id)

    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item, classes=classes,
                           all_classes=all_classes)

@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    images = items.get_images(item_id)

    return render_template("images.html", item=item, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "POST":
        check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".png"):
            flash("VIRHE: väärä tiedostomuoto")
            return redirect("/images/" + str(item_id))

        image = file.read()
        if len(image) > 100 * 1024:
            flash("VIRHE: liian suuri kuva")
            return redirect("/images/" + str(item_id))

        items.add_image(item_id, image)
        return redirect("/images/" + str(item_id))

@app.route("/delete_images", methods=["POST"])
def delete_images():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        items.delete_image(item_id, image_id)

    return redirect("/images/" + str(item_id))

@app.route("/update_item", methods=["POST"])
def update_items():
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    distance = request.form["distance"]
    if not re.search("^[1-9][0-9]{0,2}$", distance):
        abort(403)
    city = request.form["city"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_items(item_id, title, description, distance, city, classes)

    return redirect("/item/" + str(item_id))

@app.route("/delete_item/<int:item_id>", methods=["GET", "POST"])
def delete_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_item.html", item=item)

    if request.method == "POST":
        check_csrf()

        if "delete" in request.form:
            items.delete_item(item_id)
            return redirect("/")
        return redirect("/item/" + str(item_id))

@app.route("/delete_user/<int:user_id>", methods=["GET", "POST"])
def delete_user(user_id):
    require_login()

    user = users.get_user(user_id)
    if not user:
        abort(404)
    if user["id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_user.html", user=user)

    if request.method == "POST":
        check_csrf()

        if "delete" in request.form:
            users.delete_user(user_id)
            session.clear()
            return redirect("/")
        return redirect("/user/" + str(user_id))

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []

    return render_template("find_item.html", query=query, results=results)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")
    if len(username) > 20:
        flash("VIRHE: käyttäjätunnus saa olla enintään 20 merkkiä")
        return redirect("/register")

    if len(password1) < 8 or len(password2) < 8:
        flash("VIRHE: salasanan tulee olla enemmän kuin 8 merkkiä")
        return redirect("/register")


    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
