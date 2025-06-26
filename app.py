from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

app = FastAPI()

# Paths
scaler_path = Path("./artifacts/features_dataTransformation/scaler.joblib")
model_path = Path("./artifacts/model/model.joblib")

# Load artifacts
try:
    scaler = joblib.load(scaler_path) if scaler_path.exists() else None
    model = joblib.load(model_path) if model_path.exists() else None
except Exception as e:
    print(f"Error loading artifacts: {e}")
    scaler = None
    model = None

class PredictionInput(BaseModel):
    date: str
    family: str
    state: str
    city: str
    type_x: str
    type_y: str = "Regular Day"  # Default value
    onpromotion: int
    dcoilwtico: float
    transactions: int
    store_nbr: int
    cluster: int

@app.post("/predict")
def predict(data: PredictionInput):
    if model is None or scaler is None:
        return {"error": "Model or Scaler not found. Please train first."}
    
    try:
        # Create DataFrame from input
        input_data = data.dict()
        df = pd.DataFrame([input_data])
        
        # Date features (matches your FeatureEngineering class)
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["day_of_week"] = df["date"].dt.dayofweek
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
        df["day_of_year"] = df["date"].dt.dayofyear
        df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
        df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
        
        # Cyclical features (matches your encode_cyclical method)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
        df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        
        # Add lag features (empty since we don't have history for single prediction)
        for lag in [7, 14, 30, 60]:
            df[f"sales_lag_{lag}"] = 0  # Initialize with 0 for single prediction
        
        # Add rolling features (empty since we don't have history)
        for window in [7, 30, 60]:
            df[f"sales_roll_mean_{window}"] = 0
            df[f"sales_roll_std_{window}"] = 0
        
        # Add expanding features (empty since we don't have history)
        df["sales_expanding_mean"] = 0
        df["sales_expanding_max"] = 0
        df["sales_expanding_min"] = 0
        
        # Add interaction features (matches your add_interactions method)
        df["onpromotion_trend"] = df["onpromotion"] * df["day_of_year"]
        df["month_sales_interaction"] = 0  # Can't calculate without sales
        
        # One-Hot Encoding (matches your encode_and_scale method)
        cat_columns = ["family", "state", "city", "type_x", "type_y"]
        df = pd.get_dummies(df, columns=cat_columns, drop_first=True, dtype=int)
        
        # Get expected columns from model (convert to string to be safe)
        expected_columns = [str(col) for col in model.feature_names_in_]
        
        # Add missing columns with 0 values
        for col in expected_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Ensure correct column order and only keep expected columns
        df = df[expected_columns]
        
        # Scale features (matches your scale_columns criteria)
        scale_columns = [
            col for col in df.columns 
            if any(x in col for x in [
                "sales_lag_", "sales_roll", "sales_expanding",
                "onpromotion_trend", "month_sales_interaction",
                "dcoilwtico", "transactions"
            ])
        ]
        if scale_columns:
            df[scale_columns] = scaler.transform(df[scale_columns])
        
        # Predict
        prediction = model.predict(df)
        return {"predicted_sales": float(prediction[0])}
        
    except Exception as e:
        return {"error": f"Error during prediction: {str(e)}"}

@app.get("/")
def read_root():
    return {"message": "Store Sales Prediction API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)