import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path


class FeatureEngineeringAndDataTransformation:
    def __init__(self, train_file, test_file, output_dir, scale_file, dtype_spec=None):
        self.train_file = train_file
        self.test_file = test_file
        self.output_dir = output_dir
        self.scale_file = scale_file
        self.dtype_spec = dtype_spec or {"some_column_name": str}

    def load_data(self):
        train_df = pd.read_csv(self.train_file, low_memory=False, dtype=self.dtype_spec)
        test_df = pd.read_csv(self.test_file, low_memory=False, dtype=self.dtype_spec)
        return train_df, test_df

    def fill_na(self, df):
        df = df.copy()
        df["type_y"] = df.get("type_y", pd.Series("Regular Day", index=df.index)).fillna("Regular Day")
        df["transactions"] = df.get("transactions", pd.Series(0, index=df.index)).fillna(0)
        df["dcoilwtico"] = df["dcoilwtico"].bfill()
        return df

    def add_dates(self, df):
        df = df.copy()
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

    def add_interactions(self, df):
        df = df.copy()
        df["onpromotion_trend"] = df["onpromotion"] * df["day_of_year"]
        return df

    def encode_cyclical(self, df):
        df = df.copy()
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        df.drop(["month", "day_of_week"], axis=1, inplace=True)
        return df

    def encode_and_scale(self, train_df, test_df):
        cat_columns = ["family", "state", "city", "type_x", "type_y"]

        combined = pd.concat([train_df, test_df], keys=["train", "test"])
        combined = pd.get_dummies(combined, columns=cat_columns, drop_first=True, dtype=int)

        train_df = combined.xs("train").copy()
        test_df = combined.xs("test").copy()

        scale_columns = [
            col for col in train_df.columns
            if any(x in col for x in [
                "onpromotion_trend",
                "dcoilwtico", "transactions"
            ])
        ]
        scaler = MinMaxScaler()
        train_df[scale_columns] = scaler.fit_transform(train_df[scale_columns])
        test_df[scale_columns] = scaler.transform(test_df[scale_columns])

        os.makedirs(self.output_dir, exist_ok=True)
        joblib.dump(scaler, self.scale_file)

        return train_df, test_df

    def save(self, train_df, test_df):
        train_df.to_csv(Path(self.output_dir) / "train_final.csv", index=False)
        test_df.to_csv(Path(self.output_dir) / "test_final.csv", index=False)

    def run(self):
        train_df, test_df = self.load_data()
        train_df, test_df = self.fill_na(train_df), self.fill_na(test_df)

        train_df, test_df = self.add_dates(train_df), self.add_dates(test_df)

        train_df = self.add_interactions(train_df)
        test_df = self.add_interactions(test_df)

        train_df, test_df = self.encode_cyclical(train_df), self.encode_cyclical(test_df)

        train_df, test_df = self.encode_and_scale(train_df, test_df)

        self.save(train_df, test_df)

        print(f"Final shapes -> Train: {train_df.shape}, Test: {test_df.shape}")
        print("✅ Done: Final files saved!")
