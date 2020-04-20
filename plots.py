import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json



class DailyPlots:

    def __init__(self, dt):
        self.dt = dt

    def infected(self):
        fig = px.bar(
            self.dt
            , x="fecha"
            , y='casos'
            , color="casos"
            , title="Infectados"
            , color_continuous_scale=px.colors.sequential.Sunsetdark

        )
        return fig

    def deaths(self):
        fig = px.bar(
            self.dt
            , x="fecha"
            , y='fallecimientos'
            , color="fallecimientos"
            , title="Fallecidos"
            , color_continuous_scale=px.colors.sequential.YlOrRd


        )
        return fig

    def all_imputed(self):
        fig = px.line(
            self.dt,
            x="fecha",
            y="casos",
            title = "Estadísticos Imputados"
        )
        fig.add_scatter(
            x =self.dt.fecha,
            y=self.dt.fallecimientos,
            mode="lines",
            name ="Fallecidos"
        )
        fig.add_scatter(
            x =self.dt.fecha,
            y=self.dt.imputed_uci,
            mode="lines",
            name ="Ingresos UCI"
        )
        fig.add_scatter(
            x =self.dt.fecha,
            y=self.dt.imputed_hos,
            mode="lines",
            name ="Hospitalizados"
        )
        fig.add_scatter(
            x =self.dt.fecha,
            y=self.dt.altas,
            mode="lines",
            name ="Altas"
        )
        fig.update_layout(shapes=[
            dict(
                type= 'line',
                yref= 'paper', y0= 0, y1= 1,
                xref= 'x', x0= "2020-04-8", x1= "2020-04-8"
            )
        ])

        return fig


class MapPlot:

    def __init__(self):
        ccaa = pd.read_csv("https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv")
        ccaa = ccaa.iloc[:19, [1,len(ccaa.columns)-1]]
        geojson_names = ['Andalucia', 'Aragon', 'Asturias', 'Baleares', 'Canarias', 'Cantabria',
                         'Castilla-La Mancha', 'Castilla-Leon', 'Cataluña', 'Ceuta', 'Valencia', 'Extremadura',
                         'Galicia', 'Madrid', 'Melilla', 'Murcia', 'Navarra', 'Pais Vasco', 'La Rioja']
        ccaa.CCAA = geojson_names
        ccaa.columns = ["CCAA","Casos"]
        ccaa["lon"] = [
            -4.781781, -0.659680, -5.992278, 2.905567, -15.675631, -4.030503, -3.004896, -4.781781, 1.529704, -5.344635,
            -0.553555, -6.151062, -7.910482, -3.716192, -2.948448, -1.483965, -1.646159, -2.615614, -2.518741
        ]
        ccaa["lat"] = [
            37.462498, 41.519807, 43.291806, 39.571921, 28.340070, 43.196969, 39.581025, 41.753871, 41.798855,35.888737,
            39.400376, 39.191082, 42.757532, 40.494110, 35.291773, 38.001222, 42.667265, 43.043277, 42.274566
        ]
        self.dt = ccaa

    def Map(self):
        px.set_mapbox_access_token(
            "pk.eyJ1IjoicjRtc2kiLCJhIjoiY2s4enhvZ2Z6MDBkajNpbnoxNGRwMGV6MSJ9.2zKymbQhYrmC-YwSaJUNbQ")
        communities_map = px.scatter_mapbox(
            self.dt,
            lat="lat",
            lon="lon",
            color="Casos",
            size="Casos",
            color_continuous_scale=px.colors.sequential.Reds,
            size_max=40,
            zoom=4,
            hover_name="CCAA",
            opacity=0.8

        )

        return communities_map

# numpy==1.16.5
# panda==0.3.1
# plotly==4.6.0
# lxml==4.4.1
# requests==2.22.0
# streamlit==0.57.3
