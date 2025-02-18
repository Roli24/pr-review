import subprocess
from .config import SONARQUBE_URL, SONARQUBE_TOKEN, PROJECT_KEY, SONAR_SCANNER_PATH

import subprocess
from tempfile import NamedTemporaryFile
import requests

class SonarQube:
    @staticmethod
    def run_analysis_on_changed_code(files_with_changes):
        for file_path, changed_code in files_with_changes.items():
            print(f"Analyzing {file_path}...")

            # Create a temporary file to store the changed code
            with NamedTemporaryFile(delete=False, suffix=".java") as temp_file:
                temp_file.write(changed_code.encode())
                temp_file_path = temp_file.name

            
            # Run SonarQube analysis on this temporary file
            try:
                result = subprocess.run([SONAR_SCANNER_PATH, 
                                 f'-Dsonar.projectKey={PROJECT_KEY}', 
                                 f"-Dsonar.sources={temp_file_path}",
                                 f'-Dsonar.host.url={SONARQUBE_URL}', 
                                 f'-Dsonar.login={SONARQUBE_TOKEN}', 
                                 f'-Dsonar.scm.disabled=true', 
                                 f'-Dsonar.exclusions=**/Pictures/**'], 
                                check=True, capture_output=True, text=True)
                print("SonarQube analysis completed successfully." + result.stdout)
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error running SonarQube analysis for {file_path}: {e}")
                print(e.stdout)
                print(e.stderr)


    @staticmethod
    def get_results(files_with_changes):
        file_paths = ",".join(files_with_changes.keys())  # Convert file list to SonarQube format
        
        response = requests.get(
            f'{SONARQUBE_URL}/api/issues/search',
            params={
                "componentKeys": PROJECT_KEY,
                "file": file_paths,  # Only get results for changed files
            },
            auth=(SONARQUBE_TOKEN, ''))
        return response.json()

    
    @staticmethod
    def get_additional_metrics():
        metrics = ['coverage', 'duplicated_lines_density', 'code_smells', 'bugs', 'vulnerabilities']
        metrics_str = ','.join(metrics)
        response = requests.get(f'{SONARQUBE_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys={metrics_str}', 
                                auth=(SONARQUBE_TOKEN, ''))
        return response.json()