import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NBAStatsPipeline:
    def __init__(self):
        self.api_key = os.getenv('SPORTDATA_API_KEY')
        print(f"API Key loaded: {'*' * len(str(self.api_key))}")
        
        # Updated base URL for sportsdata.io
        self.base_url = "https://api.sportsdata.io/v3/nba"
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = os.getenv('DYNAMODB_TABLE_NAME')

    def fetch_player_stats(self, season="2024"):
        """Fetch player statistics from sportsdata.io"""
        # Using the standings endpoint as a test
        url = f"{self.base_url}/scores/json/Standings/{season}"
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key
        }
        
        try:
            print(f"Attempting to fetch data from: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stats: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text[:200]}...")  # Print first 200 chars
            return None

def main():
    pipeline = NBAStatsPipeline()
    
    print("Testing NBA Stats Pipeline...")
    stats = pipeline.fetch_player_stats()
    if stats:
        print(json.dumps(stats, indent=2))
    else:
        print("Failed to fetch stats")

if __name__ == "__main__":
    main()
