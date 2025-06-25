# spotify-ad-killer

I made this because I kept seeing a ton of over-complicated versions of these, so I made my own in under a hundred lines. This script automatically detects when a Spotify ad is playing and restarts Spotify to skip it.

## How does it work?
It checks the Spotify window title. If the title doesn’t have a dash (-), it means Spotify is either not playing a song (title shows "Spotify Free") or it’s playing an ad. When that happens, the script restarts Spotify and skips to the next track, so you don't replay the same song.

## Notes:
Only works on windows 10/11 (haven't tested on windows 10)
This interrupts your screen for like 3 seconds so add some window names in exceptions for apps that you don't wanna be interrupted on (won't do anything when that app is in foreground)
This was made for my own pc so it might not work if your device is slower (spotify may take too long to restart)
