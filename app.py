import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from pipreqs import *

from procesado import Process
from plots import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

st.title("COVID-19 en España")
st.markdown("¡Bienvenido! El propósito de esta web es predecir la evolución de la pandemia en España.")

st.header("Mapa Interactivo")

tile = st.selectbox(
    label="Seleccionar entre: Casos, Fallecidos, Recuperados",
    options=["casos", "fallecidos", "recuperados"],
    index=0,
)

st.plotly_chart(MapPlot().Map(tile))

def get_data():
    data = Process().cleaning()
    return data


df = get_data()

fig = DailyPlots(dt=df).infected()
st.plotly_chart(fig)

fig = DailyPlots(dt=df).deaths()
st.plotly_chart(fig)

fig = DailyPlots(dt=df).weekend()
st.plotly_chart(fig)

st.sidebar.title('Índice')
section_ind = st.sidebar.radio('',['Gráficos', 'Predicciones'])
