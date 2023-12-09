from python.birthday import Birthday
from python.api import GitHubAPI

birthday = Birthday()
api_call = GitHubAPI('README.md')

def main():
    api_call.create_table()

    # Think about another way of doing this, because saving the holer readme is a huge act and a waste of resources
    with open('README.md', 'r') as file:
        readme_contents = file.read()
        
    updated_content = birthday.append_age_after_comment(readme_contents)

    with open('README.md', 'w') as file:
        file.write(updated_content)
    
if __name__ == '__main__':
    main()