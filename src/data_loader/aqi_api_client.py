import os
import requests
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

class AQIAPIClient:
    """
    Client for fetching real-time Air Quality Index (AQI) data
    from the AQICN (World Air Quality Index) API.
    """

    BASE_URL = "https://api.waqi.info/feed"

    def __init__(self, api_token: str = None) -> None:
        if api_token:
            self.api_token = api_token  # Use provided token
        else:
            load_dotenv()  # Load environment variables from .env if no token is provided
            self.api_token = os.getenv("AQICN_API_TOKEN")

        if not self.api_token:
            raise ValueError("API token not found. Please set AQICN_API_TOKEN in .env file.")

    def fetch_city_aqi(self, city: str) -> Dict[str, Any]:
        """
        Fetch real-time AQI data for a given city.

        Parameters
        ----------
        city : str
            City name (e.g., 'tehran', 'isfahan').

        Returns
        -------
        dict
            Parsed AQI data.
        """
        url = f"{self.BASE_URL}/{city}/?token={self.api_token}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # This will raise an error for bad responses (4xx/5xx)
        except requests.RequestException as e:
            raise RuntimeError(f"Network/API error for city '{city}'") from e

        data = response.json()

        if data.get("status") != "ok":
            raise RuntimeError(f"API returned error for city '{city}': {data}")

        return self._parse_response(city, data["data"])

    def _parse_response(self, city: str, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse raw API response into a clean dictionary.
        """
        iaqi = raw.get("iaqi", {})

        return {
            "city": city,
            "aqi": raw.get("aqi"),
            "pm25": iaqi.get("pm25", {}).get("v"),
            "pm10": iaqi.get("pm10", {}).get("v"),
            "co": iaqi.get("co", {}).get("v"),
            "no2": iaqi.get("no2", {}).get("v"),
            "so2": iaqi.get("so2", {}).get("v"),
            "o3": iaqi.get("o3", {}).get("v"),
            "timestamp": datetime.utcnow().isoformat(),
        }
