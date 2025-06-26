from ml_service.constants import *
from ml_service.utils.main_utils import read_yaml, create_directories
from ml_service.entity.config_entity import (DataAcquisitionConfig, DataPreprocessingConfig, FeatureEngineeringAndDataTransformationConfig, ModelBuildingAndEvaluationConfig)


class ConfigurationManager:
    def __init__(self, 
                 config_filepath: str = CONFIG_FILE_PATH,
                 params_filepath: str = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        root_dir = Path(self.config.modelBuildingAndEvaluation.root_dir)
        create_directories([root_dir])

    def get_data_acquisition_config(self) -> DataAcquisitionConfig:
        """Get the configuration for data acquisition.

        Returns:
            DataAcquisitionConfig: Paths and source details for data acquisition.
        """
        config = self.config.data_acquisition
        create_directories([config.root_dir])

        return DataAcquisitionConfig(
            root_dir=Path(config.root_dir),
            source=config.source,
            dataset_name=config.dataset_name,
            local_dir=Path(config.local_dir),
            data_files=dict(config.data_files)  
        )


    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        """Get the configuration for data preprocessing.

        Returns:
            DataPreprocessingConfig: Paths for train and test preprocessed files.
        """
        config = self.config.data_preprocessing
        create_directories([config.root_dir])

        return DataPreprocessingConfig(
            root_dir=Path(config.root_dir),
            train_file=Path(config.root_dir) / config.train_file,
            test_file=Path(config.root_dir) / config.test_file
        )
    

    def get_feature_engineering_and_data_transformation_config(self) -> FeatureEngineeringAndDataTransformationConfig:
        """Get the configuration for feature engineering and data transformation."""
        config = self.config.features_dataTransformation
        feature_config = FeatureEngineeringAndDataTransformationConfig(
            root_dir=Path(config.root_dir),
            input_train_file=config.input_train_file,
            input_test_file=config.input_test_file,
            train_file=config.train_final,
            test_file=config.test_final,
            scaler_file=config.scaler_file
        )
        create_directories([feature_config.root_dir])
        return feature_config
    

    def get_modelBuilding_and_evaluation_config(self) -> ModelBuildingAndEvaluationConfig:
        """Construct the EvaluationConfig object based on modelBuildingAndEvaluation settings."""
        model_cfg = self.config.modelBuildingAndEvaluation

        return ModelBuildingAndEvaluationConfig(
            path_of_model=Path(model_cfg.model_file),
            input_train_file=Path(model_cfg.input_train_file),
            input_test_file=Path(model_cfg.input_test_file),
            metrics_file=Path(model_cfg.evaluation_metrics),
            all_params=self.params,
            mlflow_uri=self.params.get("TRACKING_SERVER", "")
        )