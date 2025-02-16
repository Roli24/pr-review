import requests
import json
from .config import OLLAMAN_API_URL

class Ollaman:
    @staticmethod
    def format_issues(issues):
        formatted_issues = []
        for issue in issues['issues']:
            start_line = issue['textRange']['startLine']
            end_line = issue['textRange']['endLine']
            formatted_issues.append(f"- {issue['message']} (start line {start_line}) (end line {end_line})")
        return "\n".join(formatted_issues)


    @staticmethod
    def format_additional_metrics(metrics):
        formatted_metrics = []
        for metric in metrics['component']['measures']:
            formatted_metrics.append(f"{metric['metric']}: {metric['value']}")
        return "\n".join(formatted_metrics)

    @staticmethod
    def run_analysis(issues, additional_metrics, git_diff):
        formatted_issues = Ollaman.format_issues(issues)
        #formatted_metrics = Ollaman.format_additional_metrics(additional_metrics)
        prompt = (
            "Analyze and optimize the code. Identify issues and provide an improved version with explanations:\n\n"
            "### Issues Identified:\n"
            f"{formatted_issues}\n\n"
            "### Git Diff Changes:\n"
            f"{git_diff}\n\n"
            "### Optimized Code:\n"
            "```java\n"
            "(Provide the improved version of the code)\n"
            "```\n\n"
            "### Explanations:\n"
            "- Explain what was changed and why."
        ) 
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