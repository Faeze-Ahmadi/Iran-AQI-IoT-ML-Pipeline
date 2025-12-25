from src.data_loader.aqi_api_client import AQIAPIClient
from src.pipeline.collector import collect_records
from src.storage.sqlite_storage import SQLiteStorage
from src.visualization.plots import PlotService
import logging

logger = logging.getLogger(__name__)

def run_aqicn_pipeline(api_token: str, db_path: str, plots_dir: str, cities: list[str]) -> None:
    if not api_token:
        raise RuntimeError("AQICN_API_TOKEN is missing. AQICN mode requires a valid token in .env")

    client = AQIAPIClient(api_token=api_token)  # Initialize API client
    storage = SQLiteStorage(db_path)  # Initialize SQLite storage

    result = collect_records(client, cities)  # Collect AQI data

    for e in result.errors:
        logger.warning("Collector error: %s", e)

    inserted = storage.insert_many(result.records)
    logger.info("Inserted %d rows into SQLite: %s", inserted, db_path)

    latest = storage.fetch_latest_per_city()  # Fetch the latest data

    # Ensure that 'aqi' column is in the dataframe before plotting
    for record in latest:
        if 'aqi' not in record:
            logger.warning("AQI data is missing for city: %s", record.get("city"))
            continue  # Skip this record if AQI data is missing
        else:
            logger.info(f"AQI data for {record.get('city')}: {record.get('aqi')}")  # Log the AQI data

    result = collect_records(client, cities)

    for e in result.errors:
        logger.warning("Collector error: %s", e)

    if not result.records:
        logger.error("No AQICN data collected. Skipping plotting.")
        return

    plotter = PlotService(plots_dir)  # Initialize PlotService

    # Save the latest AQI bar plot
    out = plotter.plot_latest_aqi_bar(latest, filename="latest_aqi.png")
    logger.info("Saved plot: %s", out)

    # Save the error histogram (if needed for analysis)
    error_out = plotter.plot_error_histogram(latest, filename="aqi_error_hist.png")
    logger.info("Saved error histogram: %s", error_out)
