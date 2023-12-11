from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import codecs


URL = 'https://graphql.anilist.co'
CURRENTLY_START_MARKER = '<!-- CURRENTLY START -->'
CURRENTLY_END_MARKER = '<!-- CURRENTLY END -->'

COMPLETED_START_MARKER = '<!-- COMPLETED START -->'
COMPLETED_END_MARKER = '<!-- COMPLETED END -->'

def fetch_watching(status):
    transport = AIOHTTPTransport(url=URL)

    client = Client(transport=transport)
    
    query = gql(
        '''query CurrentlyWatching ($name: String, $status: MediaListStatus) {
        MediaListCollection (userName: $name, type:ANIME, status: $status){
            lists {
                entries {
                    mediaId
                    progress
                    media {
                        title {
                            romaji
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
        'name': "CrimsonshadeTV",
        'status': status
    }

    result = client.execute(query, variables)
    return result

def main(start_marker, end_marker):
    readme = ''

    with codecs.open('README.md', 'r', "utf-8") as file:
        readme = file.read()

        injection = ''
    if (start_marker == CURRENTLY_START_MARKER):
        watchlist = fetch_watching("CURRENT")
        injection = currently_injection(watchlist)
    elif (start_marker == COMPLETED_START_MARKER):
        watchlist = fetch_watching("COMPLETED")
        injection = watched_injection(watchlist)

    start_pos = readme.find(start_marker) + len(start_marker) + 1
    end_pos = readme.find(end_marker)
        
    readme = readme[:start_pos] + injection + readme[end_pos:]

    with codecs.open("README.md", 'w', "utf-8") as file:
        file.write(readme)

def currently_injection(content):
    titles = ''
    for lists in content.get('MediaListCollection').get('lists'):
        for entry in lists.get('entries'):
            media_id = entry.get('mediaId')
            current_progess = entry.get('progress')
            english_title = entry.get('media').get('title').get('english')
            romaji_title = entry.get('media').get('title').get('romaji')
            if english_title is None:
                titles += f'''- **[{romaji_title}](https://anilist.co/anime/{media_id})** episode **{current_progess}**\n'''
            else:
                titles += f'''- **[{english_title}](https://anilist.co/anime/{media_id})** episode **{current_progess}**\n'''
    
    print(titles)
    return titles

def watched_injection(content):
    titles = ''
    for lists in content.get('MediaListCollection').get('lists'):
        for entry in lists.get('entries'):
            media_id = entry.get('mediaId')
            english_title = entry.get('media').get('title').get('english')
            romaji_title = entry.get('media').get('title').get('romaji')
            if english_title is None:
                titles += f'''- **[{romaji_title}](https://anilist.co/anime/{media_id})**\n'''
            else:
                titles += f'''- **[{english_title}](https://anilist.co/anime/{media_id})**\n'''
    
    print(titles)
    return titles

if __name__ == '__main__':
    main(CURRENTLY_START_MARKER, CURRENTLY_END_MARKER)
    main(COMPLETED_START_MARKER, COMPLETED_END_MARKER)