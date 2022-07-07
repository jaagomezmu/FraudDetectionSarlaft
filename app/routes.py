from tracemalloc import start
from app import app
from forms import InfoForm
from functions import mapa_ciudad
from requests import session
from flask import redirect, render_template, url_for, flash, request
import pandas as pd
import json
import datetime
import plotly
import plotly.express as px

# obteniendo los datasets
transacciones_final = pd.read_parquet('app/data/transacciones_final.parquet')
usuarios_movii = pd.read_parquet('app/data/usrs_movii.parquet')
# Dataset para las coordenadas de las ciudades,  recurso: https://simplemaps.com
dfcol = pd.read_excel('app\data\mapa_colombia.xlsx')
# Merge
df_merge = transacciones_final.merge(usuarios_movii, how='left', on='usr_id')
df_merge.rename(columns={'labels_x':'etiqueta_transaccion','labels_y':'etiqueta_usuarios', 'id':'id_transaccion'}, inplace = True)
df_merge.drop(columns=['year','month'], inplace=True)

startdate = ''
enddate = ''
producto = ''
subproducto = ''
#########################
######## RUTAS ##########
#########################

@app.route("/",methods=['GET','POST'])
def index():
    form = InfoForm()
    form.producto.choices = list(df_merge['producto'].unique())
    form.subproducto.choices = list(df_merge['sub_producto'].unique())
    if form.validate_on_submit():
        startdate = form.startdate.data
        print(startdate)
        session['startdate'] = startdate
        enddate = form.enddate.data
        print(enddate)
        session['enddate']=enddate
        product = form.producto.data
        print(product)
        session['product']=product
        subproduct = form.subproducto.data
        print(subproduct)
        session['subproduct']=subproduct
        return redirect(url_for("summary_report"))
    frad_location = df_merge[df_merge['Anomaly']==True]
    fig2 = mapa_ciudad(frad_location['city'])
    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report.html", form = form, title = "Reports", graph0 = graphJSON)

@app.route("/summary_report",methods=['GET','POST'])
def summary_report():
    form = InfoForm()
    stardate = pd.to_datetime(stardate, infer_datetime_format="%Y-%m-%d")
    print(stardate)
    stardate = pd.to_datetime(enddate, infer_datetime_format="%Y-%m-%d")
    print(producto)
    print(subproducto)
    df = df_merge[(df_merge['fecha_transaccion']>= stardate)&(df_merge['fecha_transaccion']<= enddate)]
    df['producto'] = df['producto'].cat.remove_unused_categories()
    validacion1 = producto in list(df['producto'])
    if validacion1 == True:
        df2 = df[df['producto']== producto]
    else:
        new_message = 'product is not reported'
        flash(new_message)
    fig = px.line(df2, x='fecha_transaccion', y='movilizado', color='producto')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report_filtered.html",form = form, graph0 = graphJSON)


@app.route("/new_user",methods=['GET','POST'])
def new_user():
    form2 = InfoForm()
    q = request.args.get('q', type=int)
    usrs = q in list(df_merge['usr_id'])
    fail_message = 'User {} not found'.format(q)
    success_message = 'User {} found in database'.format(q)
    if usrs == True:
        global id_user
        id_user = q
        flash(success_message)
        global df
        df = df_merge[df_merge['usr_id']==id_user]
    else:
        flash(fail_message)
    return render_template("user.html", form=form2)

@app.route("/user_summary_report", methods=['GET','POST'])
def user_summary_report():

    return render_template("user_filtered.html")