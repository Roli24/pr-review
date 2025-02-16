import os

# Configuration
SONARQUBE_URL = 'http://localhost:9001'
SONARQUBE_TOKEN = 'sqa_570b61032514cf67e78c2c1041531839b288d3f4'
PROJECT_KEY = 'Test4'
OLLAMAN_API_URL = 'http://localhost:11434/api/generate'
SONAR_SCANNER_PATH = os.path.expanduser('~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner')
DIRECTORY_TO_ANALYZE = '/Users/in45828930/Documents/pr-review' 
REPORT_PATH = '/Users/in45828930/Downloads/pr_review_report.json'

# GitHub Configuration
GITHUB_REPO = 'Roli24/SharedSolutions'
GITHUB_PR_NUMBER = 1
GITHUB_TOKEN = ''