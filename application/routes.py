from application import app
from flask import render_template, url_for
import pandas as pd
import json
import plotly
import plotly.express as px

@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/report")
def report():
    return render_template("report.html", title = "Reports")

@app.route("/user")
def user():
    return render_template("user.html", title = "Users")