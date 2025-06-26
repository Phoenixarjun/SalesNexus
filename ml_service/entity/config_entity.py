from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class DataAcquisitionConfig:
    """Config for downloading and accessing raw data files."""
    root_dir: Path
    source: str          
    dataset_name: str    
    local_dir: Path       
    data_files: Dict[str, str]  



@dataclass(frozen=True)
class DataPreprocessingConfig:
    """Config for preprocessing data."""
    root_dir: Path
    train_file: Path
    test_file: Path

@dataclass(frozen=True)
class FeatureEngineeringAndDataTransformationConfig:
    root_dir: Path
    input_train_file: str
    input_test_file: str
    train_file: str
    test_file: str
    scaler_file: str

@dataclass(frozen=True)
class ModelTrainingConfig:
    """Config for model training and saving the final artifact."""
    root_dir: Path
    model_file: Path


@dataclass(frozen=True)
class ModelBuildingAndEvaluationConfig:
    path_of_model: Path
    input_train_file: Path
    input_test_file: Path
    metrics_file: Path
    all_params: dict
    mlflow_uri: str