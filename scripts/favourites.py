from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

URL = 'https://graphql.anilist.co'
START_MARKER = '<!-- FAVOURITES START -->'
END_MARKER = '<!-- FAVOURITES END -->'

def main():
    readme = ''
    favorites = fetch_favorites()
    with open('README.md', 'r') as file:
        readme = file.read()

    start_pos = readme.find(START_MARKER) + len(START_MARKER) + 1
    end_pos = readme.find(END_MARKER)
    injection = parse_injection(favorites)

    readme = readme[:start_pos] + injection + readme[end_pos:]

    with open('README.md', 'w') as file:
        file.write(readme)
    
def parse_injection(favourites):
    titles = ''
    for anime in favourites['User']['favourites']['anime']['nodes']:
        anime_id = anime['id']
        anime_title = anime['title'].get('english')

        titles += f'''- **[{anime_title}](https://anilist.co/anime/{anime_id})**\n'''
    return titles

def fetch_favorites():
    transport = AIOHTTPTransport(url=URL)
    client = Client(transport=transport)

    query = gql(
        '''query Favorites($name: String) {
            User (name: $name) {
                favourites {
                    anime {
                        nodes {
                            id
                            title {
                                english
                            }
                        }
                    }
                }
            }
        }
'''
    )

    variables = {
        "name": "CrimsonshadeTV"
    }

    result = client.execute(query, variables)
    return result

if __name__ == '__main__':
    main()