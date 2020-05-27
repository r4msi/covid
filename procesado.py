import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta



class Process:

    def __init__(self):
        self.dt = pd.read_csv(
            "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv",
             parse_dates=["fecha"]
        )

    def cleaning(self):
        self.dt.casos_total = self.dt.casos_pcr
        self.dt.drop(["casos_pcr", "casos_test_ac"], axis=1,inplace=True)
        self.dt.altas.fillna(0, inplace=True)
        self.dt.fallecimientos.fillna(0, inplace=True)
        self.dt.loc[:8, "ingresos_uci"].fillna(0, inplace=True)
        self.dt.loc[:8, "hospitalizados"].fillna(0, inplace=True)
        self.dt.casos_total = pd.DataFrame.diff(self.dt.casos_total)
        self.dt.altas = pd.DataFrame.diff(self.dt.altas)
        self.dt.ingresos_uci = pd.DataFrame.diff(self.dt.ingresos_uci)
        self.dt.hospitalizados = pd.DataFrame.diff(self.dt.hospitalizados)
        self.dt.fallecimientos = pd.DataFrame.diff(self.dt.fallecimientos)
        self.dt.iloc[0, 1:6] = 0
        # Cambio en el sistema de recuento.
        self.dt.loc[self.dt.fecha=="2020-04-17",["altas","fallecimientos"]] = [3900, 585]
        self.dt.loc[self.dt.fecha=="2020-04-29",["fallecimientos"]] = 325
        self.dt.loc[self.dt.fecha=="2020-05-22",["fallecimientos"]] = 56
        self.dt.loc[self.dt.fecha=="2020-04-19",["casos_total"]] = 3000
        self.dt.loc[self.dt.fecha=="2020-05-11",["casos_total"]] = 700
        self.dt.loc[self.dt.fecha=="2020-05-22",["casos_total"]] = 446
        self.dt.loc[self.dt.fecha=="2020-05-25",["casos_total"]] = 132
        self.dt.loc[self.dt.fecha=="2020-05-26",["casos_total"]] = 194
        self.dt.loc[self.dt.fecha=="2020-05-27",["casos_total"]] = 231
        self.dt.loc[self.dt.fecha=="2020-05-25",["fallecimientos"]] = 50
        self.dt.loc[self.dt.fecha=="2020-05-26",["fallecimientos"]] = 35
        self.dt.loc[self.dt.fecha=="2020-05-27",["fallecimientos"]] = 39
        # Creación de variables temporales para captar tendencia y estacionalidad.
        self.dt["days"] = datetime.now() - self.dt.fecha
        self.dt["days"] = self.dt.days.apply(lambda x: int(x.days))

        return self.dt

class ProccesModel:
    def __init__(self, data):
        self.dt = data

    def features(self):
        data_lag = self.dt[["fecha","casos_total","days","fallecimientos"]]
        data_lag["casos_total"] = self.dt.casos_total.shift(7).fillna(7)
        data_lag = data_lag.iloc[:-5,:]
        forecast = self.dt.iloc[-5:,[0,1]]

        forecast.reset_index(drop=True, inplace=True)
        for i in range(len(forecast)):
            c = 1
            c += i
            forecast.loc[i,"fecha"] = self.dt.loc[len(self.dt)-1, "fecha"] + timedelta(days=c)
        forecast["days"] = datetime.now() - forecast.fecha
        forecast["days"] = forecast.days.apply(lambda x: int(x.days))

        return data_lag, forecast

class ProcessMap:
    def __init__(self):
        ccaa = pd.read_csv("https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/ccaa_covid19_casos.csv")
        ccaa = ccaa.iloc[:19, [1,len(ccaa.columns)-1]]
        geojson_names = ['Andalucia', 'Aragon', 'Asturias', 'Baleares', 'Canarias', 'Cantabria',
                         'Castilla-La Mancha', 'Castilla-Leon', 'Cataluña', 'Ceuta', 'Valencia', 'Extremadura',
                         'Galicia', 'Madrid', 'Melilla', 'Murcia', 'Navarra', 'Pais Vasco', 'La Rioja']
        ccaa.CCAA = geojson_names
        ccaa.columns = ["CCAA","casos_total"]
        ccaa["lon"] = [
            -4.781781, -0.659680, -5.992278, 2.905567, -15.675631, -4.030503, -3.004896, -4.781781, 1.529704, -5.344635,
            -0.553555, -6.151062, -7.910482, -3.716192, -2.948448, -1.483965, -1.646159, -2.615614, -2.518741
        ]
        ccaa["lat"] = [
            37.462498, 41.519807, 43.291806, 39.571921, 28.340070, 43.196969, 39.581025, 41.753871, 41.798855,35.888737,
            39.400376, 39.191082, 42.757532, 40.494110, 35.291773, 38.001222, 42.667265, 43.043277, 42.274566
        ]
        self.dt = ccaa

    def ret(self):
        return self.dt
