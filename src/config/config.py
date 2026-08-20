"""
Config Module: Control the configurations of All the Scraper
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
#!================================================
#!           BASE DIRECTORY
#!================================================

BASE_DIR = Path(__file__).resolve().parents[2]



#!================================================
#!           ENVIRONMENT VARIABLES
#!================================================

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

#!================================================
#!           NEWS API
#!================================================

NEWS_API_BASE_URL = "https://newsapi.org/v2"


API_KEY = st.secrets.get("API_KEY") or os.getenv("API_KEY")

#!================================================
#!           API ENDPOINTS
#!================================================

EVERYTHING_ENDPOINT =  (f"{NEWS_API_BASE_URL}/everything")

TOP_HEADLINES_ENDPOINT = (f"{NEWS_API_BASE_URL}/top-headlines")

SOURCES_ENDPOINT = (f"{NEWS_API_BASE_URL}/sources")


#!================================================
#!           REQUEST CONFIGS
#!================================================

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_PAGE = 1

#!================================================
#!           NEWS CATEGORIES
#!================================================

NEWS_CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology",
]


#!================================================
#!            NEWS LANGUAGES
#!================================================

NEWS_LANGUAGES = {
    "English": "en",
    "Urdu": "ud",
    "Arabic": "ar",
    "German": "de",
    "Spanish": "es",
    "French": "fr",
    "Hebrew": "he",
    "Italian": "it",
    "Dutch": "nl",
    "Norwegian": "no",
    "Portuguese": "pt",
    "Russian": "ru",
    "Swedish": "sv",
    "Chinese": "zh",
}


#!================================================
#!            SORTING OPTIONS
#!================================================

SORT_OPTIONS = {
    "Newest": "publishedAt",
    "Relevance": "relevancy",
    "Popularity": "popularity",
}

#!================================================
#!            DATA DIRECTORIES
#!================================================

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

#!================================================
#!            OUTPUT FILES
#!================================================

RAW_JSON = RAW_DATA_DIR / "raw_news_data.json"
EXCEL_PATH = PROCESSED_DATA_DIR / "news.xlsx" 
CSV_PATH = PROCESSED_DATA_DIR / "news.csv"
CLEAN_JSON_PATH = PROCESSED_DATA_DIR / "news.json"

#!================================================
#!            LOGGING DIRECTORY
#!================================================

LOGGING_DIR = BASE_DIR /"logs"

LOGGING_FILE_PATH = LOGGING_DIR / "scraper.logs"