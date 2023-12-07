from python.birthday import Birthday

birthday = Birthday()

def append_age_after_comment(content):
    for match in birthday.get_pattern_matches(content):
        birthdate = birthday.get_birthday(match)
        age = birthday.calculate_age(birthdate)

        age_insertion = f" {age} "
        content = content[:match.end()] + age_insertion + content[match.end():]
        break  
    
    return content
    
if __name__ == '__main__':
    # Read the README file as a single string
    with open('README.md', 'r') as file:
        readme_contents = file.read()
        
    updated_content = append_age_after_comment(readme_contents)

    with open('README.md', 'w') as file:
        file.write(updated_content)