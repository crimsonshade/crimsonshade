from datetime import datetime
import re

def get_pattern_matches(content):
    pattern = re.compile(r'(<!--\s*age:(\d{4})-(\d{1,2})-(\d{1,2})\s*-->)(?:\s*(\d+))?')
    matches = pattern.finditer(content)
    
    return matches

def get_birthday(match):
    year, month, day = map(int, (match.group(2), match.group(3), match.group(4)))
    birthdate = datetime(year, month, day)
    return birthdate

def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def main(content):
    for match in get_pattern_matches(content):
        birthdate = get_birthday(match)
        age = calculate_age(birthdate)
        
        existing_age = match.group(4)
        if existing_age:
            start_index = match.end() - len(existing_age)
            end_index = match.end()
            
            age_insertion = f"{age}"
            content = content[:start_index] + age_insertion + content[end_index:]
        else:
            age_insertion = f" {age}"
            content = content[:match.end()] + age_insertion + content[match.end():]
        break
        
    return content

if __name__ == '__main__':
    with open('README.md', 'r') as file:
        readme_contents = file.read()
    
    updated_content = main(readme_contents)

    with open('README.md', 'w') as file:
        file.write(updated_content)