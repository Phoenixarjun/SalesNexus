from pathlib import Path
from typing import Dict
import pandas as pd


class DataProcessor:
    """Perform merging, cleaning, and exporting of Store Sales Time Series data."""

    def __init__(self, data_dir: Path, data_files: Dict[str, str]) -> None:
        self.data_dir = data_dir
        self.data_files = data_files
        self.data = {}

    def load(self) -> "DataProcessor":
        """Load all files and standardize date columns."""
        self.data = {
            name: pd.read_csv(self.data_dir / path) for name, path in self.data_files.items()
        }
        # ✅ Ensure 'date' columns are ALWAYS datetime
        for key in ["train", "test", "oil", "holidays_events", "transactions"]:
            if key in self.data and "date" in self.data[key].columns:
                self.data[key]["date"] = pd.to_datetime(self.data[key]["date"])
        return self

    def interpolate_oil(self) -> "DataProcessor":
        """Interpolate missing values in the oil data."""
        self.data["oil"].set_index("date", inplace=True)
        self.data["oil"]["dcoilwtico"] = self.data["oil"]["dcoilwtico"].interpolate(method="linear")
        self.data["oil"].reset_index(inplace=True)
        return self

    def merge_train_test(self) -> "DataProcessor":
        """Merge train/test with stores and transactions."""
        self.data["train_merged"] = (
            self.data["train"]
            .merge(self.data["stores"], on="store_nbr", how="left")
            .merge(self.data["transactions"], on=["store_nbr", "date"], how="left")
        )
        self.data["test_merged"] = (
            self.data["test"]
            .merge(self.data["stores"], on="store_nbr", how="left")
            .merge(self.data["transactions"], on=["store_nbr", "date"], how="left")
        )
        return self

    def merge_holidays_and_oil(self) -> "DataProcessor":
        """Merge holidays and oil data for final train/test."""
        holidays_oil_merged = self.data["oil"].merge(self.data["holidays_events"], on="date", how="left")

        self.data["train_final"] = self.data["train_merged"].merge(holidays_oil_merged, on="date", how="left")
        self.data["test_final"] = self.data["test_merged"].merge(holidays_oil_merged, on="date", how="left")

        # Final interpolate + forward fill
        for df_name in ["train_final", "test_final"]:
            self.data[df_name]["dcoilwtico"] = (
                self.data[df_name]["dcoilwtico"].interpolate(method="linear").ffill()
            )
        return self

    def drop_irrelevant_columns(self) -> "DataProcessor":
        """Drop low-value and sparse columns, remove duplicates."""
        drop_cols = ["description", "locale_name", "locale", "transferred"]
        for df_name in ["train_final", "test_final"]:
            self.data[df_name].drop(columns=drop_cols, errors="ignore", inplace=True)
            self.data[df_name].drop_duplicates(inplace=True)
        return self

    def save(self, train_file: Path, test_file: Path) -> "DataProcessor":
        """Save final merged train and test files."""
        train_file.parent.mkdir(parents=True, exist_ok=True) 
        self.data["train_final"].to_csv(train_file, index=False)
        self.data["test_final"].to_csv(test_file, index=False)

        print(f"✅ Final train saved to: {train_file}")
        print(f"✅ Final test saved to: {test_file}")

        return self
