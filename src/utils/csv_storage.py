from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


class CSVStorage:
    """
    Handles persistence of AQI data into CSV files.
    """

    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def append_records(
        self,
        filename: str,
        records: List[Dict[str, Any]]
    ) -> None:
        """
        Append records to a CSV file. Creates file if it does not exist.
        """
        file_path = self.data_dir / filename
        df = pd.DataFrame(records)

        if file_path.exists():
            df.to_csv(file_path, mode="a", header=False, index=False)
        else:
            df.to_csv(file_path, mode="w", header=True, index=False)
