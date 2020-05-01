import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import ExtraTreesRegressor


class Process:

    def __init__(self):
        self.dt = pd.read_csv(
            "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv",
             parse_dates=["fecha"]
        )

    def cleaning(self):
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
        self.dt.loc[self.dt.fecha=="2020-04-18", ["casos_total"]] = 4499.00
        self.dt.loc[self.dt.fecha=="2020-04-24", ["casos_total"]] = 5229.00
        # self.dt.loc[self.dt.fecha=="2020-04-26", ["casos_total"]] = 1729.00
        # self.dt.loc[self.dt.fecha=="2020-04-27", ["casos_total"]] = 1831.00
        self.dt.loc[self.dt.fecha=="2020-04-29",["fallecimientos"]] = 325
        self.dt.loc[self.dt.fecha=="2020-04-29",["casos_total"]] = 3000

        # Imputación de hospitalizados e ingresos en la UCI
        imputer_uci = IterativeImputer(
            estimator=ExtraTreesRegressor(n_estimators=300),
            max_iter=10,
            random_state=0
        )
        imputer_hos = IterativeImputer(
            estimator=ExtraTreesRegressor(n_estimators=300),
            max_iter=10,
            random_state=0
        )
        imputer_uci.fit(self.dt.drop(["hospitalizados","fecha"], axis=1))
        imputer_hos.fit(self.dt.drop(["ingresos_uci","fecha"],axis=1))

        imputed_uci = imputer_uci.transform(self.dt.drop(["hospitalizados","fecha"], axis=1))
        imputed_uci = pd.DataFrame(imputed_uci, columns=[["casos_total", "altas", "fallecimientos", "ingresos_uci"]])

        imputed_hos = imputer_hos.transform(self.dt.drop(["ingresos_uci","fecha"], axis=1))
        imputed_hos = pd.DataFrame(imputed_hos, columns=[["casos_total", "altas", "fallecimientos", "hospitalizados"]])

        self.dt["imputed_uci"] = imputed_uci.iloc[:,3]
        self.dt["imputed_hos"] = imputed_hos.iloc[:,3]

        # Creación de variables temporales para captar tendencia y estacionalidad.
        self.dt["days"] = datetime.now() - self.dt.fecha
        self.dt["days"] = self.dt.days.apply(lambda x: int(x.days))
        self.dt["month"] = self.dt.fecha.apply(lambda x: int(x.month))
        self.dt["weekday"] = self.dt.fecha.apply(lambda x: x.weekday())

        return self.dt

class ProccesModel:
    def __init__(self, data):
        self.dt = data

    def features(self):
        data_lag = self.dt[["fecha","casos_total","days","fallecimientos"]]
        data_lag["casos_total"] = self.dt.casos_total.shift(5).fillna(5)
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
