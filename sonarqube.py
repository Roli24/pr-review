import subprocess
import requests
from .config import SONARQUBE_URL, SONARQUBE_TOKEN, PROJECT_KEY, SONAR_SCANNER_PATH, DIRECTORY_TO_ANALYZE

class SonarQube:
    @staticmethod
    def run_analysis():
        try:
            result = subprocess.run([SONAR_SCANNER_PATH, 
                                     f'-Dsonar.projectKey={PROJECT_KEY}', 
                                     f'-Dsonar.sources={DIRECTORY_TO_ANALYZE}', 
                                     f'-Dsonar.host.url={SONARQUBE_URL}', 
                                     f'-Dsonar.login={SONARQUBE_TOKEN}', 
                                     f'-Dsonar.scm.disabled=true'], 
                                    check=True, capture_output=True, text=True)
            print("SonarQube analysis completed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error running SonarQube analysis: {e}")
            print(e.stdout)
            print(e.stderr)

    @staticmethod
    def get_results():
        response = requests.get(f'{SONARQUBE_URL}/api/issues/search?componentKeys={PROJECT_KEY}', 
                                auth=(SONARQUBE_TOKEN, ''))
        return response.json()

    @staticmethod
    def get_additional_metrics():
        metrics = ['coverage', 'duplicated_lines_density', 'code_smells', 'bugs', 'vulnerabilities']
        metrics_str = ','.join(metrics)
        response = requests.get(f'{SONARQUBE_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys={metrics_str}', 
                                auth=(SONARQUBE_TOKEN, ''))
        return response.json()