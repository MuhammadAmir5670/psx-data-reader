from concurrent.futures import ThreadPoolExecutor, as_completed, _base
from dateutil.relativedelta import relativedelta
from pandas import DataFrame as container
from bs4 import BeautifulSoup as parser
from collections import defaultdict
from datetime import datetime, date
from typing import Union
from tqdm import tqdm

import threading
import pandas as pd
import numpy as np
import requests
import time


class DataReader:

    def __init__(self):
        self.__history = "https://dps.psx.com.pk/historical"
        self.__symbols = "https://dps.psx.com.pk/symbols"
        self.__local = threading.local()

    @property
    def session(self):
        if not hasattr(self.__local, "session"):
            self.__local.session = requests.Session()
        return self.__local.session

    def tickers(self):
        return pd.read_json(self.__symbols)

    def get_psx_data(self, symbol: str, dates: list) -> container:
        data = futures = []
        
        with tqdm(total=len(dates), desc="Downloading {}'s Data".format(symbol)) as progressbar:

            with ThreadPoolExecutor(max_workers=6) as executor:
                for date in dates:
                    futures.append(executor.submit(self.download, symbol=symbol, date=date))

                for future in as_completed(futures):
                    data.append(future.result())
                    progressbar.update(1)
            
            data = [instance for instance in data if isinstance(instance, container)]
        
        return self.preprocess(data)
    
    def stocks(self, tickers: Union[str, list], start: date, end: date) -> container:
        tickers = [tickers] if isinstance(tickers, str) else tickers
        dates = self.daterange(start, end)

        data = [self.get_psx_data(ticker, dates)[start: end] for ticker in tickers]

        if len(data) == 1:
            return data[0]

        return pd.concat(data, keys=tickers, names=["Ticker", "Date"])


    def download(self, symbol: str, date: date):
        session = self.session
        post = {"month": date.month, "year": date.year, "symbol": symbol}
        with session.post(self.__history, data=post) as response:
            data = parser(response.text, features="html.parser")
            data = self.toframe(data)
        return data

    # def toframe(self, data):
    #     stocks = defaultdict(list)
    #     rows = data.select("tr")
    #     headers = [header.getText() for header in data.select("th")]

    #     for row in rows:
    #         cols = [col.getText() for col in row.select("td")]
        
    #         for key, value in zip(headers, cols):
    #             if key.lower() in ("time", "date"):
    #                 value = datetime.strptime(value, "%b %d, %Y")
    #             stocks[key].append(value)

    #     date_col = next(c for c in headers if c.lower() in ("time", "date"))
    #     return pd.DataFrame(stocks, columns=headers).set_index(date_col)

    def toframe(self, data):
        stocks = defaultdict(list)

        # Extract rows and headers (strip whitespace)
        rows    = data.select("tr")
        headers = [h.get_text(strip=True) for h in data.select("th")]

        # Parse each row
        for row in rows:
            cols = [td.get_text(strip=True) for td in row.select("td")]
            if len(cols) != len(headers):
                continue  # skip incomplete rows

            for key, value in zip(headers, cols):
                if key.lower() in ("time", "date"):
                    # PSX uses format like “Jun 26, 2025”
                    value = datetime.strptime(value, "%b %d, %Y")
                stocks[key].append(value)

        # Pick whichever header exists: “Date” or old “TIME”
        date_col = next(h for h in headers if h.lower() in ("time", "date"))

        # Build DataFrame and set the date index
        return pd.DataFrame(stocks, columns=headers).set_index(date_col)


    def daterange(self, start: date, end: date) -> list:
        period = end - start
        number_of_months = period.days // 30
        current_date = datetime(start.year, start.month, 1)
        dates = [current_date]

        for month in range(number_of_months):
            prev_date = dates[-1]
            dates.append(prev_date + relativedelta(months=1))

        dates = dates if len(dates) else [start]
        return dates

    # def preprocess(self, data: list) -> pd.DataFrame:
    #     # concatenate each frame to a single dataframe
    #     data = pd.concat(data)
    #     # sort the data by date
    #     data = data.sort_index()
    #     # change indexes from all uppercase to title
    #     data = data.rename(columns=str.title)
    #     # change index label Title to Date
    #     data.index.name = "Date"
    #     # remove non-numeric characters from volume column 
    #     data.Volume = data.Volume.str.replace(",", "")
    #     # coerce each column type to float
    #     for column in data.columns:
    #         data[column] = data[column].str.replace(",", "").astype(np.float64)
    #     return data

    def preprocess(self, data: list) -> pd.DataFrame:
        # 1) Concatenate month-by-month slices
        data = pd.concat(data)

        # 2) Sort by date index
        data = data.sort_index()

        # 3) Normalize column names (title-case) and rename index
        data = data.rename(columns=str.title)
        data.index.name = "Date"

        # 4) Clean and cast each column
        for col in data.columns:
            # strip commas everywhere
            series = data[col].str.replace(",", "")
            if col == "Change (%)":
                # remove percent sign before casting
                series = series.str.replace("%", "")
            data[col] = series.astype(np.float64)

        return data


data_reader = DataReader()

if __name__ == "__main__":
    data = data_reader.stocks(["SILK", "PACE"], date(2021, 1, 7), date.today())
    print(data)
