import pandas as pd
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def extract_cities(filepath):
    logging.info(f"Reading cities from {filepath}...")
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Loaded {len(df)} cities")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        raise

def extract_weather(cities_df):
    logging.info("Fetching weather data from Open-Meteo API...")
    weather_records = []

    for _, row in cities_df.iterrows():
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": row["lat"],
                "longitude": row["lon"],
                "current_weather": True,
                "hourly": "relative_humidity_2m,precipitation_probability"
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data["current_weather"]
            weather_records.append({
                "city": row["city"],
                "country": row["country"],
                "lat": row["lat"],
                "lon": row["lon"],
                "temperature_c": current["temperature"],
                "windspeed_kmh": current["windspeed"],
                "weather_code": current["weathercode"],
                "is_day": bool(current["is_day"])
            })
            logging.info(f"Fetched weather for {row['city']}")

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch weather for {row['city']}: {e}")
            continue

    logging.info(f"Successfully fetched weather for {len(weather_records)} cities")
    return pd.DataFrame(weather_records)

