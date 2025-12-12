from src.data_loader.aqi_api_client import AQIAPIClient
from src.utils.csv_storage import CSVStorage


def main() -> None:
    client = AQIAPIClient()
    storage = CSVStorage(data_dir="data")

    cities = ["tehran", "isfahan", "mashhad", "ahvaz"]
    records = []

    for city in cities:
        try:
            data = client.fetch_city_aqi(city)
            records.append(data)
            print(data)
        except RuntimeError as e:
            print(f"[ERROR] {e}")

    if records:
        storage.append_records(
            filename="aqi_history.csv",
            records=records
        )
        print("Data saved successfully.")


if __name__ == "__main__":
    main()
