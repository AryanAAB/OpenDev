import __main__
import requests

# Replace these with your information
GITHUB_TOKEN = "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"
OWNER = "Significant-Gravitas"  # e.g., "octocat"
REPO = "AutoGPT"    # e.g., "Hello-World"
BASE_URL = "https://api.github.com"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_commits():
    """Fetch the latest commits from the repository."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/commits"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        commits = response.json()
        for commit in commits:
            print(f"Commit: {commit['commit']['message']}")
            print(f"Author: {commit['commit']['author']['name']}")
            print(f"Date: {commit['commit']['author']['date']}")
            print("-" * 50)
    else:
        print("Failed to fetch commits:", response.json())

def get_pull_requests(state="all"):
    """Fetch pull requests (open, closed, or all)."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/pulls"
    params = {"state": state}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        pull_requests = response.json()
        for pr in pull_requests:
            print(f"PR Title: {pr['title']}")
            print(f"Author: {pr['user']['login']}")
            print(f"State: {pr['state']}")
            print(f"Created At: {pr['created_at']}")
            print("-" * 50)
    else:
        print("Failed to fetch pull requests:", response.json())

def get_issues(state="all"):
    """Fetch issues (open, closed, or all)."""
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}/issues"
    params = {"state": state}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            print(f"Issue Title: {issue['title']}")
            print(f"Author: {issue['user']['login']}")
            print(f"State: {issue['state']}")
            print(f"Created At: {issue['created_at']}")
            print("-" * 50)
    else:
        print("Failed to fetch issues:", response.json())

def print_forks():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    # Send GET request to GitHub API
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repo_data = response.json()['forks_count']
        print(f"Forks count: {repo_data}")
    else:
        print("Failed to fetch forks count:", response.json())

def print_stars():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    # Send GET request to GitHub API
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repo_data = response.json()['stargazers_count']
        print(f"Stars: {repo_data}")
    else:
        print("Failed to fetch forks count:", response.json())
    


def get_pull_request_state(pull_number):
    """Fetch the PR details to check if it has been merged or closed."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pull_number}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        pr_data = response.json()
        merged = pr_data['merged']
        state = pr_data['state']
        print(f"Pull Request #{pull_number} - State: {state}, Merged: {merged}")
        if merged:
            print(f"Pull request #{pull_number} has been merged.")
        elif state == 'closed':
            print(f"Pull request #{pull_number} is closed but not merged.")
        else:
            print(f"Pull request #{pull_number} is still open.")
    else:
        print(f"Error fetching pull request {pull_number}: {response.status_code}, Response: {response.json()}")


if __name__ == "__main__":
    print("Fetching commits...")
    get_commits()
    
    print("\nFetching pull requests...")
    get_pull_requests()
    
    print("\nFetching issues...")
    get_issues()

    print("Fetching the no of forks")
    print_forks()

    print("-"*50)

    print("Fetching the no of stars")
    print_stars()

    print("-"*50)

    print("Checking if pull request merged")
    get_pull_request_state(9172)

