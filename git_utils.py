import os
import subprocess
import requests
import re
import json
import ollama
import os


def get_changed_files(repo, pr_number, token):
    url = f"https://api.github.com/repos/Roli24/SharedSolutions/pulls/1"
    headers = {
        "Authorization": f"token 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",
        "Accept": "application/vnd.github.v3.diff"  # Get raw diff format
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    diff_text = response.text

    changed_files = set()
    for line in diff_text.split("\n"):
        match = re.match(r"diff --git a/(.*?) b/", line)
        if match:
            changed_files.add(match.group(1))

    return changed_files

def checkout_pr_branch(repo, pr_number):
    """Clones the repo and checks out the PR branch."""
    os.system(f"git clone https://github.com/Roli24/SharedSolutions.git")
    repo_name = repo.split("/")[-1]
    os.chdir(repo_name)

    os.system(f"git fetch origin pull/1/head:pr-1")
    os.system(f"git checkout pr-1")

import os
import subprocess

def run_sonar_analysis(changed_files):
    """Runs SonarQube on the changed files."""
    sonar_scanner_path = os.path.expanduser("~/sonar-scanner/sonar-scanner-4.6.2.2472-macosx/bin/sonar-scanner")

    # Filter out non-existent files
    existing_files = [file for file in changed_files if os.path.exists(file)]
    absolute_files = [os.path.abspath(file) for file in changed_files if os.path.exists(file)]


    if not existing_files:
        print("⚠️ No valid changed files found. Skipping SonarQube analysis.")
        return
    print("🔍 Files to analyze:", existing_files)


    sonar_cmd = [
        sonar_scanner_path,
        "-Dsonar.projectKey=Sonar_Test",
        "-Dsonar.sources=" + ",".join(absolute_files),  # Only analyze changed files
        "-Dsonar.java.binaries=.",  # Trick SonarQube to not complain (empty directory)
        "-Dsonar.host.url=http://localhost:9001",
        "-Dsonar.login=sqp_d3b5f3ae2635d7c87e6522d6965e030338e61e01"
        "-Dsonar.analysis.mode=preview" \
        "-Dsonar.report.export.path=sonar-report.json"

    ]

    subprocess.run(sonar_cmd)



def fetch_sonar_issues():
    sonar_token = "sqp_d3b5f3ae2635d7c87e6522d6965e030338e61e01"
    sonar_url = "http://localhost:9001/api/issues/search?componentKeys=Sonar_Test&resolved=false&types=BUG,VULNERABILITY,CODE_SMELL"

    curl_command = [
        "curl", "-u", f"{sonar_token}:", sonar_url
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        with open("sonar-report.json", "w") as file:
            file.write(result.stdout)
        print("✅ SonarQube report saved as sonar-report.json")
    else:
        print(f"❌ Failed to fetch SonarQube issues: {result.stderr}")


def parse_sonar_issues():
    """Reads the SonarQube JSON report and extracts issues with line numbers."""
    with open("sonar-report.json", "r") as file:
        data = json.load(file)

    issues = []
    for issue in data.get("issues", []):
        file_path = issue["component"].replace(":", "/")  # Normalize file path
        line = issue.get("line", None)
        message = issue.get("message", "")
        severity = issue.get("severity", "INFO")

        if line:
            issues.append({
                "file": file_path,
                "line": line,
                "message": message,
                "severity": severity
            })

    return issues



def suggest_fix(file_path, line, message):
    """Generates an improved code suggestion using Ollama AI."""
    
    # Remove 'Sonar_Test/' from the path if present
    corrected_file_path = file_path.replace("Sonar_Test/", "")

    if not os.path.exists(corrected_file_path):
        print(f"❌ File not found: {corrected_file_path}")
        return None

    with open(corrected_file_path, "r") as file:
        lines = file.readlines()

    if line > len(lines):
        print(f"❌ Line {line} is out of range for {corrected_file_path}")
        return None  # Skip if line number is out of range

    code_snippet = lines[line - 1]  # Extract the affected line

    prompt = f"""
    The following code has a SonarQube issue:

    **File**: {corrected_file_path}
    **Line {line}**: {code_snippet.strip()}
    **Issue**: {message}

    Please suggest an improved version of this line with best practices:
    """

    import ollama
    response = ollama.chat(model="codellama", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]  # Extract AI-generated suggestion

    """Generates an improved code suggestion using Ollama AI."""
    with open(file_path, "r") as file:
        lines = file.readlines()

    if line > len(lines):
        return None  # Skip if line number is out of range

    code_snippet = lines[line - 1]  # Extract the affected line

    prompt = f"""
    The following code has a SonarQube issue:
    
    **File**: {file_path}
    **Line {line}**: {code_snippet.strip()}
    **Issue**: {message}

    Please suggest an improved version of this line with best practices:
    """

    response = ollama.chat(model="codellama", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]  # Extract AI-generated suggestion


def get_latest_commit_sha():
    """Fetches the latest commit SHA from the PR."""
    url = "https://api.github.com/repos/Roli24/SharedSolutions/pulls/1"
    headers = {
        "Authorization": "token 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",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch commit SHA: {response.status_code} - {response.text}")
        return None

    try:
        data = response.json()
        return data.get("head", {}).get("sha")
    except json.JSONDecodeError:
        print("❌ JSON decoding failed: Empty or invalid response received from GitHub API.")
        print(f"Response content: {response.text}")
        return None

def get_pr_files():
    """Fetches the list of files changed in the PR."""
    url = "https://api.github.com/repos/Roli24/SharedSolutions/pulls/1/files"
    headers = {
        "Authorization": f"token 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",
        "Accept": "application/vnd.github.v3+json"  # Correct header
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # Ensure JSON is returned
    print(f"❌ Failed to fetch PR files: {response.status_code} - {response.text}")
    return []


def get_diff_position(file, line):
    """Finds the GitHub diff position for a given file and line number."""
    file = file.replace("Sonar_Test/", "", 1)  # Ensure path matches GitHub API response
    files = get_pr_files()
    for f in files:
        if f["filename"] == file:
            patch = f["patch"]
            diff_lines = patch.split("\n")
            pos = 0
            for diff_line in diff_lines:
                if diff_line.startswith("@@"):  # Found a diff hunk
                    parts = diff_line.split(" ")
                    new_file_info = parts[2]  # e.g., "+22,5"
                    start_line = int(new_file_info.split(",")[0][1:])  # Extract "22"
                    pos = start_line
                elif diff_line.startswith("+"):  # This is a line that was added
                    pos += 1
                    if pos == line:
                        return pos  # Found the position

    print(f"❌ No matching diff position found for {file}:{line}")
    return None

    """Finds the GitHub diff position for a given file and line number."""
    files = get_pr_files()
    for f in files:
        if f["filename"] == file:
            patch = f.get("patch", "")
            diff_lines = patch.split("\n")
            pos = None
            new_line = None

            for diff_line in diff_lines:
                if diff_line.startswith("@@"):
                    # Extract new file position
                    parts = diff_line.split(" ")
                    new_file_info = parts[2]  # Example: +22,5 or +22
                    new_start = new_file_info[1:]  # Remove '+'

                    if "," in new_start:
                        new_line = int(new_start.split(",")[0])
                    else:
                        new_line = int(new_start)

                    pos = new_line
                elif diff_line.startswith("+"):
                    if pos is not None:
                        if pos == line:
                            return pos  # Return the correct position
                        pos += 1  # Increment the position for added lines

    print(f"❌ No matching diff position found for {file}:{line}")
    return None
    """Finds the GitHub diff position for a given file and line number."""
    files = get_pr_files()
    for f in files:
        if f["filename"] == file:
            patch = f["patch"]
            diff_lines = patch.split("\n")
            pos = 0
            for diff_line in diff_lines:
                if diff_line.startswith("@@"):  # Found a diff hunk
                    parts = diff_line.split(" ")
                    new_file_info = parts[2]  # e.g., "+22,5"
                    start_line = int(new_file_info.split(",")[0][1:])  # Extract "22"
                    pos = start_line
                elif diff_line.startswith("+"):  # This is a line that was added
                    pos += 1
                    if pos == line:
                        return pos  # Found the position

    print(f"❌ No matching diff position found for {file}:{line}")
    return None

def post_pr_comment(file, line, comment):
    """Posts a review comment on a GitHub PR at a specific diff position."""
    commit_sha = get_latest_commit_sha()
    if not commit_sha:
        return

    position = get_diff_position(file, line)
    if position is None:
        print(f"❌ Skipping comment for {file}:{line} (position not found).")
        return

    url = f"https://api.github.com/repos/Roli24/SharedSolutions/pulls/1"
    headers = {
        "Authorization": f"token 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",
        "Accept": "application/vnd.github.v3.diff"  # Get raw diff format
    }
    payload = {
        "body": comment,
        "commit_id": commit_sha,
        "path": file,
        "position": position  # GitHub expects diff position
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print(f"✅ Comment added to {file}:{line}")
    else:
        print(f"❌ Failed to add comment: {response.json()}")



if __name__ == "__main__":
    REPO = "Roli24/SharedSolutions"
    PR_NUMBER = 1
    GITHUB_TOKEN = "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"

    changed_files = get_changed_files(REPO, PR_NUMBER, GITHUB_TOKEN)
    checkout_pr_branch(REPO, PR_NUMBER)
    run_sonar_analysis(changed_files)
    fetch_sonar_issues()
    sonar_issues = parse_sonar_issues()
    print(sonar_issues)

    for issue in sonar_issues:
        pr_comment = f"🔍 **SonarQube Issue:** {issue['message']}"
        post_pr_comment(issue["file"], issue["line"], pr_comment)
   