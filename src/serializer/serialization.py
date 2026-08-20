"""
Serializer Module: Serialize The Clean Data into EXCEL JSON & CSV
"""
from src.config.logger import logger
from src.config.config import(
    CLEAN_JSON_PATH
)

class Serialization:
    
    def __init__(self,dataframe):
        self.df = dataframe
        
    
    def save_json(self):
        
        try:
            
            logger.info("Making Serailized Json")
            
            self.df.to_json(
                CLEAN_JSON_PATH,
                index=False,
                orient="records"
            )

            logger.info("Json Serailized Successful")
            
        except Exception as e:
            logger.error(f"Failed to Seralized Json | {e}")
            raise
        
    