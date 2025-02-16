from .sonarqube import SonarQube
from .ollaman import Ollaman
from .report import Report
from .config import REPORT_PATH

def main():
    SonarQube.run_analysis()
    sonarqube_results = SonarQube.get_results()
    ollaman_results = Ollaman.run_analysis(sonarqube_results)
    Report.generate(sonarqube_results, ollaman_results, REPORT_PATH)
    print(f"PR review report generated: {REPORT_PATH}")

if __name__ == "__main__":
    main()