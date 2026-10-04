import logging
from extract import extract_cities, extract_weather
from transform import transform
from load import load

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    logging.info("Pipeline started...")
    try:
        cities_df = extract_cities("weather_pipeline\\cities.csv")
        weather_df = extract_weather(cities_df)
        clean_df = transform(weather_df)
        load(clean_df)
        logging.info("Pipeline completed successfully!")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()