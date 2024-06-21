import requests
import argparse
from datetime import datetime

API_URL = 'https://musicbrainz.org/ws/2/'
USER_AGENT = 'album_search_tool/1.0 ( gmwarzecha@tutanota.com )'

def format_release_date(date_str):
  try:
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%Y")
  except ValueError:
    return date_str


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
      albums = []
      for release in releases:
        title = release['title']
        release_date_str = release['first-release-date']
        release_date = format_release_date(release_date_str)
        if release_date:
          albums.append((title, release_date))

      albums.sort(key=lambda x: x[1])

      print("\nReleases:\n") 
      for title, release_date in albums:
        print(f"- {title} {release_date}\n")
        
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