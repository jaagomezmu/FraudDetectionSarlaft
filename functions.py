import pandas as pd
import plotly.express as px

def mapa_ciudad():
    ## Ubicaciones de las ciudades, recurso: https://simplemaps.com
    ## Esta linea se debe mantener, se refiere a la lectura de las coordenadas de las ciudades
    dfcol = pd.read_excel('app/data/mapa_colombia.xlsx')
    dfcol['city'] = dfcol['city'].str.lower()
    dfcol['city'] = dfcol['city'].str.replace("á","a")
    dfcol['city'] = dfcol['city'].str.replace("ó","o")
    dfcol['city'] = dfcol['city'].str.replace("í","i")
    ## Lectura de los usuarios
    usuarios = pd.read_parquet('app/data/sample_users.parquet')
    dflist = pd.DataFrame(usuarios['city'])
    # Seleccion de las ciudades presentes
    mapa = px.scatter_mapbox(
        dflist.groupby("city", as_index=False).size().merge(dfcol, on="city"),
        lat="lat",
        lon="lng",
        hover_name="city",
        size="size",
    ).update_layout(mapbox={"style": "carto-positron", "zoom": 4}, margin={"t":0,"b":0,"l":300,"r":250})

    return mapa