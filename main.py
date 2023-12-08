from python.birthday import Birthday

birthday = Birthday()

def append_age_after_comment(content):
    for match in birthday.get_pattern_matches(content):
        birthdate = birthday.get_birthday(match)
        age = birthday.calculate_age(birthdate)
        
        existing_age = match.group(5)
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

def main():
    # Think about another way of doing this, because saving the holer readme is a huge act and a waste of resources
    with open('README.md', 'r') as file:
        readme_contents = file.read()
        
    updated_content = append_age_after_comment(readme_contents)

    with open('README.md', 'w') as file:
        file.write(updated_content)
    
if __name__ == '__main__':
    main()