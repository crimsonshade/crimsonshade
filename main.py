from datetime import datetime
import re

# Function to calculate age
def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Read the README file as a single string
with open('README.md', 'r') as file:
    readme_contents = file.read()

# Regular expression pattern to find the age comment and capture the date
pattern = re.compile(r'(<!--\s*age:(\d{4})-(\d{1,2})-(\d{1,2})\s*-->)')

# Find all matches
matches = pattern.finditer(readme_contents)

# For each match, calculate age and append it after the comment
for match in matches:
    # Extract birthdate from the captured groups and convert to integers
    year, month, day = map(int, (match.group(2), match.group(3), match.group(4)))
    birthdate = datetime(year, month, day)
    age = calculate_age(birthdate)

    # Append age right after the closing comment tag
    age_insertion = f" {age} "
    readme_contents = readme_contents[:match.end()] + age_insertion + readme_contents[match.end():]
    break  # Assuming only one such comment exists; remove this if there are multiple

# Write back to README
with open('README.md', 'w') as file:
    file.write(readme_contents)
