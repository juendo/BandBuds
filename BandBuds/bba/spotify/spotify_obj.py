import spotipy
export SPOTIPY_CLIENT_ID=''
export SPOTIPY_SECRET=''
export SPOTIPY_REDIRECT_URI=''

spotify = spotipy.Spotify()
results = spotify.search(q='artist' + name, type='artist')
print results