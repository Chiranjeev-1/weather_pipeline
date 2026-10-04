import logging
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load(df):
    logging.info("Starting load to PostgreSQL...")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in environment variables")

    engine = create_engine(database_url)
    df["wind_category"] = df["wind_category"].astype(str)
    df.to_sql("weather_data", engine, if_exists="replace", index=False)

    logging.info(f"Loaded {len(df)} records into weather_data table")