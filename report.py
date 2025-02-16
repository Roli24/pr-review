import json

class Report:
    @staticmethod
    def generate(sonarqube_results, ollaman_results, output_path):
        report = {
            'sonarqube': sonarqube_results,
            'ollaman': ollaman_results
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)