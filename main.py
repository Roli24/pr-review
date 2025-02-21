from .sonarqube import SonarQube
from .ollama import Ollaman
from .report import Report
from .config import REPORT_PATH, GITHUB_REPO, GITHUB_PR_NUMBER, GITHUB_TOKEN
from .git_utils import run_analysis_on_changed_code

def main():
    # Get GitHub PR diff
    modified_files = run_analysis_on_changed_code(GITHUB_REPO, GITHUB_PR_NUMBER, GITHUB_TOKEN)
    print("GitHub PR diff:", modified_files)

    SonarQube.run_analysis_on_changed_code(modified_files)   
    #sonarqube_results = SonarQube.get_results(modified_files)
   
    
    # Perform performance analysis
   # performance_analysis = analyze_performance(sonarqube_results, ollaman_results)
    
    # Generate PR summary
    #pr_summary = generate_pr_summary(git_diff)
    #print(f"PR summary: {pr_summary}")

    # Generate report
    #Report.generate(sonarqube_results, ollaman_results, REPORT_PATH)
    print(f"PR review report generated: {REPORT_PATH}")

if __name__ == "__main__":
    main()