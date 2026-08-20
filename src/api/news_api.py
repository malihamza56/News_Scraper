import requests
from src.config.config import (
    API_KEY,
    EVERYTHING_ENDPOINT,
    TOP_HEADLINES_ENDPOINT,
    SOURCES_ENDPOINT,
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE
)
from src.config.logger import logger

print(bool(API_KEY))
class NewsAPI:
    
    
    #^------------------------------
    #^       constructor
    #^------------------------------
    
    def __init__(self):
        self.apiKey = API_KEY
        
        if not self.apiKey:
            
            raise ValueError("API KEY MISSING | UNABLE TO LOAD FROM ENVIRONMENT")
        
        self.headers = {
            "X-Api-Key" : self.apiKey
        }
        
    
    #^------------------------------
    #^       RESPONSE FUNCTION
    #^------------------------------
    
        
    def get_response(
        self,
        encpoints,
        params
    ):
        
        
        try:
            
            
            logger.info(f"Sending Request to news api: {encpoints}")
            
            response = requests.get(
                url=encpoints,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            
            response.raise_for_status()
            
            logger.info(f"News Api Response | {response.status_code}")
            
            data = response.json()
            
            return data
        
        except requests.exceptions.HTTPError :
            logger.error(f"HTTP Error occured ")
            raise
        
        except requests.exceptions.Timeout :
            logger.error(f"Timeout Error Occured")
            raise
        
        except Exception as e:
            logger.error(f"An Error occured | {e}")
            raise
        
        
    
    #^--------------------------------------
    #^       EVERYTHING ENDPOINT FUNCTION
    #^--------------------------------------
    
        
    def get_everything(
        self,
        keyword,
        source = None,
        from_date = None,
        to_date = None,
        language = None,
        domain = None,
        sort_by = "publishedAt",
        page = DEFAULT_PAGE,
        max_page = MAX_PAGE_SIZE  
    ):
        
        #*QUERY PARAMS

        params = {
            'q' : keyword,
            'pageSize':max_page,
            'page' : page,
            'sortBy' : sort_by
        }
        
        
        if language:
            params['language'] = language
            
        if source:
            params['sources'] = source
            
        if domain:
            params['domain'] = domain
        
        if from_date:
            params['from'] = from_date
            
        if to_date:
            params['to'] = to_date
            
        
        logger.info(
            f"""Fetching Articles {keyword} |
            from {EVERYTHING_ENDPOINT} |
            page {page}"""
        )
        
        return self.get_response(
            params=params,
            encpoints=EVERYTHING_ENDPOINT
        )
        
        

    #^------------------------------
    #^       TOP_HEADLINES
    #^------------------------------
      
    def get_top_headlines(
        self,
        keyword=None,
        country=None,
        category=None,
        sources=None,
        page_size=DEFAULT_PAGE_SIZE,
        page=DEFAULT_PAGE,
    ):
        
        
        #*QUERY PARAMS
                
        params = {
            'pageSize':page_size,
            'page':page
        }
        
        
        if keyword:
            params['q'] = keyword
            
        if country:
            params['country'] = country
            
        if category:
            params['category'] = category
            
        if sources:
            params['sources'] = sources
            
        
        logger.info(
            f"""fethcing top headlines |
            page: {page}
            """
        )
        
        return self.get_response(
            params=params,
            encpoints=TOP_HEADLINES_ENDPOINT
        )
        
        
    
    
    def get_sources(
        self,
        category=None,
        language=None,
        country=None,
    ):
        """
        Fetch available News API sources.

        Returns raw JSON response.
        """

        params = {}

        if category:
            params["category"] = category

        if language:
            params["language"] = language

        if country:
            params["country"] = country

        logger.info(
            "Fetching News API sources..."
        )

        return self._request(
            endpoint=SOURCES_ENDPOINT,
            params=params,
        )