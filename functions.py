import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# obteniendo los datasets
transacciones_final = pd.read_parquet('app/data/transacciones_final.parquet')
usuarios_movii = pd.read_parquet('app/data/usrs_movii.parquet')
# Dataset para las coordenadas de las ciudades,  recurso: https://simplemaps.com
dfcol = pd.read_excel('app\data\mapa_colombia.xlsx')
# Merge
df_merge = transacciones_final.merge(usuarios_movii, how='left', on='usr_id')
df_merge.rename(columns={'labels_x':'etiqueta_transaccion','labels_y':'etiqueta_usuarios', 'id':'id_transaccion'}, inplace = True)
df_merge.drop(columns=['year','month'], inplace=True)

def mapa_ciudad(x = df_merge['city']):
    dflist = pd.DataFrame(x)
    # Seleccion de las ciudades presentes
    mapa = px.scatter_mapbox(
        dflist.groupby("city", as_index=False).size().merge(dfcol, on="city"),
        lat="lat",
        lon="lng",
        hover_name="city",
        center=go.layout.mapbox.Center(lat=4.5,lon=-74),
            size="size").update_layout(mapbox={"style": "carto-positron", "zoom": 4}, margin={"t":0,"b":0,"l":0,"r":0})

    return mapa

def dibujar_tabla(id_user = 3249216):
    filter = df_merge.loc[df_merge['usr_id']==id_user]
    filter2 = filter.sort_values(by='fecha_transaccion', ascending = False)
    filter2 = filter2[['fecha_transaccion','id_transaccion','nombre_producto','producto','sub_producto', 'tipo_deposito','nro_transaccion', 'trx_activo', 'movilizado','Anomaly_Score','Anomaly']]
    columns = [i for i in filter2.columns]
    rows = [[i for i in row] for row in filter2.T.itertuples()]
    fig = go.Figure(data=[go.Table(
    columnorder = [1,2,3,4,5,6,7,8,9,10],
    columnwidth = [60,60,60,60,60,60,60,60,60,60],
    header= dict(
    values = [i for i in filter2.columns],
    line_color='darkslategray',
    fill_color='royalblue',
    align=['left','center'],
    font=dict(color='white', size=12),
    height=60
    ),
    cells=dict(
    values=filter2.T.values,
    line_color='darkslategray',
    fill=dict(color=['paleturquoise', 'white']),
    align=['center', 'center'],
    font_size=10,
    height=50)
    )
    ])
    fig.update_layout(autosize=False,width=1000,height=300,margin=dict(l=0,r=0,b=0,t=0,pad=0))
    return fig

def anomaly_scoring(id_user = 3249216):
    filter3 = df_merge[df_merge['usr_id'] == id_user][["movilizado", "Anomaly_Score","Anomaly",'fecha_transaccion']]
    filter3 = filter3.sort_values(by='fecha_transaccion')
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = round(filter3.Anomaly_Score.mean(),2),
        title = {"text": "ANOMALY SCORING<br><span style='font-size:0.8em;color:gray'>average value</span>"},
        delta = {'reference': 0, 'relative': False, "valueformat": ".0f"},
        domain = {'x': [0,0 ], 'y': [0,0]}))
    fig.update_layout(autosize=True,width=400,height=200,margin=dict(l=0,r=0,b=0,t=0,pad=0))
    return fig

def acumulado_anormal():
    fraudes = df_merge[df_merge['Anomaly'] == True][["id_transaccion",'genero',"usr_id","producto","movilizado", "Anomaly_Score","Anomaly",'fecha_transaccion']]
    id_user = len(fraudes['usr_id'].unique())
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = id_user,
        title = {"text": "<span style='font-size:0.8em;color:gray'>ACCUMULATED ABNORMAL USERS</span><br>"},
        delta = {'relative': True},
        domain = {'x': [0, 0], 'y': [0, 0]}))
    fig.update_layout(autosize=True,width=500,height=250,margin=dict(l=0,r=0,b=0,t=0,pad=0))
    return fig

def acumulado_anormal_tran():
    fraudes = df_merge[df_merge['Anomaly'] == True][["id_transaccion",'genero',"usr_id","producto","movilizado", "Anomaly_Score","Anomaly",'fecha_transaccion']]
    id_transaccion = len(fraudes['id_transaccion'].unique())
    fig = go.Figure()
    fig.add_trace(go.Indicator(
    mode = "number+delta",
    value = id_transaccion,
    title = {"text": "<span style='font-size:0.8em;color:gray'>ACCUMULATED ABNORMAL TRANSACTIONS</span><br>"},
    delta = {'relative': True},
    domain = {'x': [0, 0], 'y': [0, 0]}))
    fig.update_layout(autosize=True,width=500,height=250,margin=dict(l=0,r=0,b=0,t=0,pad=0))
    return fig

def filtro_resumen(startdate, enddate, product):
    filtro1 = df_merge[df_merge['Anomaly'] == True][['fecha_transaccion', 'nombre_producto','tipo_deposito', 'producto', 'sub_producto','movilizado', 'trx_activo', 'nro_transaccion', 'etiqueta_transaccion', 'Anomaly', 'Anomaly_Score']]
    startdate = "2021-02-01"
    enddate = '2021-02-02'
    product = 'CB'
    startdate = pd.to_datetime(startdate, format="%Y-%m-%d")
    enddate = pd.to_datetime(enddate, format="%Y-%m-%d")
    filtro2 = filtro1[(filtro1['fecha_transaccion'] >= startdate) & (filtro1['fecha_transaccion'] <= enddate)]
    filtro3 = filtro2[filtro2['producto'] == product]
    num_anomalos_filtrados = filtro3.Anomaly.sum()
    filtro3 =filtro3[['tipo_deposito','sub_producto', 'movilizado', 'trx_activo', 'nro_transaccion','etiqueta_transaccion', 'Anomaly_Score']]
    # Nuero de anomalas 
    filtro4 = filtro3.groupby(['sub_producto'])['movilizado','Anomaly_Score','nro_transaccion'].sum()
    filtro4 = filtro4.sort_values(by='movilizado', ascending = False)
    filtro4 = filtro4.reset_index()
    filtro5 = filtro4.query('movilizado > 0')
    columns = [i for i in filtro5.columns]
    rows = [[i for i in row] for row in filtro5.T.itertuples()]
    fig = go.Figure(data=[go.Table(
    # columnorder = [1,2,3,4,5,6,7,8,9,10],
    # columnwidth = [60,60,60,60,60,60,60,60,60,60],
    header= dict(
    values = [i for i in filtro5.columns],
    line_color='darkslategray',
    fill_color='royalblue',
    align=['left','center'],
    font=dict(color='white', size=12),
    height=60
    ),
    cells=dict(
    values=filtro5.T.values,
    line_color='darkslategray',
    fill=dict(color=['paleturquoise', 'white']),
    align=['center', 'center'],
    font_size=10,
    height=50)
    )
    ])
    fig.update_layout(autosize=False,width=1000,height=300,margin=dict(l=0,r=0,b=0,t=0,pad=0))
    return fig