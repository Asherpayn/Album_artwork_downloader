# Album_artwork_downloader
A program that allows you to download album artwork from spotify, usefull for adding artwork to mp3 files or albums on ipods.

**my attempt at "vibe coding"**
I created this as i needed to get album artork for my ipod. Itunes does have a similar function but i only have a windows xp laptop that isnt supported by apple. So it *also* barely works.  

# Before you start
you will need to install python the following python packages:
- `spotipy` for interacting with the spotify api
- `requests` for making http requests
- `os` for interacting with the operating system

- you might need more so check the python file for what it uses

you will need to have a spotify account for this
go to the [Spotify developer dashboard](https://developer.spotify.com/dashboard).
Once logged in, click the "Create an App" button.
Fill in the required details:
App Name: Choose a name for this application (e.g., "Album Artwork Downloader")
Redirect URI: Enter a redirect URI (e.g., http://localhost:8080/callback). This is required for OAuth authentication but can be a placeholder for now.
Click "Create" to create the application.

after creating the app you will be redirected to the apps dashboard.
you will see the 
Client ID: A unique identifier for your app
Client Secret: A secret key used to authenticate your app with the Spotify API.
