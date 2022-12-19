import argparse
import youtube_dl
import random

def is_new_song(_line):
    if len(_line[0].strip()) > 1:
        return True
    else:
        return False

def generate_id():
    return ''.join([chr(random.randint(97, 122)) for _ in range(10)])


def parse_by_song(_lines):
    all_songs = []
    by_song = []
    
    for line in _lines:
        url = line[1].strip()

        if is_new_song(line) and len(by_song) > 1:
            all_songs.append(by_song)
            by_song = [url]
        else:
            by_song.append(url)

    if len(by_song) > 1:
        all_songs.append(by_song)
    
    return all_songs

def download_by_url(_url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([_url])
    return

def download_main(_file):

    with open(_file, "r") as f:
        lines = f.readlines()

    lines = [l.split(",") for l in lines]
    
    all_songs = parse_by_song(lines)
    
    for song in all_songs:
        for i, url in enumerate(song):
            if i == 0:
                pass # dirの作成
            
            download_by_url(url)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")

    args = parser.parse_args()

    download_main(args.file)
