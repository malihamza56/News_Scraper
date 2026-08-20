"""
Cleaner Module: Clean and normalize extracted news data.
"""

from datetime import datetime

from src.config.logger import logger


class Cleaner:

    def __init__(self, news_data):

        self.news_data = news_data

        if not news_data:
            raise ValueError(
                "News data not received"
            )

    def clean_data(self):

        cleaned_data = []

        try:

            logger.info(
                "Cleaning extracted news data..."
            )

            seen_urls = set()

            for article in self.news_data:

                # ------------------------------------------------
                # BASIC FIELDS
                # ------------------------------------------------

                title = (
                    article.get("title")
                    or "Unknown Title"
                ).strip()

                author = (
                    article.get("author")
                    or "Unknown Author"
                ).strip()

                description = (
                    article.get("description")
                    or "No Description Available"
                ).strip()

                url = (
                    article.get("url")
                    or ""
                ).strip()

                published_at = (
                    article.get("publishedAt")
                    or ""
                ).strip()

                # ------------------------------------------------
                # DUPLICATE CHECK
                # ------------------------------------------------

                if url:

                    if url in seen_urls:

                        logger.info(
                            f"Duplicate article skipped | {url}"
                        )

                        continue

                    seen_urls.add(url)

                # ------------------------------------------------
                # DATE CLEANING
                # ------------------------------------------------

                published_date = self.clean_date(
                    published_at
                )

                # ------------------------------------------------
                # STORE CLEAN ARTICLE
                # ------------------------------------------------

                cleaned_data.append(
                    {
                        "title": title,
                        "author": author,
                        "description": description,
                        "url": url,
                        "publishedAt": published_date,
                    }
                )

            logger.info(
                f"News cleaning completed | "
                f"{len(cleaned_data)} unique articles"
            )

            return cleaned_data

        except Exception as e:

            logger.error(
                f"Failed to clean news data | {e}"
            )

            raise

    # ============================================================
    # DATE CLEANER
    # ============================================================

    @staticmethod
    def clean_date(date_value):

        if not date_value:
            return "Unknown Date"

        try:

            # News API usually returns ISO-8601
            dt = datetime.fromisoformat(
                date_value.replace(
                    "Z",
                    "+00:00"
                )
            )

            return dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        except (ValueError, TypeError):

            logger.warning(
                f"Unable to normalize date | {date_value}"
            )

            return date_value.strip()