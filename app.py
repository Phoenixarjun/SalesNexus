from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = Path("./artifacts/model")
FEATURES_DIR = Path("./artifacts/features_dataTransformation")

try:
    scaler = joblib.load(FEATURES_DIR / "scaler.joblib")
    model = joblib.load(MODEL_DIR / "model.joblib")
    print("✅ Model and scaler loaded successfully")
except Exception as e:
    print(f"❌ Error loading artifacts: {e}")
    scaler = None
    model = None

class PredictionInput(BaseModel):
    date: str
    family: str
    state: str
    city: str
    type_x: str
    type_y: str = "Regular Day"
    onpromotion: int = 0
    dcoilwtico: float = 50.0
    transactions: int = 1000
    store_nbr: int
    cluster: int = 1

@app.get("/")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict(data: PredictionInput):
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Service Unavailable: Model not loaded"
        )
    
    try:
        input_dict = data.dict()
        df = pd.DataFrame([input_dict])
        
        df = process_features(df)
        
        df = align_features(df)
        
        prediction = model.predict(df)
        
        return {
            "status": "success",
            "predicted_sales": float(prediction[0]),
            "message": "Prediction successful"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {str(e)}"
        )

def process_features(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all feature engineering steps"""
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["day_of_year"] = df["date"].dt.dayofyear
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)
    
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["day_of_week_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
    df["day_of_week_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
    
    
    df["onpromotion_trend"] = df["onpromotion"] * df["day_of_year"]
    df["month_sales_interaction"] = 0
    
    return df

def align_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure the DataFrame has all expected columns"""
    cat_columns = ["family", "state", "city", "type_x", "type_y"]
    df = pd.get_dummies(df, columns=cat_columns, drop_first=True, dtype=int)
    
    expected_columns = model.feature_names_in_
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
    
    df = df[expected_columns]
    
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
    
    return df

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)