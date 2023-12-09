from datetime import datetime
import re

class Birthday:
    def __init__(self) -> None:
        pass
    
    def get_pattern_matches(self, content):
        """Tries to find a specific pattern inside the found content

        Args:
            content (list): All lines read of the imported file

        Returns:
            list: A list of all matches, where the pattern fits
        """
        
        pattern = re.compile(r'(<!--\s*age:(\d{4})-(\d{1,2})-(\d{1,2})\s*-->)(?:\s*(\d+))?')
        matches = pattern.finditer(content)
        
        return matches
    
    def get_birthday(self, match):
        """Extracts my birthdate out of the birthday comment inside the README file.

        Args:
            match (list): The correct values of my birthday found inside the comment

        Returns:
            int: My birthdate as a datetime
        """
        
        year, month, day = map(int, (match.group(2), match.group(3), match.group(4)))
        birthdate = datetime(year, month, day)
        return birthdate

    def calculate_age(self, birthdate):
        """Calculates my current age by using the datetime package

        Args:
            birthdate (datetime): the date of my birth.

        Returns:
            int: My age
        """
        
        today = datetime.now()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    
    def append_age_after_comment(self, content):
        for match in self.get_pattern_matches(content):
            birthdate = self.get_birthday(match)
            age = self.calculate_age(birthdate)
            
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