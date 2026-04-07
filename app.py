from flask import Flask, request, jsonify, session, render_template, redirect
import json, os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

DB = "users.json"

def load():
    if os.path.exists(DB):
        return json.load(open(DB))
    return {}

def save(d):
    json.dump(d, open(DB,"w"), indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dash():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    db = load()

    if data["username"] in db:
        return jsonify({"error":"User exists"})

    db[data["username"]] = {
        "password": generate_password_hash(data["password"]),
        "accounts":[]
    }

    save(db)
    return jsonify({"message":"Registered"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    db = load()

    if data["username"] not in db:
        return jsonify({"error":"Not found"})

    if not check_password_hash(db[data["username"]]["password"], data["password"]):
        return jsonify({"error":"Wrong password"})

    session["user"] = data["username"]
    return jsonify({"message":"Logged in"})

@app.route("/add_account", methods=["POST"])
def add_acc():
    db = load()
    user = session.get("user")

    db[user]["accounts"].append(request.json)
    save(db)
    return jsonify({"ok":True})

@app.route("/accounts")
def accounts():
    db = load()
    return jsonify(db[session["user"]]["accounts"])

app.run()
