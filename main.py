from .sonarqube import SonarQube
from .ollama import Ollaman
from .report import Report
from .config import REPORT_PATH

def main():
    SonarQube.run_analysis()
    sonarqube_results = SonarQube.get_results()
    print("SonarQube results:", sonarqube_results)
    
    # Fetch additional metrics
    additional_metrics = SonarQube.get_additional_metrics()
    print("Additional SonarQube metrics:", additional_metrics)
    
    # Pass all data to Ollaman model
    ollaman_results = Ollaman.run_analysis(sonarqube_results, additional_metrics)
    Report.generate(sonarqube_results, ollaman_results, REPORT_PATH, additional_metrics)
    print(f"PR review report generated: {REPORT_PATH}")

if __name__ == "__main__":
    main()