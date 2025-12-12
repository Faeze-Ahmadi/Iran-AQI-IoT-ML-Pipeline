from src.data_loader.aqi_api_client import AQIAPIClient


def main() -> None:
    client = AQIAPIClient()

    cities = ["tehran", "isfahan", "mashhad", "ahvaz"]

    for city in cities:
        try:
            data = client.fetch_city_aqi(city)
            print(data)
        except RuntimeError as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
