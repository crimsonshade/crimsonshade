import requests

# Define the start and end markers for the project section in the Markdown file
START_MARKER = '<!-- PROJECTS START -->'
END_MARKER = '<!-- PROJECTS END -->'

def fetch_projects():
    """Fetch list of projects from the GitHub API."""
    url = "https://api.github.com/orgs/crmsn-xyz/repos"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def insert_projects( projects_content):
    """Insert projects content into the Markdown file between defined markers."""
    with open('README.md', 'r') as file:
        content = file.read()

    # Find the positions of the start and end markers
    start_pos = content.find(START_MARKER) + len(START_MARKER)
    end_pos = content.find(END_MARKER)

    # Check if both markers are found
    if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
        # Create new content with projects inserted between markers
        new_content = content[:start_pos] + '\n' + projects_content + content[end_pos:]
        with open('README.md', 'w') as file:
            file.write(new_content)
    else:
        print("Markers not found or in wrong order.")

def get_topics(project):
    topics = project.get('topics', [])
    if not topics:
        return ""
    else:
        return ", ".join(topics)

def main():
    """Main function to fetch projects and update the Markdown file."""
    projects_content = ""
    number = 0
    for project in fetch_projects():
        number += 1
        # Append each project in HTML format to the projects_content string
        projects_content += f"""\t<tr>
    \t<td>{number}</td>
    \t<td><a href=\"{project.get('html_url')}\">{project.get('name')}</a></td>
    \t<td>{project.get('description', 'No description')}</td>
    \t<td>{get_topics(project)}</td>
\t</tr>
"""
    
    # Insert the compiled projects content into the Markdown file
    insert_projects(projects_content)
    
if __name__ == '__main__':
    main()