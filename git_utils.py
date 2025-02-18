import requests
import re

def get_github_pr_diff(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff"  # Request raw diff format
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        diff_text = response.text

        files_with_changes = {}
        current_file = None
        changed_lines = []

        # Parse the diff line by line
        for line in diff_text.split("\n"):
            # Match file name changes
            match = re.match(r"diff --git a/(.*?) b/", line)
            if match:
                if current_file and changed_lines:
                    files_with_changes[current_file] = "\n".join(changed_lines)
                current_file = match.group(1)
                changed_lines = []
            
            # Capture added/modified lines (ignoring deletions)
            elif line.startswith("+") and not line.startswith("+++"):
                changed_lines.append(line[1:])  # Remove leading '+'
        
        # Save last file's changes
        if current_file and changed_lines:
            files_with_changes[current_file] = "\n".join(changed_lines)

        print ("files_with_changes", files_with_changes)
        return files_with_changes

    except requests.exceptions.RequestException as e:
        print(f"Error getting GitHub PR diff: {e}")
        return {}
