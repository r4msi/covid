import pandas as pd

dt = pd.read_csv(
        "https://raw.githubusercontent.com/datadista/datasets/master/COVID%2019/nacional_covid19.csv",
         parse_dates=["fecha"]
         )
dt = dt.loc[dt["fecha"]>"2020-04-20", ["fecha", "casos_pcr"]]
dt.casos_pcr = pd.DataFrame.diff(dt.casos_pcr)

print(dt.head())
