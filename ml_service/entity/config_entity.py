from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataAcquisitionConfig:
    """Config for downloading the raw data from Kaggle using opendatasets."""
    root_dir: Path
    source: str           
    dataset_name: str     
    local_dir: Path       

@dataclass(frozen=True)
class DataPreparationConfig:
    """Config for data cleaning and preparation."""
    root_dir: Path
    raw_dir: Path
    processed_dir: Path

@dataclass(frozen=True)
class FeatureEngineeringConfig:
    """Config for extracting and storing features."""
    root_dir: Path
    feature_file: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    """Config for model training and saving the final artifact."""
    root_dir: Path
    model_file: Path
