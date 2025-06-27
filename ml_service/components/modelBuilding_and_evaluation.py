import os
from pathlib import Path
import pandas as pd
import numpy as np
import mlflow
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error
from urllib.parse import urlparse
from xgboost import XGBRegressor
from ml_service.utils.main_utils import save_json
from ml_service.constants import PARAMS_FILE_PATH


class ModelBuildingAndEvaluation:
    """Train, Evaluate Model and Track Results with MLflow."""
    def __init__(self, config):
        self.config = config
        self.model = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

    def load_data(self):
        """Load, sample, and split data into train/val sets."""
        train_df = pd.read_csv(self.config.input_train_file)
        test_df = pd.read_csv(self.config.input_test_file)

        # Ensure 'date' is datetime
        train_df["date"] = pd.to_datetime(train_df["date"])
        # train_df = train_df.sample(n=50000, random_state=42).reset_index(drop=True)

        # Split into training and validation
        train_split = train_df[train_df["date"].dt.year <= 2016].reset_index(drop=True)
        val_split = train_df[train_df["date"].dt.year == 2017].reset_index(drop=True)

        self.X_train = train_split.drop(columns=["sales", "date"])
        self.y_train = train_split["sales"]

        self.X_test = val_split.drop(columns=["sales", "date"])
        self.y_test = val_split["sales"]

    def train_model(self):
        """Train XGBoost Model based on config parameters."""
        self.model = XGBRegressor(
            random_state=self.config.all_params["RANDOM_STATE"],
            n_estimators=self.config.all_params["N_ESTIMATORS"],
            learning_rate=self.config.all_params["LEARNING_RATE"],
            max_depth=self.config.all_params["MAX_DEPTH"],
            subsample=self.config.all_params["SUBSAMPLE"],
            colsample_bytree=self.config.all_params["COLSAMPLE_BY_TREE"],
            objective=self.config.all_params["OBJECTIVE"]
        )
        self.model.fit(self.X_train, self.y_train)

        # Save trained model
        os.makedirs(Path(self.config.path_of_model).parent, exist_ok=True)
        joblib.dump(self.model, self.config.path_of_model)

    def evaluate(self) -> dict:
        """Evaluate Model and Save Metrics."""
        y_pred = self.model.predict(self.X_test)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        mae = mean_absolute_error(self.y_test, y_pred)
        rmsle = np.sqrt(np.mean(np.square(np.log1p(np.maximum(y_pred, 0)) - np.log1p(self.y_test))))

        metrics = {"rmse": rmse, "mae": mae, "rmsle": rmsle}
        save_json(self.config.metrics_file, metrics)

        return metrics

    def log_into_mlflow(self, metrics: dict):
        """Log Model Parameters and Metrics into MLflow."""
        mlflow.set_tracking_uri(self.config.mlflow_uri)
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme
        model_params = {
            "MODEL_TYPE": self.config.all_params["MODEL_TYPE"],
            "RANDOM_STATE": self.config.all_params["RANDOM_STATE"],
            "N_ESTIMATORS": self.config.all_params["N_ESTIMATORS"],
            "LEARNING_RATE": self.config.all_params["LEARNING_RATE"],
            "MAX_DEPTH": self.config.all_params["MAX_DEPTH"],
            "SUBSAMPLE": self.config.all_params["SUBSAMPLE"],
            "COLSAMPLE_BY_TREE": self.config.all_params["COLSAMPLE_BY_TREE"],
            "REG_ALPHA": self.config.all_params["REG_ALPHA"],
            "REG_LAMBDA": self.config.all_params["REG_LAMBDA"],
            "GAMMA": self.config.all_params["GAMMA"],
            "OBJECTIVE": self.config.all_params["OBJECTIVE"]
        }

        with mlflow.start_run():
            mlflow.log_params(model_params)
            mlflow.log_metrics(metrics)

            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(self.model, "model",
                                          registered_model_name="SalesNexus_XGBoost_Model")
            else:
                mlflow.sklearn.log_model(self.model, "model")

    def create_submission(self, test_file, submission_file):
        """Create Submission File for Kaggle-style prediction."""
        test_df = pd.read_csv(test_file)

        # Ensure columns match training
        missing_cols = set(self.X_train.columns) - set(test_df.columns)
        for col in missing_cols:
            test_df[col] = 0
        test_features = test_df[self.X_train.columns]

        sales_predictions = self.model.predict(test_features)
        sales_predictions = np.where(sales_predictions < 0, 0, sales_predictions)

        submission = test_df[["id"]].copy()
        submission["sales"] = sales_predictions
        submission.to_csv(submission_file, index=False)

        print(f"✅ Submission saved! Shape: {submission.shape}")

    def run_pipeline(self):
        """Complete End-to-End Model Training, Evaluation, and Logging."""
        self.load_data()
        self.train_model()
        metrics = self.evaluate()
        self.log_into_mlflow(metrics)
        return metrics
