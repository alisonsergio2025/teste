
import pandas as pd
import xgboost as xgb
import yfinance as yf
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
)
import datetime
from datetime import datetime, timedelta

class Forecast():
    def __init__(self, ticker):
        data = yf.Ticker("BZ=F")
        df = pd.DataFrame(data.history(period="max"))
        
        df['Date'] = pd.to_datetime(df.index, format='%Y-%m-%d').date
        df.index = df['Date']

        df = self.create_features(df)

        self.df = df

    def create_features(self, df):
        df["Date"] = pd.to_datetime(df["Date"])
        df["year"] = df["Date"].dt.year
        df["month"] = df["Date"].dt.month
        df["day"] = df["Date"].dt.day
        df["dayofweek"] = df["Date"].dt.dayofweek
        return df

    def split_train_test(self):
        train_size = self.df.shape[0] - 7
        train, test = self.df[:train_size], self.df[train_size:]
        
        self.train = self.create_features(train)
        self.test = self.create_features(test)
        
        self.FEATURES = ["year", "month", "day", "dayofweek"]
        self.TARGET = "Close"

    def calculate_metrics(self, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        return mae, mse, mape

    def train_xgb(self):
        X_train, y_train = self.train[self.FEATURES], self.train[self.TARGET]
        X_test, y_test = self.test[self.FEATURES], self.test[self.TARGET]
        
        reg = xgb.XGBRegressor(objective="reg:squarederror")
        reg.fit(X_train, y_train)
        
        preds = reg.predict(X_test)
        metrics = self.calculate_metrics(y_test, preds)
        self.metrics_xgb = pd.DataFrame([metrics], columns=["MAE", "MSE", "MAPE"])
        self.xgb_model = reg
        self.xbg_train_df = self.train
        self.xgb_test_df = self.test.copy()
        self.xgb_test_df['Predictions'] = reg.predict(X_test)

    def predict_future_days(self):
        days = []
        for i in range(6):
            day = (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')
        
            days.append(day)
        df = pd.DataFrame(days, columns=['Date'])
        
        X_pred = self.create_features(df)
        X_pred = X_pred.set_index('Date')
        preds = reg.predict(X_pred)

        self.df_real = pd.concat([self.xbg_train_df, self.xgb_test_df])
        X_pred['Close'] = preds
        self.seven_days_pred = X_pred
        