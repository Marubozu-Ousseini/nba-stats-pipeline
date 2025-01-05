import os
import json
import boto3
import requests
import logging
import watchtower
from datetime import datetime
from pythonjsonlogger import jsonlogger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
def setup_logger():
    logger = logging.getLogger('NBAStatsPipeline')
    logger.setLevel(logging.INFO)

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)
    logger.addHandler(console_handler)

    # CloudWatch handler
    try:
        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group='NBAStatsPipeline',
            log_stream=f'stats-collection-{datetime.now().strftime("%Y-%m-%d")}'
        )
        cloudwatch_handler.setFormatter(json_formatter)
        logger.addHandler(cloudwatch_handler)
    except Exception as e:
        logger.error(f"Failed to set up CloudWatch logging: {e}")

    return logger

class NBAStatsPipeline:
    def __init__(self):
        self.logger = setup_logger()
        self.api_key = os.getenv('SPORTDATA_API_KEY')
        self.base_url = "https://api.sportsdata.io/v3/nba"
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = os.getenv('DYNAMODB_TABLE_NAME')

        self.logger.info("Initialized NBA Stats Pipeline", 
                        extra={
                            'service': 'nba-stats',
                            'base_url': self.base_url,
                            'table_name': self.table_name
                        })

    def fetch_player_stats(self, season="2024"):
        """Fetch player statistics from sportsdata.io"""
        try:
            url = f"{self.base_url}/scores/json/Standings/{season}"
            self.logger.info(f"Fetching data from API", 
                           extra={
                               'url': url,
                               'season': season
                           })

            headers = {
                "Ocp-Apim-Subscription-Key": self.api_key
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.logger.info("Successfully fetched data", 
                           extra={
                               'teams_count': len(data),
                               'season': season
                           })
            return data

        except requests.exceptions.RequestException as e:
            self.logger.error("API request failed", 
                            extra={
                                'error': str(e),
                                'url': url,
                                'status_code': getattr(e.response, 'status_code', None)
                            })
            return None
        except Exception as e:
            self.logger.error("Unexpected error occurred", 
                            extra={
                                'error': str(e),
                                'error_type': type(e).__name__
                            })
            return None

def main():
    try:
        pipeline = NBAStatsPipeline()
        
        print("Testing NBA Stats Pipeline...")
        stats = pipeline.fetch_player_stats()
        
        if stats:
            print(json.dumps(stats[:2], indent=2))  # Show first 2 teams only
        else:
            print("Failed to fetch stats")

    except Exception as e:
        logging.error(f"Main execution failed: {e}")

if __name__ == "__main__":
    main()