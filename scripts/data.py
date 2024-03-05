import codecs
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

URL = 'https://graphql.anilist.co'

class Injections:

    def __init__(self, status):
        self.status = status

    def fetch_watching(self):
    """
    Read the anilist.co API and returns the results

    return: The values outputted by the anime api 
    """
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
    """
    extract the data from the JSON file from the api.

    return: an Array filled with dictionarys with all values inside

    values: current_progress, score, media_id, name (in english and romaji)
    """
        animes = []

        for lists in self.fetch_watching().get('MediaListCollection').get('lists'):
            for entry in lists.get('entries'):
                dictionary = {}

                if self.status == "CURRENT":
                    current_progess = entry.get('progress')
                    dictionary["current_progress"] = current_progess
                elif self.status == "COMPLETED":
                    score = entry.get("score")
                    dictionary["score"] = score

                media_id = entry.get('mediaId')
                dictionary["media_id"] = media_id

                english_title = entry.get('media').get('title').get('english')
                dictionary["name"] = english_title

                if english_title == None:
                    romaji_title = entry.get('media').get('title').get('romaji')
                    dictionary["name"] = romaji_title

                animes.append(dictionary)

        return animes

    def print_string(self):
    """
    Creates a string from the given anime values.

    return: Output string with a link to the anime, and the score / current_progrss
    """
        titles = self.get_animes()
        all_stings = ""
        
        # ✅ TODO: Check for the status
        if self.status == "CURRENT":
        # ✅ TODO: if status = CURRENT -> print short titles
            for title in range(len(titles)):
                anime = titles[title]
                string = f'''- **[{anime["name"]}](https://anilist.co/anime/{anime["media_id"]})** episode **{anime["current_progress"]}**\n'''
                all_stings += string
        
        # ✅ TODO: if status = COMPLETED -> print titles
        # TODO: Try to sort these strings, by the score
        elif self.status == "COMPLETED":
            for title in range(len(titles)):
                anime = titles[title]
                string = f'''- **[{anime["name"]}](https://anilist.co/anime/{anime["media_id"]})** With a score of **{anime["score"]}**\n'''
                all_stings += string

        return all_stings                