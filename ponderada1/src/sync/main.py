from flask import Flask, make_response
from database.database import db
from flask import jsonify, request, render_template
from database.models import User
from flask_jwt_extended import JWTManager, set_access_cookies
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests as http_request

app = Flask(__name__, template_folder="templates")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ponderada1.db"
# initialize the app with the extension
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "botafogo" 
# Seta o local onde o token será armazenado
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)


# Verifica se o parâmetro create_db foi passado na linha de comando
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)


# CRUD 

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(username=data["username"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.username = data["username"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())


# login

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    print(username, password)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    # recupera o token
    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response


# register

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    user = User.query.filter_by(username=username, password=password).first()
    if user is not None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    register_user = http_request.post("http://localhost:5000/users", json={"username": username, "password": password})
    if register_user.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    return render_template("login.html")


# update

@app.route("/user-update", methods=["POST"])
def user_update():
    old_username = request.form.get("old_username", None)
    old_password = request.form.get("old_password", None)
    user = User.query.filter_by(username=old_username, password=old_password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    new_username = request.form.get("new_username", None)
    new_password = request.form.get("new_password", None)
    update_user = http_request.put(f"http://localhost:5000/users/{user.id}", json={"username": new_username, "password": new_password})
    if update_user.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    return render_template("user-login.html")


# delete

@app.route("/user-delete", methods=["POST"])
def user_delete():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    print(username, password)
    user = User.query.filter_by(username=username, password=password).first()
    print(user)
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    register_user = http_request.delete(f"http://localhost:5000/users/{user.id}", json={"username": username, "password": password})
    if register_user.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    return render_template("login.html")

# templates

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")

@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

# token

@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(username=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })