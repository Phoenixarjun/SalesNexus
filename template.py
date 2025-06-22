import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "SalesNexus"

list_of_files = [

    f"ml_service/__init__.py",
    f"ml_service/components/__init__.py",
    f"ml_service/components/data_loader.py",
    f"ml_service/components/feature_engineering.py",
    f"ml_service/components/model_training.py",
    f"ml_service/config/__init__.py",
    f"ml_service/config/configuration.py",
    f"ml_service/constants/__init__.py",
    f"ml_service/constants/application.py",
    f"ml_service/entity/__init__.py",
    f"ml_service/entity/artifacts_entity.py",
    f"ml_service/entity/config_entity.py",
    f"ml_service/exception/__init__.py",
    f"ml_service/logger/__init__.py",
    f"ml_service/pipeline/__init__.py",
    f"ml_service/pipeline/training_pipeline.py",
    f"ml_service/utils/__init__.py",
    f"ml_service/utils/main_utils.py",

    "data/.gitkeep",
    "research/trials.ipynb",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "app.py",
    "Dockerfile",
    ".env"
]

if __name__ == '__main__':
    for filepath in list_of_files:
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)

        if filedir:
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Created directory: {filedir}")

        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, "w") as f:
                pass
            logging.info(f"Created empty file: {filepath}")

        else:
            logging.info(f"{filename} already exists.")
