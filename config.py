import os

# Configuration
SONARQUBE_URL = 'http://localhost:9001'
SONARQUBE_TOKEN = 'sqp_cdd08fb86e82de71d7b4d27c3419a26b43b7437c'
PROJECT_KEY = 'New_Test'
OLLAMAN_API_URL = 'http://localhost:11434/api/generate'
SONAR_SCANNER_PATH = os.path.expanduser('~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner')
REPORT_PATH = '/Users/in45828930/Documents/pr-review/pr_review_report.json'

# GitHub Configuration
GITHUB_REPO = 'Roli24/SharedSolutions'
GITHUB_PR_NUMBER = 1
GITHUB_TOKEN = ''