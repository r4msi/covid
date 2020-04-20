import streamlit as st
from procesado import *
from plots import *
from models import Models


st.sidebar.title('Índice')
section_ind = st.sidebar.radio('',['Gráficos', 'Predicciones'])

st.title("COVID-19 en España")
st.markdown("¡Bienvenido! El propósito de esta web es predecir la evolución de la pandemia en España.")
st.write(":iphone: *Si se accede desde el móvil es recomendable rotar la pantalla.*")
st.write(":bar_chart: *Todos los gráficos son interactivos. Para volver al modo original: doble toque/click.*")

def get_data():
    data = Process().cleaning()
    return data


df = get_data()

if section_ind == "Gráficos":


    st.header("Mapa Interactivo CCAA:")

    st.plotly_chart(MapPlot().Map())

    fig = DailyPlots(dt=df).infected()
    st.plotly_chart(fig)

    fig = DailyPlots(dt=df).deaths()
    st.plotly_chart(fig)

    st.write(":exclamation: *A partir del 8 de Abril se dejaron de reportar los ingresos en la UCI/Hospitalizados. Han sido imputados con ExtraTreesRegressor (parecido a Random Forest).*")

    fig = DailyPlots(dt=df).all_imputed()
    st.plotly_chart(fig)


if section_ind == "Predicciones":
    data_lag, forecast = ProccesModel(data = df).features()
    st.header("Predicción")
    st.write(":sauropod: *Para automatizar el proyecto y su adaptabilidad en función del tiempo, SARIMAX se estima con auto_arima (escoge los parámetros que minimizan el AIC). Por tanto, puede tardar unos segundos extras en cargar. *")

    options = st.selectbox(
        label="Modelo a elegir",
        options = ["OLS", "SARIMAX"]
    )
    if options == "OLS":
        p, fig, sum = Models(data=df, data_lag=data_lag, forecast = forecast ).fit_ols()
        st.plotly_chart(fig)
        st.markdown("Se reportal la raiz del error cuadrático medio")
        st.latex(r'\epsilon = \sum^i_1\dfrac{(\hat{y}-y_i)^2}{N}')
        st.table(p)
        st.header("Calidad del Modelo")
        st.text(sum)
    else:
        p, fig, summary = Models(data=df, data_lag=data_lag, forecast = forecast ).fit_sarimax()
        st.plotly_chart(fig)
        st.table(p)
        st.header("Calidad del Modelo")
        st.text(summary)
