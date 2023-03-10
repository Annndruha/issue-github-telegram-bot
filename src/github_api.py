# Marakulin Andrey https://github.com/Annndruha
# 2023

import requests


class Github:
    def __init__(self, organization_nickname, token):
        self.issue_url = 'https://api.github.com/repos/' + organization_nickname + '/{}/issues'
        self.org_repos_url = f'https://api.github.com/orgs/{organization_nickname}/repos'
        self.org_members_url = f'https://api.github.com/orgs/{organization_nickname}/members'

        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def open_issue(self, repo, title, comment):
        payload = {'title': title, 'body': comment}
        r = requests.post(self.issue_url.format(repo), headers=self.headers, json=payload)
        if 'Issues are disabled for this repo' in r.text:
            raise GithubIssueDisabledError
        return r

    def get_repos(self, page):
        data = {'sort': 'pushed', 'per_page': 9, 'page': page}
        r = requests.get(self.org_repos_url, headers=self.headers, params=data)
        return r.json()

    def close_issue(self, repo, number_str, comment=''):
        url = self.issue_url.format(repo) + '/' + number_str
        payload = {'state': 'closed', 'body': comment}
        r = requests.patch(url, headers=self.headers, json=payload)
        return r

    def reopen_issue(self, repo, number_str):
        url = self.issue_url.format(repo) + '/' + number_str
        payload = {'state': 'open'}
        r = requests.patch(url, headers=self.headers, json=payload)
        return r.json(), r.status_code

    def get_issue(self, repo, number_str):
        url = self.issue_url.format(repo) + '/' + number_str
        r = requests.get(url, headers=self.headers)
        return r.json(), r.status_code

    def get_issue_human_link(self, repo, number_str):
        url = self.issue_url.format(repo) + '/' + number_str
        return url.replace('api.github.com/repos', 'github.com')

    def get_members(self, page):
        data = {'sort': 'full_name', 'per_page': 9, 'page': page}
        r = requests.get(self.org_members_url, headers=self.headers, params=data)
        return r.json()

    def set_assignee(self, repo, number_str, member_login, comment):
        url = self.issue_url.format(repo) + '/' + number_str
        payload = {'assignees': [member_login], 'body': comment}
        r = requests.patch(url, headers=self.headers, json=payload)
        return r


class GithubIssueDisabledError(Exception):
    pass
