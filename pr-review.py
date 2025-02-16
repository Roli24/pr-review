import subprocess
import requests
import json
import os

# Configuration
SONARQUBE_URL = 'http://localhost:9001'
SONARQUBE_TOKEN = 'sqp_00af0dfe325275f9347e27ad3552b424e5d2b0c1'
PROJECT_KEY = 'Test'
OLLAMAN_API_URL = 'http://localhost:11434/api/generate'
SONAR_SCANNER_PATH = os.path.expanduser('~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner')

def get_sonarqube_results():
    # Get SonarQube analysis results
    response = requests.get(f'{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}', 
                            auth=(SONARQUBE_TOKEN, ''))
    return response.json()

def run_sonarqube_analysis():
    # Run SonarQube Scanner
    try:
        result = subprocess.run([SONAR_SCANNER_PATH, 
                                 f'-Dsonar.projectKey={PROJECT_KEY}', 
                                 f'-Dsonar.sources=.', 
                                 f'-Dsonar.host.url={SONARQUBE_URL}', 
                                 f'-Dsonar.login={SONARQUBE_TOKEN}', 
                                 f'-Dsonar.scm.disabled=true', 
                                 f'-Dsonar.exclusions=**/Pictures/**'], 
                                check=True, capture_output=True, text=True)
        print("SonarQube analysis completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running SonarQube analysis: {e}")
        print(e.stdout)
        print(e.stderr)

def format_issues_for_ollaman(issues):
    # Format the issues for the Ollaman model
    formatted_issues = []
    for issue in issues['issues']:
        formatted_issues.append(f"- {issue['message']} (line {issue['line']})")
    return "\n".join(formatted_issues)

def run_ollaman_analysis(issues):
    # Run Ollaman model analysis by hitting the API
    formatted_issues = format_issues_for_ollaman(issues)
    print("formatted issues from sonar "+formatted_issues)
    prompt = f"Analyze and optimize the code. Identify issues and provide an improved version with explanations:\n\n### Issues Identified:\n{formatted_issues}\n\n### Optimized Code:\n```python\n(Provide the improved version of the code)\n```\n\n### Explanations:\n- Explain what was changed and why."
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
    try:
        print("Sending request to Ollaman API...")
        response = requests.post(OLLAMAN_API_URL, json=payload, timeout=180)  # 3-minute timeout
        response.raise_for_status()  # Raise an error for bad status codes
        print("Ollaman API response status code:", response.status_code)  # Debugging line
        print("Ollaman API response headers:", response.headers)  # Debugging line
        print("Ollaman API response text:", response.text)  # Debugging line
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollaman API: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from Ollaman API: {e}")
        print("Response text:", response.text)
        return {}

def generate_report(sonarqube_results, ollaman_results):
    # Combine results and generate a report
    report = {
        'sonarqube': sonarqube_results,
        'ollaman': ollaman_results
    }
    with open('/Users/in45828930/Downloads/pr_review_report.json', 'w') as f:
        json.dump(report, f, indent=4)

def main():
    run_sonarqube_analysis()
    sonarqube_results = get_sonarqube_results()
    ollaman_results = run_ollaman_analysis(sonarqube_results)
    generate_report(sonarqube_results, ollaman_results)
    print("PR review report generated: /Users/in45828930/Downloads/pr_review_report.json")

if __name__ == "__main__":
    main()