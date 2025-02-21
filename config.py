import os

# Configuration
SONARQUBE_URL = 'http://localhost:9001'
SONARQUBE_TOKEN = 'sqp_d3b5f3ae2635d7c87e6522d6965e030338e61e01'
PROJECT_KEY = 'Sonar_Test'
OLLAMAN_API_URL = 'http://localhost:11434/api/generate'
SONAR_SCANNER_PATH = os.path.expanduser('~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner')
REPORT_PATH = '/Users/in45828930/Documents/pr-review/pr_review_report.json'

# GitHub Configuration
GITHUB_REPO = 'Roli24/SharedSolutions'
GITHUB_PR_NUMBER = 1
GITHUB_TOKEN = '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'