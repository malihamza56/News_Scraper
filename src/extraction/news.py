"""
Extractor Module: Extract the required Fields from Articles
"""

from src.config.logger import logger


class Extractor:
    
    def __init__(self , response):
        self.response = response
        
        if not response:
            raise ValueError("Json Response not recieved")
        
        
    def extract_fields(
        self
    ):
        
        
        news_data = []
        
        try:
            
            
            logger.info("Extracting Fields from Response")
            
            articles = self.response.get("articles",[])
            
            for article in articles:
                
                title = article.get('title')
                author = article.get('author')
                description = article.get('description')
                url = article.get('url')
                published_date = article.get('publishedAt')
                
                
                news_data.append(
                    {
                        'title':title,
                        'author':author,
                        'description':description,
                        'url':url,
                        'publishedAt':published_date
                    }
                )
            logger.info(f"Data Fields extracted successfully")
            
            
            return news_data
        
        except Exception as e:
            logger.error(f"Failed to extract Data Fields | {e}")
            raise
        
