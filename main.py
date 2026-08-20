
"""
Main Module: Controls the complete news scraping workflow.
"""
import pandas as pd
from src.config.logger import logger
from src.api.news_api import NewsAPI
from src.extraction.news import Extractor
from src.services.cleaner import Cleaner
from src.serializer.serialization import Serialization
from src.exporter.exporter import Exporter


def scrape_news(
    keyword,
    language="en",
    sort_by="publishedAt",
):
    """
    Complete news scraping workflow.

    Flow:
        News API
        -> Extractor
        -> Cleaner
        -> Serializer
        -> Exporter

    Returns:
        Cleaned news data.
    """

    try:

        logger.info(
            "News scraping workflow started."
        )

        # ====================================================
        # 1. NEWS API
        # ====================================================

        api = NewsAPI()

        response = api.get_everything(
            keyword=keyword,
            language=language,
            sort_by=sort_by
        )

        logger.info(
            "Raw response received from News API."
        )

        # ====================================================
        # 2. EXTRACTOR
        # ====================================================

        extractor = Extractor(
            response=response
        )

        news_data = extractor.extract_fields()

        logger.info(
            f"Articles extracted | {len(news_data)}"
        )

        # ====================================================
        # 3. CLEANER
        # ====================================================

        cleaner = Cleaner(
            news_data=news_data
        )

        cleaned_data = cleaner.clean_data()

        logger.info(
            f"Articles cleaned | {len(cleaned_data)}"
        )
        
        # ====================================================
        #  DATAFRAME
        # ====================================================
        
        df = pd.DataFrame(data=cleaned_data)
        
        # ====================================================
        # 4. SERIALIZER
        # ====================================================

        serializer = Serialization(
            dataframe=df
        )

        serializer.save_json()

        logger.info(
            "News data serialized successfully."
        )

        # ====================================================
        # 5. EXPORTER
        # ====================================================

        exporter = Exporter(
            dataframe=df
        )

        exporter.export_csv()
        exporter.export_excel()

        logger.info(
            "CSV and Excel reports generated successfully."
        )

        # ====================================================
        # RETURN
        # ====================================================

        return {
            "status": "success",
            "total_results": response.get(
                "totalResults",
                0
            ),
            "articles": cleaned_data,
        }

    except Exception as e:

        logger.error(
            f"News scraping workflow failed | {e}"
        )

        raise


# ============================================================
# CLI TEST MODE
# ============================================================

def main():

    try:

        keyword = input(
            "Enter news keyword: "
        ).strip()

        if not keyword:

            raise ValueError(
                "Keyword is required."
            )

        language = input(
            "Enter language code "
            "(default: en): "
        ).strip()

        if not language:
            language = "en"

        sort_by = input(
            "Enter sort type "
            "(publishedAt / relevancy / popularity): "
        ).strip()

        if not sort_by:
            sort_by = "publishedAt"

        result = scrape_news(
            keyword=keyword,
            language=language,
            sort_by=sort_by,
        )

        print(
            f"\nTotal matching results: "
            f"{result['total_results']}"
        )

        print(
            f"Articles extracted: "
            f"{len(result['articles'])}"
        )

        print(
            "\nNews scraping completed successfully!"
        )

    except Exception as e:

        logger.error(
            f"Application failed | {e}"
        )

        print(
            f"❌ Error: {e}"
        )


if __name__ == "__main__":
    main()