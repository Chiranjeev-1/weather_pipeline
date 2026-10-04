import pandas as pd
import logging

def transform(df):
    logging.info("Starting transformation...")
    logging.info(f"Raw records: {len(df)}")

    # Drop any rows where city or temperature is missing
    df.dropna(subset=["city", "temperature_c"], inplace=True)

    # Strip whitespace
    df["city"] = df["city"].str.strip().str.title()
    df["country"] = df["country"].str.strip().str.upper()

    # Map weather codes to human readable conditions
    weather_map = {
        0: "Clear Sky",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Icy Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Slight Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        80: "Slight Showers",
        81: "Moderate Showers",
        82: "Heavy Showers",
        95: "Thunderstorm",
        99: "Thunderstorm with Hail"
    }
    df["weather_condition"] = df["weather_code"].map(weather_map).fillna("Unknown")

    # Add temperature in Fahrenheit
    df["temperature_f"] = (df["temperature_c"] * 9/5) + 32

    # Categorize wind speed
    df["wind_category"] = pd.cut(
        df["windspeed_kmh"],
        bins=[0, 20, 40, 60, 1000],
        labels=["Calm", "Moderate", "Strong", "Storm"]
    )

    # Add timestamp
    df["extracted_at"] = pd.Timestamp.now()

    logging.info(f"Transformed {len(df)} records")
    return df