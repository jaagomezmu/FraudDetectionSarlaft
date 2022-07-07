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
            size="size").update_layout(mapbox={"style": "carto-positron", "zoom": 4}, margin={"t":0,"b":50,"l":0,"r":0})

    return mapa