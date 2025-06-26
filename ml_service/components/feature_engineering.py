import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

class FeatureEngineeringAndDataTransformation:
    def __init__(self, train_file, test_file, output_dir, scale_file):
        self.train_file = train_file
        self.test_file = test_file
        self.output_dir = output_dir
        self.scale_file = scale_file

    def load_data(self):
        return pd.read_csv(self.train_file), pd.read_csv(self.test_file)

    def fill_na(self, df):
        df["type_y"] = df.get("type_y", pd.Series("Regular Day", index=df.index)).fillna("Regular Day")
        df["transactions"] = df.get("transactions", pd.Series(0, index=df.index)).fillna(0)
        df["dcoilwtico"] = df["dcoilwtico"].bfill()
        return df

    def create_dates(self, df):
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["day_of_week"] = df["date"].dt.dayofweek
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
        df["day_of_year"] = df["date"].dt.dayofyear
        df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
        df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
        return df

    def encode_and_scale(self, train_df, test_df):
        sales_values = train_df["sales"]

        cat_columns = ["family", "state", "city", "type_x", "type_y"]

        train_df = pd.get_dummies(train_df, columns=cat_columns, drop_first=True, dtype=int)
        test_df = pd.get_dummies(test_df, columns=cat_columns, drop_first=True, dtype=int)

        common_columns = set(train_df.columns).intersection(set(test_df.columns))
        train_df = train_df[list(common_columns) + ["sales"]] if "sales" in train_df.columns else train_df[list(common_columns)]
        test_df = test_df[list(common_columns)]

        if "sales" not in train_df.columns:
            train_df["sales"] = sales_values

        scale_columns = [
            col for col in train_df.columns
            if any(x in col for x in [
                "sales_lag_", "sales_roll", "sales_expanding",
                "onpromotion_trend", "month_sales_interaction",
                "dcoilwtico", "transactions"
            ])
        ]
        scaler = MinMaxScaler()
        train_df[scale_columns] = scaler.fit_transform(train_df[scale_columns])
        test_df[scale_columns] = scaler.transform(test_df[scale_columns])

        os.makedirs(self.output_dir, exist_ok=True)
        joblib.dump(scaler, self.scale_file)

        return train_df, test_df


    def add_lags(self, df):
        df = df.sort_values(["store_nbr", "family", "date"])
        for lag in [7, 14, 30, 60]:
            df[f"sales_lag_{lag}"] = df.groupby(["store_nbr", "family"])["sales"].shift(lag)
        return df

    def add_rolling(self, df):
        df = df.sort_values(["store_nbr", "family", "date"])
        for window in [7, 30, 60]:
            df[f"sales_roll_mean_{window}"] = df.groupby(["store_nbr", "family"])["sales"].shift(1).rolling(window).mean()
            df[f"sales_roll_std_{window}"] = df.groupby(["store_nbr", "family"])["sales"].shift(1).rolling(window).std()
        return df

    def add_expanding(self, df):
        df["sales_expanding_mean"] = df.groupby(["store_nbr", "family"])["sales"].expanding(min_periods=1).mean().reset_index(level=[0,1], drop=True)
        df["sales_expanding_max"] = df.groupby(["store_nbr", "family"])["sales"].expanding(min_periods=1).max().reset_index(level=[0,1], drop=True)
        df["sales_expanding_min"] = df.groupby(["store_nbr", "family"])["sales"].expanding(min_periods=1).min().reset_index(level=[0,1], drop=True)
        return df

    def add_interactions(self, df, is_train=False):
        df["onpromotion_trend"] = df["onpromotion"] * df["day_of_year"]
        if is_train:
            df["month_sales_interaction"] = df["month"] * df["sales"]
        return df

    def drop_na(self, df):
        sales_columns = [c for c in df.columns if any(x in c for x in ["sales_lag_", "sales_roll"])]
        df.dropna(subset=sales_columns, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def save(self, train_df, test_df):
        train_df.to_csv(self.output_dir / "train_final.csv", index=False)
        test_df.to_csv(self.output_dir / "test_final.csv", index=False)

    def run(self):
        train_df, test_df = self.load_data()
        train_df, test_df = self.fill_na(train_df), self.fill_na(test_df)
        train_df, test_df = self.create_dates(train_df), self.create_dates(test_df)

        train_df = self.add_lags(train_df)
        train_df = self.add_rolling(train_df)
        train_df = self.add_expanding(train_df)

        train_df = self.add_interactions(train_df, is_train=True)
        test_df = self.add_interactions(test_df, is_train=False)

        train_df, test_df = self.encode_cyclical(train_df), self.encode_cyclical(test_df)

        train_df = self.drop_na(train_df)

        train_df, test_df = self.encode_and_scale(train_df, test_df)

        self.save(train_df, test_df)

        print("✅ Done: Final files saved!")

