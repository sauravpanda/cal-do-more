from github import Github
from github import Auth
import os

access_token = os.environ.get("GITHUB_PAT_TOKEN")
auth = Auth.Token(access_token)

g = Github(auth=auth)
repo = g.get_repo("Cloud-Code-AI/cal-do-more")


def create_github_issue(issueTitle, description):
    # print(issueTitle, "desc", description)
    repo.create_issue(title=issueTitle,
                      body=description)

    return "Issue Created"


def get_github_issue(number):
    issue = repo.get_issue(number)
    return issue


def get_all_open_github_issues():
    open_issues = repo.get_issues(state='open')
    return open_issues


def close_github_issue(number):
    issue = get_github_issue(number)
    issue.edit(state='closed')
    return "Issue Closed"


if __name__ == "__main__":
    # print(create_github_issue(
    #     "New Example Issue",
    #     "This is a just a test issue. Delete later",
    #     labels=[],
    #     assignee="Rsakhuja"
    # ))

    # print(get_github_issue(28))
    # open_issues = get_all_open_github_issues()
    # for issue in open_issues:
    #     print(issue)

    print(close_github_issue(28))
