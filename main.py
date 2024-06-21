import requests
import argparse

API_URL = 'https://musicbrainz.org/ws/2/'
USER_AGENT = 'album_search_tool/1.0 ( gmwarzecha@tutanota.com )'

def get_artist_id(artist_name):
  params = {
    'query': artist_name, 
    'fmt': 'json',
  }

  headers = {
    'User-Agent': USER_AGENT,
  }

  response = requests.get(f"{API_URL}artist/", params=params, headers=headers)

  if response.status_code == 200:
    data = response.json()
    artists = data.get('artists', [])

    if artists:
      return artists[0]['id']
    else: 
      print(f"No artist found for {artist_name}")
      return None
    
  else:
    print("Failed to fetch artist data from the API")
    return None
  
def get_artist_albums(artist_id):
  params = {
    'fmt': 'json',
  }

  headers = {
    'User-Agent': USER_AGENT,
  }

  response = requests.get(f"{API_URL}release-group?artist={artist_id}&type=album|ep", params=params, headers=headers)

  if response.status_code == 200:
    data = response.json()
    releases = data.get('release-groups', [])

    if releases:
      print("Releases:") 
      for release in releases:
        print(f"- {release['title']}\n-- {release['first-release-date']}\n")
        
    else:
      print("No albums found for this artist")
  
  else:
    print("Failed to fetch release data from the API")

def main():
  parser = argparse.ArgumentParser(description="Get all releases of an artist or band")
  parser.add_argument('artist', type=str, help="Name of the artist or band")

  args = parser.parse_args()
  artist_name = args.artist

  artist_id = get_artist_id(artist_name)
  if artist_id:
    get_artist_albums(artist_id)

if __name__ == "__main__":
  main()