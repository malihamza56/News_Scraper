"""
Exporter: Exports Data to Excel and CSV
"""
from src.config.logger import logger
from src.config.config import(
    EXCEL_PATH,
    CSV_PATH,
)

class Exporter:
    
    def __init__(self,dataframe):
        self.df = dataframe
        
    def export_csv(self):
            
            try:
                
                logger.info("Making Serailized csv")
                
                self.df.to_csv(
                    CSV_PATH,
                    index=False
                )
    
                logger.info("csv Serailized Successful")
                
            except Exception as e:
                logger.error(f"Failed to Seralized csv | {e}")
                raise
            
    def export_excel(self):
        
        try:
            
            logger.info("Making Serailized Excel")
            
            self.df.to_excel(
                EXCEL_PATH,
                index=False
            )

            logger.info("Excel Serailized Successful")
            
        except Exception as e:
            logger.error(f"Failed to Seralized Excel | {e}")
            raise
        

        
