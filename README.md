Week 1 Day 4 of 30 Days DevOps Challenge: Building an NBA statistics pipeline using AWS.

# NBA Stats Pipeline

## Project Overview
This project creates an automated data pipeline that collects and stores NBA team statistics using AWS services. It demonstrates core DevOps principles including cloud storage, API integration, automated data collection, and infrastructure as code.

## Architecture
The pipeline follows a serverless architecture pattern:
1. Fetches real-time NBA statistics from the SportsData.io API
2. Processes and transforms the data into structured formats
3. Stores the data in DynamoDB for efficient querying
4. Uses CloudWatch for comprehensive logging and monitoring
5. Runs on a scheduled basis using AWS Lambda

## Features
- Real-time NBA team statistics collection
- Automated data storage in DynamoDB
- Structured logging with CloudWatch integration
- Error handling and retry logic
- Lambda-based scheduling
- Decimal precision for statistical accuracy

## Technologies Used
- Python 3.x
- AWS DynamoDB
- AWS Lambda
- AWS CloudWatch
- SportsData.io API
- Boto3 (AWS SDK)
- Python JSON Logger

## Prerequisites
- AWS Account (Free Tier compatible)
- SportsData.io API key
- Python 3.8 or higher
- AWS CLI configured

## Setup Instructions
1. Clone the repository
```bash
git clone https://github.com/yourusername/nba-stats-pipeline.git
cd nba-stats-pipeline
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
```bash
# Create .env file with your credentials
SPORTDATA_API_KEY=your_api_key_here
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=nba-player-stats
```

4. Run the pipeline
```bash
python src/nba_stats.py
```

## Project Structure
```
nba-stats-pipeline/
├── src/
│   ├── __init__.py
│   ├── nba_stats.py
│   └── lambda_function.py
├── tests/
├── requirements.txt
├── README.md
└── .env
```

## Data Structure
The pipeline collects and stores the following statistics:
- Team identification information
- Win/Loss records
- Points per game
- Conference standings
- Division rankings
- Historical performance metrics

## AWS Infrastructure
- DynamoDB Table:
  - Partition Key: TeamID
  - Sort Key: Timestamp
  - Attributes: Team stats and metadata
- Lambda Function:
  - Memory: 256MB
  - Timeout: 30 seconds
  - Runtime: Python 3.9
- CloudWatch:
  - Structured JSON logging
  - Error tracking
  - Performance monitoring

## Error Handling
The pipeline includes comprehensive error handling for:
- API failures
- DynamoDB throttling
- Data transformation issues
- Network timeouts
- Invalid responses

## Monitoring and Logging
- Structured JSON logs
- CloudWatch metrics
- Error tracking
- Performance monitoring
- Data quality checks

## Cleanup Instructions
```bash
# Delete DynamoDB table
aws dynamodb delete-table --table-name nba-player-stats

# Remove Lambda function (if deployed)
aws lambda delete-function --function-name nba-stats-function

# Remove CloudWatch log groups
aws logs delete-log-group --log-group-name /aws/lambda/nba-stats-function
```

## Future Enhancements
- Add player-level statistics
- Implement data visualization
- Add historical data analysis
- Create API endpoints
- Add more sports leagues

## Contributing
Contributions are welcome! Please read our contributing guidelines and submit pull requests for any improvements.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- SportsData.io for providing the NBA statistics API
- AWS for cloud infrastructure
- The Python community for excellent libraries

## Contact
For questions or feedback, please open an issue in the GitHub repository.
