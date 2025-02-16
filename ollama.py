import requests
import json
from .config import OLLAMAN_API_URL

class Ollaman:
    @staticmethod
    def format_issues(issues):
        formatted_issues = []
        for issue in issues['issues']:
            formatted_issues.append(f"- {issue['message']} (line {issue['line']})")
        return "\n".join(formatted_issues)

    @staticmethod
    def run_analysis(issues):
        formatted_issues = Ollaman.format_issues(issues)
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