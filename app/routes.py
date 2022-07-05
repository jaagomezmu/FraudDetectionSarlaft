from html.entities import html5
from requests import session
from app import app
from flask import redirect, render_template, url_for, session
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
import pandas as pd
import json
import datetime
import plotly
import plotly.express as px
from functions import mapa_ciudad

class InfoForm(FlaskForm):
    startdate = DateField('Start date', format = '%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End date', format = '%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

transactions = pd.read_parquet('app/data/sample_transactions.parquet')
transactions['producto'] = transactions['producto'].cat.remove_unused_categories()
users = pd.read_parquet('app/data/sample_users.parquet')

@app.route("/")
def index():
    return render_template("index.html", title = "Home")

@app.route("/report", methods=['GET','POST'])
def report():
    form = InfoForm()
    if form.validate_on_submit():
        session['startdate'] = form.startdate.data
        session['enddate'] = form.enddate.data
        return redirect(url_for('report_filtered'))
    
    fig = px.bar(transactions, x='fecha_transaccion', y='movilizado', color='producto')
    fig2 = mapa_ciudad()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report.html", form = form, title = "Reports",graph0 = graphJSON, graph1 = graphJSON2)

@app.route("/report_filtered", methods=['GET','POST'])
def report_filtered():
    stardate = datetime.datetime.strptime(session['startdate'],"%a, %d %b %Y %H:%M:%S GMT")
    enddate = datetime.datetime.strptime(session['enddate'],"%a, %d %b %Y %H:%M:%S GMT")
    df = transactions[(transactions['fecha_transaccion']>= stardate)&(transactions['fecha_transaccion']<= enddate)]
    df['producto'] = df['producto'].cat.remove_unused_categories()
    fig = px.bar(df, x='fecha_transaccion', y='movilizado', color='producto')
    fig2 = mapa_ciudad()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report_filtered.html",graph0 = graphJSON, graph1 = graphJSON2)


@app.route("/user")
def user():
    
    fig = px.histogram(users, x='genero')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("user.html", title = "Users",graphJSON=graphJSON)