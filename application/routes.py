from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px

transactions = pd.read_parquet(r'application\data\sample_transactions.parquet')
users = pd.read_parquet(r'application\data\sample_users.parquet')


@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/report")
def report():
    fig = px.bar(transactions, x='fecha_transaccion', y='movilizado', color='producto')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report.html", title = "Reports",graphJSON=graphJSON)

@app.route("/user")
def user():
    
    fig = px.histogram(users, x='genero')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("user.html", title = "Users",graphJSON=graphJSON)