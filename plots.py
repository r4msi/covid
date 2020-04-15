import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
import requests


class DailyPlots:

    def __init__(self, dt):
        self.dt = dt

    def infected(self):
        fig = px.bar(
            self.dt
            , x="dateRep"
            , y='cases'
            , color="cases"
            , title="Infectados"
            , color_continuous_scale=px.colors.sequential.Sunsetdark

        )
        return fig

    def deaths(self):
        fig = px.bar(
            self.dt
            , x="dateRep"
            , y='deaths'
            , color="deaths"
            , title="Fallecidos"
            , color_continuous_scale=px.colors.sequential.YlOrRd

        )
        return fig

    def weekend(self):
        fig = px.bar(
            self.dt
            , x="dateRep"
            , y='cases'
            , color="weekend"
            , title="Estacionalidad FDS"
        )
        return fig


class MapPlot:

    def __init__(self):
        url = "https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain"
        html = requests.get(url).content
        df_list = pd.read_html(html)
        ccaa = pd.DataFrame(df_list[5])
        ccaa = ccaa.iloc[:19, [0, 1, 4, 5]]
        ccaa.columns = ["name", "casos", "fallecidos", "recuperados"]
        ccaa.casos = ccaa.casos.astype(int)
        ccaa.fallecidos = ccaa.fallecidos.astype(int)
        ccaa.recuperados = ccaa.recuperados.astype(int)
        geojson_names = ['Andalucia', 'Aragon', 'Asturias', 'Baleares', 'Canarias', 'Cantabria',
                         'Castilla-La Mancha', 'Castilla-Leon', 'Cataluña', 'Ceuta', 'Valencia', 'Extremadura',
                         'Galicia', 'Madrid', 'Melilla', 'Murcia', 'Navarra', 'Pais Vasco', 'La Rioja']
        ccaa.name = geojson_names
        ccaa["lon"] = [
            -4.781781, -0.659680, -5.992278, 2.905567, -15.675631, -4.030503, -3.004896, -4.781781, 1.529704, -5.344635,
            -0.553555, -6.151062, -7.910482, -3.716192, -2.948448, -1.483965, -1.646159, -2.615614, -2.518741
        ]
        ccaa["lat"] = [
            37.462498, 41.519807, 43.291806, 39.571921, 28.340070, 43.196969, 39.581025, 41.753871, 41.798855,35.888737,
            39.400376, 39.191082, 42.757532, 40.494110, 35.291773, 38.001222, 42.667265, 43.043277, 42.274566
        ]
        self.dt = ccaa

    def Map(self, tipo):
        px.set_mapbox_access_token(
            "pk.eyJ1IjoicjRtc2kiLCJhIjoiY2s4enhvZ2Z6MDBkajNpbnoxNGRwMGV6MSJ9.2zKymbQhYrmC-YwSaJUNbQ")
        communities_map = px.scatter_mapbox(
            self.dt,
            lat="lat",
            lon="lon",
            color=tipo,
            size=tipo,
            color_continuous_scale=px.colors.sequential.Reds,
            size_max=50,
            zoom=4,
            hover_name="name",
            opacity=0.8
        )

        return communities_map
