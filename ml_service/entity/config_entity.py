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
class FeatureEngineeringConfig:
    """Config for extracting and storing features."""
    root_dir: Path
    feature_file: Path

@dataclass(frozen=True)
class ModelTrainingConfig:
    """Config for model training and saving the final artifact."""
    root_dir: Path
    model_file: Path
