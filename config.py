import os

# Configuration
SONARQUBE_URL = 'http://localhost:9001'
SONARQUBE_TOKEN = 'sqp_00af0dfe325275f9347e27ad3552b424e5d2b0c1'
PROJECT_KEY = 'Test'
OLLAMAN_API_URL = 'http://localhost:11434/api/generate'
SONAR_SCANNER_PATH = os.path.expanduser('~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner')
DIRECTORY_TO_ANALYZE = '/Users/in45828930/Documents/pr-review'  # Specify the directory to analyze
REPORT_PATH = '/Users/in45828930/Downloads/pr_review_report.json'