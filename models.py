import pickle
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
from statsmodels.regression.linear_model import OLS
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX

def coeficientes(mod, x, y):
    coef = []
    for i in range(0,len(x.columns)):
        coef.append(f"{x.columns[i]} : {np.exp(mod.coef_[i])}")
    coef.append(f"R2 : {mod.score(x,y)}")
    return coef

class Models:
    def __init__(self, data, data_lag, forecast):
        self.dt = data
        self.data_lag = data_lag
        self.forecast = forecast

    def fit_log_ols(self):

        self.data_lag["casos"] = np.log(self.data_lag["casos"]+1)
        self.data_lag["fallecimientos"] = np.log(self.data_lag["fallecimientos"]+1)
        self.forecast["casos"] = np.log(self.forecast["casos"]+1)
        self.data_lag.loc[self.data_lag.fecha<="2020-04-04","days"] = 30

        # Calcular el error de hoy
        ts_ols = LinearRegression().fit(self.data_lag.iloc[:-2,].drop(["fecha","fallecimientos"],axis=1),self.data_lag.iloc[:-2,].fallecimientos)
        predictions = pd.DataFrame(
            np.exp(ts_ols.predict(self.forecast.drop("fecha", axis=1)))
        )
        e = pd.DataFrame({
        "Modelo" : "Log(OLS)",
        "Predicción de hoy" : [predictions.iloc[0,0]],
        "Error de hoy": [abs(predictions.iloc[0,0] - self.dt.loc[len(self.dt)-1,"fallecimientos"])]})

        # Predicciones
        ts_ols = LinearRegression().fit(self.data_lag.drop(["fecha","fallecimientos"],axis=1),self.data_lag.fallecimientos)
        sum = coeficientes(
            ts_ols,
            self.data_lag.drop(["fecha", "fallecimientos"],axis=1),
            self.data_lag.fallecimientos
        )
        predictions = pd.DataFrame(
            np.exp(ts_ols.predict(self.forecast.drop("fecha", axis=1)))
        )

        predictions["fecha"] = self.dt.loc[len(self.dt)-1, "fecha"]
        predictions.columns = ["fallecimientos", "fecha"]
        predictions.reset_index(drop=True, inplace=True)
        for i in range(len(self.forecast)):
            c = 0
            c += i
            predictions.loc[i,"fecha"] = predictions.fecha[i] + timedelta(days=c)

        new = pd.concat((self.dt[["fallecimientos","fecha"]],predictions.iloc[1:,:]), axis=0)

        new["Predicciones"] = np.where(new.fecha <= self.dt.loc[len(self.dt)-1, "fecha"], "Real", "Pred")

        fig = px.bar(
            new,
            x = "fecha",
            y = "fallecimientos",
            color = "Predicciones"
        )


        # predictions.columns =["Predicciones_Fallecimientos", "fecha"]
        #
        # load = str(self.dt.loc[len(self.dt)-1, "fecha"] - timedelta(days=1))
        # load = load[0:10] + "log.pkl"
        #
        # with open(load, "rb") as file:
        #     historic = pickle.load(file)
        # predictions["Error"] = 0
        # p=pd.concat([predictions.reset_index(drop=True), historic], ignore_index=True)
        # p = p.loc[p.fecha <= self.dt.loc[len(self.dt)-1, "fecha"],:]
        # p.reset_index(drop=True, inplace=True)
        # for i in range(0,len(p)):
        #     if self.dt.loc[len(self.dt)-1,"fecha"] == p.loc[i,"fecha"]:
        #         p.loc[i,"Error"] = np.sqrt((self.dt.loc[len(self.dt)-1,"fallecimientos"] - p.loc[i,"Predicciones_Fallecimientos"])**2)
        #
        # save = str(self.dt.loc[len(self.dt)-1, "fecha"])
        # save = save[0:10] + "log.pkl"
        #
        # with open(save, "wb") as file:
        #     pickle.dump(p, file)



        return  e, fig, sum

    def fit_ols(self):

        self.data_lag.loc[self.data_lag.fecha<="2020-04-04","days"] = 30
        ts_ols = OLS(
            self.data_lag.iloc[:-2,].fallecimientos,
            self.data_lag.iloc[:-2,].drop(["fecha","fallecimientos"], axis=1)
        ).fit()
        sum = ts_ols.summary()
        predictions = pd.DataFrame(
            ts_ols.predict(self.forecast.drop("fecha", axis=1))
        )

        e = pd.DataFrame({
        "Modelo" : "OLS",
        "Predicción de hoy" : [predictions.iloc[0,0]],
        "Error de hoy": [abs(predictions.iloc[0,0] - self.dt.loc[len(self.dt)-1,"fallecimientos"])]})

        predictions["fecha"] = self.dt.loc[len(self.dt)-1, "fecha"]
        predictions.columns = ["fallecimientos", "fecha"]
        predictions.reset_index(drop=True, inplace=True)
        for i in range(len(self.forecast)):
            c = 0
            c += i
            predictions.loc[i,"fecha"] = predictions.fecha[i] + timedelta(days=c)

        new = pd.concat((self.dt[["fallecimientos","fecha"]],predictions.iloc[1:,:]), axis=0)

        new["Predicciones"] = np.where(new.fecha <= self.dt.loc[len(self.dt)-1, "fecha"], "Real", "Pred")

        fig = px.bar(
            new,
            x = "fecha",
            y = "fallecimientos",
            color = "Predicciones",
        )

        # predictions.columns =["Predicciones_Fallecimientos", "fecha"]
        #
        # load = str(self.dt.loc[len(self.dt)-1, "fecha"] - timedelta(days=1))
        # load = load[0:10] + ".pkl"
        #
        # with open(load, "rb") as file:
        #     historic = pickle.load(file)
        # predictions["Error"] = 0
        # p=pd.concat([predictions.reset_index(drop=True), historic], ignore_index=True)
        # p = p.loc[p.fecha <= self.dt.loc[len(self.dt)-1, "fecha"],:]
        # p.reset_index(drop=True, inplace=True)
        # for i in range(0,len(p)):
        #     if self.dt.loc[len(self.dt)-1,"fecha"] == p.loc[i,"fecha"]:
        #         p.loc[i,"Error"] = np.sqrt((self.dt.loc[len(self.dt)-1,"fallecimientos"] - p.loc[i,"Predicciones_Fallecimientos"])**2)
        #
        # save = str(self.dt.loc[len(self.dt)-1, "fecha"])
        # save = save[0:10] + ".pkl"
        #
        # with open(save, "wb") as file:
        #     pickle.dump(p, file)



        return  e, fig, sum

    def fit_sarimax(self):

        # sarimax= auto_arima(y=self.data_lag[["fallecimientos"]],
        #                    exogenous=self.data_lag[["casos"]],
        #                    start_p=1, start_q=1,
        #                    test='adf',
        #                    max_p=2, max_q=2, m=7,
        #                    start_P=0, seasonal=True,
        #                    d=None, D=1, trace=False,
        #                    error_action='ignore',
        #                    suppress_warnings=True,
        #                    stepwise=True)

        sarimax = SARIMAX(endog=self.data_lag.iloc[:-2,][["fallecimientos"]],
                         exog=self.data_lag.iloc[:-2,][["casos"]],
                         order=(0,0,3),
                         seasonal_order=(0,0,0,0)
        ).fit()

        sum = sarimax.summary()
        predictions = pd.DataFrame(
            sarimax.forecast(steps=6, exog=self.forecast[["casos"]])
        )

        e = pd.DataFrame({
        "Modelo" : "SARIMAX",
        "Predicción de hoy" : [predictions.iloc[0,0]],
        "Error de hoy": [abs(predictions.iloc[0,0] - self.dt.loc[len(self.dt)-1,"fallecimientos"])]})

        predictions["fecha"] = self.dt.loc[len(self.dt)-1, "fecha"]
        predictions.columns = ["fallecimientos", "fecha"]
        predictions.reset_index(drop=True, inplace=True)
        for i in range(len(self.forecast)):
            c = 0
            c += i
            predictions.loc[i,"fecha"] = predictions.fecha[i] + timedelta(days=c)

        new = pd.concat((self.dt[["fallecimientos","fecha"]],predictions.iloc[1:,:]), axis=0)

        new["Predicciones"] = np.where(new.fecha <= self.dt.loc[len(self.dt)-1, "fecha"], "Real", "Pred")

        fig = px.bar(
            new,
            x = "fecha",
            y = "fallecimientos",
            color = "Predicciones",
        )

        # predictions.columns =["Predicciones_Fallecimientos", "fecha"]
        #
        # load = str(self.dt.loc[len(self.dt)-1, "fecha"] - timedelta(days=1))
        # load = load[0:10] + "_.pkl"
        #
        # with open(load, "rb") as file:
        #     historic = pickle.load(file)
        # predictions["Error"] = 0
        # p=pd.concat([predictions.reset_index(drop=True), historic], ignore_index=True)
        # p = p.loc[p.fecha <= self.dt.loc[len(self.dt)-1, "fecha"],:]
        # p.reset_index(drop=True, inplace=True)
        # for i in range(0,len(p)):
        #     if self.dt.loc[len(self.dt)-1,"fecha"] == p.loc[i,"fecha"]:
        #         p.loc[i,"Error"] = np.sqrt((self.dt.loc[len(self.dt)-1,"fallecimientos"] - p.loc[i,"Predicciones_Fallecimientos"])**2)
        #
        # save = str(self.dt.loc[len(self.dt)-1, "fecha"])
        # save = save[0:10] + "_.pkl"
        #
        # with open(save, "wb") as file:
        #     pickle.dump(p, file)


        return  e, fig, sum
