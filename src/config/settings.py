from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    # Paths
    project_root: Path
    data_dir: Path
    plots_dir: Path
    models_dir: Path

    # UCI (core dataset)
    uci_csv_path: Path

    # AQICN (bonus dataset)
    aqicn_api_token: str | None
    aqicn_db_path: Path
    cities: list[str]


def load_settings() -> Settings:
    """
    Load project settings.

    IMPORTANT:
    - AQICN_API_TOKEN is OPTIONAL
    - Only required when running in `aqicn` mode
    """
    load_dotenv()

    project_root = Path(".").resolve()
    data_dir = project_root / "data"
    plots_dir = data_dir / "plots"
    models_dir = data_dir / "models"
    uci_dir = data_dir / "uci"

    data_dir.mkdir(exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)
    uci_dir.mkdir(parents=True, exist_ok=True)

    uci_csv_path = uci_dir / "AirQualityUCI.csv"

    # AQICN token is OPTIONAL
    token = os.getenv("AQICN_API_TOKEN")
    if token:
        token = token.strip()

    aqicn_db_path = data_dir / "aqi_history.sqlite"

    cities = ["tehran", "isfahan", "mashhad", "ahvaz"]

    return Settings(
        project_root=project_root,
        data_dir=data_dir,
        plots_dir=plots_dir,
        models_dir=models_dir,
        uci_csv_path=uci_csv_path,
        aqicn_api_token=token,
        aqicn_db_path=aqicn_db_path,
        cities=cities,
    )
