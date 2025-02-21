import subprocess
from .config import SONARQUBE_URL, SONARQUBE_TOKEN, PROJECT_KEY, SONAR_SCANNER_PATH, GITHUB_TOKEN, GITHUB_PR_NUMBER
import os
import tempfile


class SonarQube:
    @staticmethod
    def run_analysis_on_changed_code(code_text):
        print(f"Running SonarQube analysis on PR {GITHUB_PR_NUMBER}...")
        # Create a temporary file to store the code
        if isinstance(code_text, dict):
            code_text = str(code_text)
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.java') as temp_file:
            temp_file.write(code_text)
            temp_file_path = temp_file.name
        
        print("Temporary file created:", temp_file_path)

         # Read and print the contents of the temporary file
        with open(temp_file_path, 'r') as temp_file:
            file_contents = temp_file.read()
            print("Contents of the temporary file:")
            print(file_contents)
        try:
            # Run SonarQube analysis on the temporary file
            result = subprocess.run([
                SONAR_SCANNER_PATH,
                f'-Dsonar.projectKey={PROJECT_KEY}',
                f'-Dsonar.host.url={SONARQUBE_URL}',
                f'-Dsonar.login={SONARQUBE_TOKEN}',
                f'-Dsonar.sources={temp_file_path}'
                '-X'  # Enable full debug logging
            ], check=True, capture_output=True, text=True)

            print("SonarQube analysis completed successfully.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error: ", e.stderr)
            print("Exit Code: ", e.returncode)
            print("Command: ", e.cmd)
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


    @staticmethod
    def get_results():
        # Fetch PR analysis results directly from SonarQube
        response = requests.get(
            f'{SONARQUBE_URL}/api/issues/search',
            params={
                "componentKeys": PROJECT_KEY,
                "pullRequest": GITHUB_PR_NUMBER,  # Fetch results for the PR
            },
            auth=(SONARQUBE_TOKEN, '')
        )
        return response.json()

    @staticmethod
    def get_additional_metrics():
        metrics = ['coverage', 'duplicated_lines_density', 'code_smells', 'bugs', 'vulnerabilities']
        metrics_str = ','.join(metrics)
        response = requests.get(f'{SONARQUBE_URL}/api/measures/component?component={PROJECT_KEY}&metricKeys={metrics_str}', 
                                auth=(SONARQUBE_TOKEN, ''))
        return response.json()

