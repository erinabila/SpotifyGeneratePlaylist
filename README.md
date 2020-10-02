# SpotifyGeneratePlaylist
 
This is a Spotify generator playlist! 

When a user is watching a Youtube account,
- If a user likes a video, it sets automatically to your Spotify account as a "Youtube Liked Playlist"
- If a user saves a video to on of their [yt-playlist-name] Youtube playlist, will be saved as [yt-playlist-name] in their Spotify account.

Instudction:

1) Install All Dependencies
   pip3 install -r requirements.txt

2) Collect You Spotify User ID and Oauth Token From Spotfiy and add it to secrets.py file

3) To Collect your User ID, Log into Spotify then go here: Account Overview and its your Username alt text
To Collect your Oauth Token, Visit this url here: https://developer.spotify.com/console/post-playlists/ Get Oauth and click the Get Token button alt text
Enable Oauth For Youtube and download the client_secrets.json

4) Run the File
python3 create_playlist.py

Technologies: 
- Youtube Data API v3 - https://developers.google.com/youtube/v3
- Spotify Web API - https://developer.spotify.com/documentation/web-api/
- Requests Library v 2.22.0 - https://requests.readthedocs.io/en/master/
- Youtube_dl v 2020.01.24 (allows you to download videos from Youtube) - https://github.com/ytdl-org/youtube-dl/
