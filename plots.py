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
