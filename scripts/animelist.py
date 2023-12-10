from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport


URL = 'https://graphql.anilist.co'
START_MARKER = '<!-- CURRENTLY START -->'
END_MARKER = '<!-- CURRENTLY END -->'

def fetch_watching():
    transport = AIOHTTPTransport(url=URL)

    client = Client(transport=transport)
    
    query = gql(
        '''query Test ($name: String) {
        MediaListCollection (userName: $name, type:ANIME, status: CURRENT){
            lists {
                entries {
                    mediaId
                    progress
                    media {
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
        'name': "CrimsonshadeTV"
    }

    result = client.execute(query, variables)
    return result

def main():
    readme = ''

    watchlist = fetch_watching()
    
    with open('README.md', 'r') as file:
        readme = file.read()

    start_pos = readme.find(START_MARKER) + len(START_MARKER) + 1
    end_pos = readme.find(END_MARKER)
    injection = parse_injection(watchlist)

    readme = readme[:start_pos] + injection + readme[end_pos:]

    with open("README.md", 'w') as file:
        file.write(readme)

def parse_injection(content):
    titles = ''
    for lists in content.get('MediaListCollection').get('lists'):
        for entry in lists.get('entries'):
            media_id = entry.get('mediaId')
            current_progess = entry.get('progress')
            english_title = entry.get('media').get('title').get('english')
            titles += f'''- **[{english_title}](https://anilist.co/anime/{media_id})** episode **{current_progess}**\n'''
    
    return titles

if __name__ == '__main__':
    main()