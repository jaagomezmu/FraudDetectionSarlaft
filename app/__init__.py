from flask import Flask

app = Flask(__name__)
app.secret_key = "cambiar_la_contraseña"

from app import routes

