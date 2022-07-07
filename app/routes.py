from app import app
from forms import InfoForm,DataStore
from functions import mapa_ciudad
from requests import session
from flask import redirect, render_template, url_for, flash, request
import pandas as pd
import json
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

data = DataStore()

#########################
######## RUTAS ##########
#########################

@app.route("/",methods=['GET','POST'])
def index():
    form = InfoForm(request.form)
    form.producto.choices = list(df_merge['producto'].unique())
    form.subproducto.choices = list(df_merge['sub_producto'].unique())
    if form.validate_on_submit():
        startdate = form.startdate.data
        print(startdate)
        data.ini = startdate
        enddate = form.enddate.data
        print(enddate)
        data.fin = enddate
        product = form.producto.data
        print(product)
        data.pro = product
        subproduct = form.subproducto.data
        print(subproduct)
        data.sub = subproduct
        return redirect(url_for("summary_report",startdate=startdate))
    frad_location = df_merge[df_merge['Anomaly']==True]
    fig2 = mapa_ciudad(frad_location['city'])
    graphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("report.html", form = form, title = "Reports", graph0 = graphJSON)

@app.route("/summary_report",methods=['GET','POST'])
def summary_report():
    startdate = data.ini
    enddate = data.fin
    product = data.pro
    subproduct = data.sub
    stardate = pd.to_datetime(data.ini, format="%Y-%m-%d")
    print(stardate)
    enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    print(enddate)
    print(product)
    print(subproduct)
    return render_template("report_filtered.html", startdate=startdate, enddate = enddate, producto=product, subproducto=subproduct)


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

    return render_template("user_filtered.html", usuario=id_user)