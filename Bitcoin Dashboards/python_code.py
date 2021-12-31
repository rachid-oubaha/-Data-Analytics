#--------------------------|scraping data|----------------------------
import requests
import json
import pandas as pd
import datetime as dt


url = 'https://api.binance.com/api/v3/klines?limit=100000'
symbol = 'BTCUSDT'
interval = '1d'
h = 24*1000 # 1000 days
end = dt.datetime.now()
start = end - dt.timedelta(hours = h)

start = str(int(start.timestamp()*1000))
end = str(int(end.timestamp()*1000))

par = {'symbol': symbol, 'interval': interval, 'startTime': start, 'endTime': end}
columns = ['datetime', 'open', 'high', 'low', 'close', 'volume','close_time', 'qav', 'num_trades','taker_base_vol', 'taker_quote_vol', 'ignore']
print(len(json.loads(requests.get(url, params= par).text)))
data = pd.DataFrame(json.loads(requests.get(url, params= par).text),columns=columns)
#format columns name
data.index = [dt.datetime.fromtimestamp(x/1000.0) for x in data.datetime]
data.datetime = pd.to_datetime(data.datetime, unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')

data["open"] = data.open.astype(float)
data["high"] = data.high.astype(float)
data["low"] = data.low.astype(float)
data["close"] = data.close.astype(float)
data["volume"] = data.volume.astype(float)

#--------------------------|time series|----------------------------
#--------------------------|ExponentialSmoothing|-------------------
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

model = ExponentialSmoothing(dataset["close"].astype(float),trend='mul',seasonal='mul',seasonal_periods=12).fit()
rangee = pd.date_range('29-12-2021',periods=100,freq='d')
predictions = model.forecast(100)
predictions_range = pd.DataFrame({'Close':predictions,'Day':rangee})
#-------------------------------|ARIMA|-----------------------------
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

model = ARIMA(dataset["close"].astype(float),order=(5,1,0)).fit()
model = model.fit()
rangee = pd.date_range('29-12-2021',periods=100,freq='d') # we can use dt.datetime.now()
predictions = model.forecast(100)
predictions_range = pd.DataFrame({'Close':predictions,'Day':rangee})
#--------------------------------------------------------------------