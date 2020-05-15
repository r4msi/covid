import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt



class DailyPlots:

    def __init__(self, dt):
        self.dt = dt

    def infected(self):
        fig = px.bar(
            self.dt
            , x="fecha"
            , y='casos_total'
            , color="casos_total"
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
        fig = px.line()
        fig.add_scatter(
            x = self.dt.fecha,
            y=self.dt.casos_total,
            mode = "lines",
            name="Nuevos Contagios"
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
        # fig.update_layout(
        #     autosize=False,
        #     width=500,
        #     height=500
        # )

        return fig


class Pcr:
    @st.cache
    def __init__(self):
        self.dt = pd.read_csv(
            "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv",
             parse_dates=["fecha"]
             )
        self.dt = self.dt.loc[self.dt["fecha"]>"2020-04-20", ["fecha", "casos_pcr"]]
        self.dt.casos_pcr = pd.DataFrame.diff(self.dt.casos_pcr)
        self.dt.loc[self.dt.fecha == "2020-04-29","casos_pcr"] = 2144
        self.dt.loc[self.dt.fecha=="2020-05-10",["casos_pcr"]] = 621

    def pcr(self):
        fig = px.bar(
            self.dt
            , x="fecha"
            , y='casos_pcr'
                , color="casos_pcr"
                , title="PCR"
                , color_continuous_scale=px.colors.sequential.Sunsetdark
            )

        return fig

class MapPlot:

    def __init__(self, dt):
        self.dt = dt

    def Map(self):
        px.set_mapbox_access_token(
            "pk.eyJ1IjoicjRtc2kiLCJhIjoiY2s4enhvZ2Z6MDBkajNpbnoxNGRwMGV6MSJ9.2zKymbQhYrmC-YwSaJUNbQ")
        communities_map = px.scatter_mapbox(
            self.dt,
            lat="lat",
            lon="lon",
            color="casos_total",
            size="casos_total",
            color_continuous_scale=px.colors.sequential.Reds,
            size_max=40,
            zoom=4,
            hover_name="CCAA",
            opacity=0.8
        )

        return communities_map

class HeatMap:
    def __init__(self, data):
        self.dt = data

    def heat(self):
        fig = plt.figure()
        sns.heatmap(
        pd.concat([
            self.dt,
            pd.get_dummies(self.dt[["weekday"]], drop_first=True)
            ], axis=1
        ).corr("spearman"),
        cmap=sns.diverging_palette(10, 220, as_cmap=True)
        )


        return fig

# numpy==1.16.5
# panda==0.3.1
# plotly==4.6.0
# lxml==4.4.1
# requests==2.22.0
# streamlit==0.57.3
