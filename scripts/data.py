from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

URL = 'https://graphql.anilist.co'

class Injections:

    def __init__(self, status):
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
    
    def get_animes(self):
        animes = []

        print(f"============ [{self.status}] ============")
        if self.status == "COMPLETED" or self.status == "CURRENT":
            for lists in self.fetch_watching().get('MediaListCollection').get('lists'):
                for entry in lists.get('entries'):
                    dictionary = {}

                    dictionary["media_id"] = entry.get('mediaId')
                    dictionary["name"] = entry.get('media').get('title').get('english')

                    if self.status == "CURRENT":
                        dictionary["current_progress"] = entry.get('progress')
                    elif self.status == "COMPLETED":
                        dictionary["score"] = entry.get("score")

                    if dictionary["name"] == None:
                        dictionary["name"] = entry.get('media').get('title').get('romaji')

                    print(f"{dictionary["name"]}")
                    animes.append(dictionary)
        else:
            for node in self.fetch_favourites().get('User').get('favourites').get('anime').get('nodes'):
                dictionary = {}

                dictionary["media_id"] = node.get('id')
                dictionary["name"] = node.get('title').get('english')

                if dictionary["name"] == None:
                    dictionary["name"] = node.get('title').get('romaji')

                print(f"{dictionary["name"]}")
                animes.append(dictionary)
        return animes

    def print_string(self):
        titles = self.get_animes()
        top_string = ""
        all_stings = ""
        
        # ✅ TODO: Check for the status
        if self.status == "CURRENT":
            top_string = "| Anime Title | Current Episode |\n|:-------|:--------|\n"
        # ✅ TODO: if status = CURRENT -> print short titles
            for title in range(len(titles)):
                anime = titles[title]
                string = f'''| **[{anime["name"]}](https://anilist.co/anime/{anime["media_id"]})** | **{anime["current_progress"]}** |\n'''
                all_stings += string
        
        # ✅ TODO: if status = COMPLETED -> print titles
        # TODO: Try to sort these strings, by the score
        elif self.status == "COMPLETED":
            top_string = "| Anime Title | Score |\n|:-------|:--------|\n"
            for title in range(len(titles)):
                anime = titles[title]
                string = f'''| **[{anime["name"]}](https://anilist.co/anime/{anime["media_id"]})** | **{anime["score"]}** |\n'''
                all_stings += string

        else:
            for title in range(len(titles)):
                anime = titles[title]
                string = f'''- **[{anime["name"]}](https://anilist.co/anime/{anime["media_id"]})**\n'''
                all_stings += string

        return top_string + all_stings                