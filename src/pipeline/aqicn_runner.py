from __future__ import annotations

import logging

from src.data_loader.aqi_api_client import AQIAPIClient
from src.pipeline.collector import collect_records
from src.storage.sqlite_storage import SQLiteStorage
from src.visualization.plots import PlotService


logger = logging.getLogger(__name__)


def run_aqicn_pipeline(
    api_token: str,
    db_path,
    plots_dir,
    cities: list[str],
) -> None:
    """
    Bonus pipeline:
    Fetch -> Store in SQLite -> Plot latest per city
    """
    if not api_token:
        raise RuntimeError("AQICN_API_TOKEN is missing. AQICN mode requires a valid token in .env")

    client = AQIAPIClient(api_token=api_token)
    storage = SQLiteStorage(db_path)

    result = collect_records(client, cities)

    for e in result.errors:
        logger.warning("Collector error: %s", e)

    inserted = storage.insert_many(result.records)
    logger.info("Inserted %d rows into SQLite: %s", inserted, db_path)

    latest = storage.fetch_latest_per_city()
    plotter = PlotService(plots_dir)
    out = plotter.plot_latest_aqi_bar(latest, filename="latest_aqi.png")
    logger.info("Saved plot: %s", out)
