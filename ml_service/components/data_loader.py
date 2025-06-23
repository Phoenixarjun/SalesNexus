from pathlib import Path
from typing import Dict
import pandas as pd
import opendatasets as od
import shutil

class DataLoader:
    """
    Handles downloading, flattening, and loading raw data files from Kaggle.
    """
    def __init__(self, data_dir: Path, source: str, data_files: Dict[str, str], dataset_name: str) -> None:
        """
        Args:
            data_dir (Path): Directory where raw files reside.
            source (str): Kaggle dataset URL.
            data_files (dict): Mapping of dataset names to filenames.
            dataset_name (str): Name of the Kaggle dataset (folder name after download).
        """
        self.data_dir = data_dir
        self.source = source
        self.data_files = data_files
        self.dataset_name = dataset_name

    def download(self) -> None:
        """Check if files already exist. If not, download and flatten."""
        if self._all_files_exist():
            print(f"✅ All files already present in: {self.data_dir}. Skipping download.")
            return

        # Otherwise, proceed with downloading
        self.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"🚀 Downloading dataset from Kaggle...")
        od.download(self.source, str(self.data_dir))
        print(f"✅ Download complete.")

        self._flatten_download()

    def _all_files_exist(self) -> bool:
        """Check if all required files already exist in the data_dir."""
        return all((self.data_dir / filename).exists() for filename in self.data_files.values())

    def _flatten_download(self) -> None:
        """Move files from Kaggle's subfolder into data_dir root."""
        kaggle_subdir = self.data_dir / self.dataset_name
        if kaggle_subdir.exists():
            for file in kaggle_subdir.iterdir():
                shutil.move(str(file), str(self.data_dir))
            kaggle_subdir.rmdir()
            print(f"📂 Flattened downloaded files into: {self.data_dir}")

    def load(self, name: str) -> pd.DataFrame:
        """Load a dataset by its configured name."""
        if name not in self.data_files:
            raise ValueError(f"Dataset '{name}' not found in configuration.")
        path = self.data_dir / self.data_files[name]
        if not path.exists():
            raise FileNotFoundError(f"File not found at {path}")
        print(f"📥 Loading: {path}")
        return pd.read_csv(path)

    def load_all(self) -> Dict[str, pd.DataFrame]:
        """Load all configured datasets as a dict of DataFrames."""
        return {name: self.load(name) for name in self.data_files.keys()}
