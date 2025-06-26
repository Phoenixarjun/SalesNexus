from pathlib import Path
from ml_service.config.configuration import ConfigurationManager
from ml_service.constants import *
from ml_service.components.data_loader import DataLoader
from ml_service.components.data_processing import DataProcessor
from ml_service.logging import logger

class DataPreprocessingTrainingPipeline:
    """Pipeline for merging, cleaning, and saving preprocessed train/test files."""
    def __init__(self):
        pass

    def main(self):
        # Load configuration details
        config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
        data_acquisition_config = config_manager.get_data_acquisition_config()
        data_preprocessing_config = config_manager.get_data_preprocessing_config()

        data_dir = Path(data_acquisition_config.local_dir)
        files = data_acquisition_config.data_files

        DataProcessor(data_dir, files) \
            .load() \
            .interpolate_oil() \
            .merge_train_test() \
            .merge_holidays_and_oil() \
            .drop_irrelevant_columns() \
            .save(data_preprocessing_config.train_file, data_preprocessing_config.test_file)

if __name__ == "__main__":
    STAGE_NAME = "Data Preprocessing Stage"
    try:
        logger.info("*******************************")
        logger.info(f">>>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataPreprocessingTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>> stage {STAGE_NAME} completed <<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e
