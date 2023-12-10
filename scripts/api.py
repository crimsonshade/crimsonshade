import requests

README = "./README.md"
START_MARKER = '<!-- PROJECTS START -->'
END_MARKER = '<!-- PROJECTS END -->'
API_LINK = 'https://api.github.com/orgs/crmsn-xyz/repos'

def main():
    projects = fetch_projects()

    readme = ''
    with open(README, "r") as file:
        readme = file.read()

    insert_values(readme, projects)

    with open(README, "w") as file:
        file.write(readme)

def parse_project_injection(projects):
    res = ""
    number = 0
    for project in projects:
        number += 1
        repo_name = project.get('name')
        repo_url = project.get('html_url')
        repo_desc = project.get('description')

        res += f"""\t<tr>
    \t<td>{number}</td>
    \t<td><a href="{repo_url}">{repo_name}</a></td>
    \t<td>{repo_desc}</td>
\t</tr>
"""
    return res

def fetch_projects():
    """Fetch list of projects from the GitHub API."""
    response = requests.get(API_LINK)
    return response.json() if response.status_code == 200 else []

def insert_values(readme, projects):
    # get the right position
    start_pos = readme.find(START_MARKER) + len(START_MARKER) + 1
    end_pos = readme.find(END_MARKER)
    injection = parse_project_injection(projects)

    readme = readme[:start_pos] + injection + readme[end_pos:]
    
if __name__ == '__main__':
    main()