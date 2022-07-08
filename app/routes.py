from app import app
from forms import InfoForm,DataStore
from functions import acumulado_anormal, acumulado_anormal_tran, filtro_resumen, mapa_ciudad, dibujar_tabla, anomaly_scoring, acumulado_anormal_tran
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
    filtro1 = df_merge[df_merge['Anomaly'] == True][['fecha_transaccion', 'nombre_producto','tipo_deposito', 'producto', 'sub_producto','movilizado', 'trx_activo', 'nro_transaccion', 'etiqueta_transaccion', 'Anomaly', 'Anomaly_Score']]
    stardate = pd.to_datetime(data.ini, format="%Y-%m-%d")
    print(stardate)
    enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    print(enddate)
    print(product)
    fig =  filtro_resumen(startdate=stardate, enddate=enddate, product=product)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    startdate = pd.to_datetime(startdate, format="%Y-%m-%d")
    enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    filtro2 = filtro1[(filtro1['fecha_transaccion'] >= startdate) & (filtro1['fecha_transaccion'] <= enddate)]
    filtro3 = filtro2[filtro2['producto'] == product]
    anomalos_filtrados = filtro3.Anomaly.sum()
    deltaday = enddate - startdate
    return render_template("report_filtered.html", graph0 = graphJSON,startdate=startdate, enddate = enddate, producto=product, anomalos_filtrados = anomalos_filtrados, deltaday = deltaday, filtered_anomalies = anomalos_filtrados)


@app.route("/new_user",methods=['GET','POST'])
def new_user():
    form2 = InfoForm()
    q = request.args.get('q', type=int)
    usrs = q in list(df_merge['usr_id'])
    fail_message = 'User {} not found'.format(q)
    success_message = 'User {} found in database'.format(q)
    if usrs == True:
        data.ids = q
        id_user =  data.ids
        flash(success_message)
        if form2.validate_on_submit():
            print("Almacenamiento_listo")
            return redirect(url_for("user_summary_report", id_user=id_user))
    else:
        flash(fail_message)
    fig1 = acumulado_anormal()
    graphJSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    fig2 = acumulado_anormal_tran()
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    account1 = len(df_merge[df_merge['Anomaly'] == True]['usr_id'].unique())/len(df_merge['usr_id'].unique())
    account1 = round(account1,2)
    account2 = len(df_merge[df_merge['Anomaly'] == True]['id_transaccion'].unique())/len(df_merge['id_transaccion'].unique())
    account2 = round(account2,2)
    print(account2)
    return render_template("user.html", form=form2, graph0 = graphJSON, graph1 = graphJSON2, account1=account1,account2=account2)

@app.route("/user_summary_report", methods=['GET','POST'])
def user_summary_report():
    id_user = data.ids
    filter3 = df_merge[df_merge['usr_id'] == id_user][["movilizado", "Anomaly_Score","Anomaly",'fecha_transaccion']]
    filter3 = filter3.sort_values(by='fecha_transaccion')
    t_movilized = filter3.movilizado.sum()
    any_risk = filter3.Anomaly.any()
    round_f = round(filter3.Anomaly_Score.mean(),2)
    deltaday = filter3['fecha_transaccion'].max()-filter3['fecha_transaccion'].min()
    fig =  dibujar_tabla(id_user = id_user)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    print('Procesamiento Listo')
    fig2 = anomaly_scoring(id_user = id_user)
    graphJSON2 = json.dumps(fig2,cls = plotly.utils.PlotlyJSONEncoder)
    return render_template("user_filtered.html", graph0 = graphJSON, graph1=graphJSON2, usuario= id_user, t_mobilized = t_movilized,deltaday=deltaday,round_f=round_f,in_or_out=any_risk)