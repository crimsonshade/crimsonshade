from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

URL = 'https://graphql.anilist.co'

class AnilistQuery:
    def __init__(self, status) -> None:
        self.status = status

    def fetch_favourites(self):
        transport = AIOHTTPTransport(url=URL)

        client = Client(transport=transport)
        
        query = gql(
            '''query Favourites ($name: String) {
            User (name: $name) {
                favourites {
                    anime {
                        nodes {
                            id
                            title {
                                english
                                romaji
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
            'status': self.status
        }
    
        result = client.execute(query, variables)
        return result

    def fetch_watching(self):
        transport = AIOHTTPTransport(url=URL)

        client = Client(transport=transport)
        
        query = gql(
            '''query CurrentlyWatching ($name: String, $status: MediaListStatus) {
            MediaListCollection (userName: $name, type:ANIME, status: $status){
                lists {
                    entries {
                        mediaId
                        progress
                        score
                        repeat
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
            'status': self.status
        }
    
        result = client.execute(query, variables)
        return result