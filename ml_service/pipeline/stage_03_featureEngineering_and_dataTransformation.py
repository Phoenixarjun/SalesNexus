from ml_service.config.configuration import ConfigurationManager
from ml_service.logging import logger
from ml_service.constants import *
from ml_service.components.feature_engineering import FeatureEngineeringAndDataTransformation
from pathlib import Path

class FeatureEngineeringTrainingPipeline:
    """Pipeline for feature engineering and data transformation."""
    def __init__(self):
        pass

    def main(self):
        config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
        feature_config = config_manager.get_feature_engineering_and_data_transformation_config()

        fe = FeatureEngineeringAndDataTransformation(
            train_file=Path(feature_config.input_train_file),
            test_file=Path(feature_config.input_test_file),
            output_dir=feature_config.root_dir,
            scale_file=Path(feature_config.scaler_file),
        )
        fe.run()

if __name__ == "__main__":
    STAGE_NAME = "Feature Engineering & Data Transformation"
    try:
        logger.info("*******************************")
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = FeatureEngineeringTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
