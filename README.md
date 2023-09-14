# Spotify Playlist Generator

Spotify Playlist Generator is a tool that allows you to automatically create and manage Spotify playlists based on your liked YouTube vidoes and custom YouTube playlists.

## Features

* Automatically adds liked YouTube vidoes to a Spotify playlists named "YouTube Liked Playlist."
* Allows you ti save YouTube videos to custo Spotify playlists with names matching your YouTube playlists.

### Instructions

1. ### Install Dependencies

Before you begin, make sure to install all the required dependencies by running the following command:

```bash
pip3 install -r requirements.txt
```

2. ### Obtain Spotify User ID and OAuth Token

To interact with Spotify API, you need to obtain your Spotify User ID and an OAuth Token. Here's how:

* **User ID: ** Log in Spotify and go to your [Account Overview](https://www.spotify.com/account/overview). Your User ID is your Spotify username.
* **OAuth Token: ** Visit the following URL yo get your OAuth Token: [Spotify OAuth Token Generator](https://developer.spotify.com/console/post-playlists/). Click the "Get Token" button to generate your token.
* Enable OAuth For Youtube and download the `client_secrets.json`.

3. ### Run the Application

Run the `create_playlist.py` script to start using the Spotify Playlist Generator:

```bash
python3 create_playlist.py
```

The script will automatically add liked YouTube videos to Spotify playlist named "YouTube Liked Playlist" and match custom YouTube playlists to Spotify playlists based on thier names.


## Technologies Used 

- [Youtube Data API v3](https://developers.google.com/youtube/v3)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Requests Library v 2.22.0](https://requests.readthedocs.io/en/master/)
- [Youtube_dl v 2020.01.24](https://github.com/ytdl-org/youtube-dl/) (allows you to download videos from Youtube)
