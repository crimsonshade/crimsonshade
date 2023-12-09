import requests

# Define the start and end markers for the project section in the Markdown file
start_marker = '<!-- PROJECTS START -->'
end_marker = '<!-- PROJECTS END -->'

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
    start_pos = content.find(start_marker) + len(start_marker)
    end_pos = content.find(end_marker)

    # Check if both markers are found
    if start_pos != -1 and end_pos != -1 and start_pos < end_pos:
        # Create new content with projects inserted between markers
        new_content = content[:start_pos] + '\n' + projects_content + content[end_pos:]
        with open('README.md', 'w') as file:
            file.write(new_content)
    else:
        print("Markers not found or in wrong order.")

def main():
    """Main function to fetch projects and update the Markdown file."""
    projects_content = ""
    number = 0
    for project in fetch_projects():
        number += 1
        # Append each project in HTML format to the projects_content string
        projects_content += f"<tr><td>{number}<td><a href=\"{project['html_url']}\">{project['name']}</a></td><td>{project.get('description', 'No description')}</td></tr>\n"
    
    # Insert the compiled projects content into the Markdown file
    insert_projects(projects_content)
    
if __name__ == '__main__':
    main()