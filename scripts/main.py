import codecs
from anime_list import AnimeList


CURRENTLY_START_MARKER = '<!-- CURRENTLY START -->'
CURRENTLY_END_MARKER = '<!-- CURRENTLY END -->'

COMPLETED_START_MARKER = '<!-- COMPLETED START -->'
COMPLETED_END_MARKER = '<!-- COMPLETED END -->'

FAVOURITE_START_MARKER = '<!-- FAVOURITES START -->'
FAVOURITE_END_MARKER = '<!-- FAVOURITES END -->'

current = AnimeList("CURRENT")
completed = AnimeList("COMPLETED")
favourite = AnimeList("FAVOURITES")

def main(start_marker, end_marker):
    readme = ''

    with codecs.open('README.md', 'r', "utf-8") as file:
        readme = file.read()

    injection = ''
    if (start_marker == CURRENTLY_START_MARKER):
        injection = current.print_string()
    elif (start_marker == COMPLETED_START_MARKER):
        injection = completed.print_string()
    elif (start_marker == FAVOURITE_START_MARKER):
        injection = favourite.print_string()

    start_pos = readme.find(start_marker) + len(start_marker) + 1
    end_pos = readme.find(end_marker)
        
    readme = readme[:start_pos] + injection + readme[end_pos:]

    with codecs.open("README.md", 'w', "utf-8") as file:
        file.write(readme)

if __name__ == '__main__':
    main(CURRENTLY_START_MARKER, CURRENTLY_END_MARKER)
    main(COMPLETED_START_MARKER, COMPLETED_END_MARKER)
    main(FAVOURITE_START_MARKER, FAVOURITE_END_MARKER)