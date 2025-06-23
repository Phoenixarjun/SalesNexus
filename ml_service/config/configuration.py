from ml_service.constants import *
from ml_service.utils.main_utils import read_yaml, create_directories
from ml_service.entity.config_entity import DataAcquisitionConfig


class ConfigurationManager:
    def __init__(self, config_filepath: str):
        """Initialize the configuration manager.

        Args:
            config_filepath (str): Path to the main configuration file (YAML).
        """
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

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
