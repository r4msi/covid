import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta


class Process:

    def __init__(self):
        self.dt = pd.read_csv(
            "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv",
            parse_dates=["dateRep"],
            date_parser=lambda x: datetime.strptime(x, "%d/%m/%Y")
        )

    def cleaning(self):
        self.dt = self.dt.loc[self.dt.geoId == "ES",].drop(["countriesAndTerritories", "countryterritoryCode"], axis=1)
        self.dt.sort_values(by="dateRep", inplace=True)
        self.dt = self.dt.iloc[56:, :]
        self.dt.dateRep = self.dt.dateRep - timedelta(days=1)
        self.dt["days"] = datetime.now() - self.dt.dateRep
        self.dt["days"] = self.dt.days.apply(lambda x: int(x.days))
        self.dt["weekday"] = self.dt.dateRep.apply(lambda x: x.strftime("%A"))
        self.dt["weekend"] = np.where((self.dt.weekday == "Saturday") | (self.dt.weekday == "Sunday"),
                                      "weekend",
                                      "labour")
        return self.dt
