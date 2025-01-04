import __main__
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()


# Replace these with your information
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OWNER = "Significant-Gravitas"  # e.g., "octocat"
REPO = "AutoGPT"    # e.g., "Hello-World"
BASE_URL = "https://api.github.com"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


# function to get the commits from the repository
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


# function to get the pull requests from the repository
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



# function to get the issues from the repository

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



# function to get the no of forks from the repository
def print_forks():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    # Send GET request to GitHub API
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repo_data = response.json()['forks_count']
        print(f"Forks count: {repo_data}")
    else:
        print("Failed to fetch forks count:", response.json())


# function to get the no of stars from the repository
def print_stars():
    url = f"{BASE_URL}/repos/{OWNER}/{REPO}"
    # Send GET request to GitHub API
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        repo_data = response.json()['stargazers_count']
        print(f"Stars: {repo_data}")
    else:
        print("Failed to fetch forks count:", response.json())
    

# function to check if the pull request is merged or not
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


# function to check if the pull request is made by the user or not
def check_user_pull_request(pull_number, username):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pull_number}"
    response = requests.get(url, headers=HEADERS)
    pull_request=response.json()
    pull_request_user=pull_request["user"]["login"]

    if(pull_request_user==username):
        print(f"Pull request {pull_number} was made by {pull_request_user}")
    else:
        print(f"Pull request {pull_number} was not made by {username}")



# function to get the timestamp of the pull request initiated and check if the pull request is created after 31st December 2024
def get_pull_request_timestamp(pull_number):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pull_number}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        pr_data = response.json()
        created_at = pr_data['created_at']
        print(f"Pull Request #{pull_number} created at: {created_at}")
        
        if created_at > "2024-12-31T00:00:00Z":
            print(f"Pull request #{pull_number} is created after 31st December 2024.")
        else:
            print(f"Pull request #{pull_number} is created before 31st December 2024.")
    else:
        print(f"Error fetching pull request {pull_number}: {response.status_code}, Response: {response.json()}")



# function to get the conversation of the pull request
def fetch_conversation_comments(pull_number):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pull_number}"

    # Send the GET request to fetch pull request details
    response = requests.get(url, headers=HEADERS)

    # Check if the request was successful
    if response.status_code == 200:
        pr_data = response.json()
        print(f"Title: {pr_data['title']}")
        print(f"Description (Body): {pr_data['body']}")
    else:
        print(f"Failed to fetch PR details: {response.status_code} - {response.text}")


def get_comment_text(comment_url):
    """Fetch the text of a specific comment from a pull request using web scraping."""
    response = requests.get(comment_url, headers=HEADERS)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_body = soup.find('div', {'class': 'comment-body'})
        if comment_body:
            print(f"Comment Text: {comment_body.get_text(strip=True)}")
        else:
            print("Failed to find the comment text in the HTML.")
    else:
        print(f"Failed to fetch comment: {response.status_code} - {response.text}")


if __name__ == "__main__":
    print("Fetching the no of stars")
    print_stars()

    print("-"*50)

    print("Checking if pull request merged")
    get_pull_request_state(9185)

    print("-"*50)

    print("Checking if the pull number is of the user or not")
    check_user_pull_request(9185, "SyedNaveedM")
    check_user_pull_request(9185, "Pwuts")


    print()
    print("-"*50)
    
    print("Checking if the pull request is created after 31st December 2024")
    get_pull_request_timestamp(9097)

    print()
    print("-"*50)

    print("Fetching the text of the comment containing the description of the pull request")
    get_comment_text("https://github.com/Significant-Gravitas/AutoGPT/pull/9185#issue-2767614409")





