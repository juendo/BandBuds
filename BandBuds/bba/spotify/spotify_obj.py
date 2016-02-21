import sys
import spotipy
import spotipy.util as util


scope = 'user-library-read'

if len(sys.argv) >1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.promtpt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks()
    for item in results['items']:
        track = item['track']
        print track['name'] + ' - ' + track['artist'][0]['name']
else:
    print "Can't get token", username