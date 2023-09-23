import json
import os
import logging
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

# Define constants for API scopes and URLs
YOUTUBE_API_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"

# Define logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Move API credentials to environment variables
SPOTIFY_TOKEN = os.environ.get("SPOTIFY_TOKEN")
SPOTIFY_USER_ID = os.environ.get("SPOTIFY_USER_ID")

class CreatePlaylist:
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        scopes = [YOUTUBE_API_SCOPE]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_videos(self):
        """Grab Our Liked Videos & Create A Dictionary Of Important Song Information"""
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        # collect each video and get important information
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(
                item["id"])

            # use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(
                youtube_url, download=False)
            song_name = video.get("track")
            artist = video.get("artist")

            if song_name is not None and artist is not None:
                # save all important info and skip any missing song and artist
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # add the uri, easy to get song to put into playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)

                }

    def create_playlist(self):
        """Create A New Playlist"""
        request_body = json.dumps({
            "name": "Youtube Liked Vids",
            "description": "All Liked Youtube Videos",
            "public": True
        })

        query = f"{SPOTIFY_API_BASE_URL}/users/{SPOTIFY_USER_ID}/playlists"
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_TOKEN}"
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    def get_spotify_uri(self, song_name, artist):
        """Search For the Song"""
        query = f"{SPOTIFY_API_BASE_URL}/search?query=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=20"
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_TOKEN}"
            }
        )
        response_json = response.json()
        songs = response_json.get("tracks", {}).get("items", [])

        if songs:
            # only use the first song
            uri = songs[0]["uri"]
            return uri
        else:
            logger.warning(f"No Spotify track found for '{song_name}' by '{artist}'")
            return None

    def add_song_to_playlist(self):
        """Add all liked songs into a new Spotify playlist"""
        # populate dictionary with our liked songs
        self.get_liked_videos()

        # collect all of uri
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        # create a new playlist
        playlist_id = self.create_playlist()

        if not playlist_id:
            logger.error("Failed to create a Spotify playlist. Aborting.")
            return

        # add all songs into the new playlist
        request_data = json.dumps(uris)

        query = f"{SPOTIFY_API_BASE_URL}/playlists/{playlist_id}/tracks"

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {SPOTIFY_TOKEN}"
            }
        )

        # check for valid response status
        if response.status_code != 200:
            logger.error(f"Failed to add songs to Spotify playlist. Status code: {response.status_code}")
        else:
            logger.info("Songs added to the Spotify playlist successfully.")

if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_song_to_playlist()
