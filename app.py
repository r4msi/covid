import streamlit as st
from procesado import *
from plots import *
from models import Models


st.sidebar.title('Contenido:')
section_ind = st.sidebar.radio('',['Gráficos','Mapas', 'Predicciones', 'Datos/Código/Contacto'])

st.title("COVID-19 en España")
check = st.checkbox("Ocultar introducción.")
if not check:
    st.markdown('''
    ¡Bienvenido! El propósito de esta web es predecir la evolución de la pandemia en España.
    El proyecto se concibe como una forma de aprender de uno de los eventos más devastadores para nuestro país y la humanidad.
    Por ello, se ha querido dar un paso al frente y crear un dashboard que aporte:
    - **Automaticidad.** Los datos se actualizan solos y los modelos aprenden de los nuevos datos de manera automática.
    - **Estimación de variables que dejaron de ser reportadas.** (Ingresos en UCI y hospitalizados).
    - **Gráficos claros, visuales y comprensibles.**
    - **Código público.** Disponible en github.
    ''')
    st.write(":arrow_forward: *La flecha superior izquierda permite cambiar de sección. (Gráficos, Mapas y Predicciones).*")
    st.write(":bar_chart: *Todos los gráficos son interactivos. Para volver al modo original: doble toque/click.*")

@st.cache
def get_data():
    data = Process().cleaning()
    return data

df = get_data()

if section_ind == "Gráficos":

    fig = DailyPlots(dt=df).infected()
    st.plotly_chart(fig)

    fig = DailyPlots(dt=df).deaths()
    st.plotly_chart(fig)

    st.write(''':exclamation: *A partir del 8 de Abril se dejaron de reportar los
    ingresos en la UCI/Hospitalizados. Si bien, se pueden estimar a partir de los datos de casos, altas y
    fallecimientos que si son conocidos. Han sido imputados con ExtraTreesRegressor (parecido a Random Forest).*''')

    fig = DailyPlots(dt=df).all_imputed()
    st.plotly_chart(fig)

if section_ind == "Mapas":

    st.header("Mapa interactivo CCAA:")
    st.write("*Incluye tanto las ciudades autónomas de Ceuta y Melilla, como las comunidades extrapeninsulares.*")
    @st.cache
    def dataMap():
        data = ProcessMap().ret()
        return data

    data_map = dataMap()
    st.plotly_chart(MapPlot(data_map).Map())

    st.header("Mapa de calor/Matriz de correlaciones:")
    st.write("*Correlaciones (kendall) de las variables del dataset.*")
    fig = HeatMap(data=df).heat()
    st.pyplot(fig)


if section_ind == "Predicciones":
    check2 = st.checkbox("Mostrar info. de modelos.")
    if check2:
        st.markdown('''
        *Se observa que los fallecimientos están asociados con los nuevos casos de hace 6/7 días.
        Probablemente porque la evolución del paciente en la primera semana es determinante.
        Por ello, la correlación es más alta comparada a los casos de hace 14 días.* **La estrategia es
        predecir los fallecimientos futuros con los casos de hace una semana:**
        - Se calcula el retardo de 7 días de los nuevos casos.
        - Para capturar la tendencia de la pandemia se crea una variable temporal, que son los días desde el inicio de los fallecimientos.
        - Se entrena una regresión lineal y otra las variables en su versión logarítmica (da mejores resultados en test).
        - Se crea un modelo más complejo: SARIMAX, basado en retardos, autoregresión, estacionalidad y medias móviles. No solo recoge la
        evolución de la variable objetivo consigo misma, si no que se introduce la variable de retardos de los casos como exógena para dar soporte
        a las predicciones.
        ''')
    data_lag, forecast = ProccesModel(data = df).features()
    st.header("Predicción:")

    options = st.selectbox(
        label="Modelo a elegir:",
        options = ["Log(OLS)", "OLS", "SARIMAX"]
    )
    if options == "Log(OLS)":
        fig, sum= Models(data=df, data_lag=data_lag, forecast = forecast ).fit_log_ols()
        st.plotly_chart(fig)
        # st.latex(r'\epsilon = \dfrac{\sum^i_1(\hat{y}-y_i)^2}{N}')
        # st.write("*Es decir, el sumatorio de la predicción - lo observado entre N.*")
        # e = np.sum(p.Error)/len(p)
        # e
        # st.table(p.sort_values("fecha",ascending=False).reset_index(drop=True))
        st.header("Calidad del Modelo:")
        st.write("Se muestra la exponencial de los coeficientes (Casos y Days).")
        st.text(sum)


    if options == "OLS":
        fig, sum= Models(data=df, data_lag=data_lag, forecast = forecast ).fit_ols()
        st.plotly_chart(fig)
        st.markdown("*Se reporta la raiz del error cuadrático medio:*")
        # st.latex(r'\epsilon = \dfrac{\sum^i_1(\hat{y}-y_i)^2}{N}')
        # st.write("*Es decir, el sumatorio de la predicción - lo observado entre N.*")
        # e = np.sum(p.Error)/len(p)
        # e
        # st.table(p.sort_values("fecha",ascending=False).reset_index(drop=True))
        st.header("Calidad del Modelo:")
        st.text(sum)
    if options == "SARIMAX":
        fig, summary = Models(data=df, data_lag=data_lag, forecast = forecast ).fit_sarimax()
        st.plotly_chart(fig)
        # st.latex(r'\epsilon = \dfrac{\sum^i_1(\hat{y}-y_i)^2}{N}')
        # st.write("*Es decir, el sumatorio de la predicción - lo observado entre N.*")
        # e = np.sum(p.Error)/len(p)
        # e
        # st.table(p.sort_values("fecha",ascending=False).reset_index(drop=True))
        st.header("Calidad del Modelo:")
        st.text(summary)

if section_ind == 'Datos/Código/Contacto':
    st.markdown('''
    - Repositorio de **github** con el código: https://github.com/r4msi/covid
    - Los **datos** se obtienen de datadista. Gracias por el maravilloso trabajo!: https://github.com/datadista/datasets/tree/master/COVID%2019
    - **Contacto:** manu.am450@gmail.com
        * Si tienes algun comentario para mejorar el proyecto o quieres información técnica sobre series temporales no dudes en contactar.
    - La app está hecha integramente en python con la librería Streamlit. Los servidores heroku.
    ''')
