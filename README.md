# spotify-ad-killer

I made this because I kept seeing a ton of over-complicated versions of these so I made my own in under a hundred lines. This script automatically detects when a Spotify ad is playing and restarts Spotify to skip it.

##How does it work?
This script just checks if the window name has a dash in it. If it doesn't, it's either not playing a song (window will be titled Spotify Free), or it's playing and ad. Then it restarts spotify and skips to the next song so it doesn't replay the same song.

##Notes:
Only works on windows 10/11 (haven't tested on windows 10)
This interrupts your screen for like 3 seconds so add some window names in exceptions for apps that you don't wanna be interrupted on (won't do anything when that app is in foreground)
