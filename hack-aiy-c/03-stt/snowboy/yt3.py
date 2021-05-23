#!/usr/bin/python3

import vlc
import youtube_dl
import time
import sys

ydl_opts = {
    'default_search': 'ytsearch1:',
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True
}


def play_music(name):
    
    while True:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                meta = ydl.extract_info(name, download=False)
                break
            except Exception as error: 
                print(error)
                time.sleep(0.01)
                pass

    if meta:
        info = meta['entries'][0]
        playurl = info['url']
        print(playurl)
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()

        try:
            while True:
                time.sleep(1)
        except:
            player.pause()


if __name__ == "__main__":
    name = sys.argv[1]
    play_music(name)



