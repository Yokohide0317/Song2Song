import argparse
import youtube_dl
import random
import os

# count分のアルファベットでランダムな文字列を生成するだけ。
def generate_id():
    count = 10
    return ''.join([chr(random.randint(97, 122)) for _ in range(count)])

# csv内をreadlines()で読んだlist形式から、曲ごとに分ける。
# [[曲名1, url1, url2, ...], [曲名2, url1, url2, ...]...]
def parse_by_song(_lines):

    # 既に保存されている曲名なら、Trueを返す。
    def is_new_song(_line):
        # csvで、0列目に曲名が書いてある行はoriginal曲として扱う。
        if len(_line[0].strip()) > 1:
            return True
        else:
            return False

    all_songs = []
    # 一番最初は入れておく。
    by_song = [_lines[0][0].strip(), _lines[0][1].strip()]

    # 2行目からスライスする。
    for line in _lines[1:]:
        url = line[1].strip()

        if is_new_song(line) and len(by_song) > 1:
            all_songs.append(by_song)

            # song_name, url(original-song)
            by_song = [line[0].strip(), url]
        else:
            by_song.append(url)

    if len(by_song) > 1:
        all_songs.append(by_song)

    return all_songs


def download_main(_file, _outdir):

    with open(_file, "r") as f:
        lines = f.readlines()

    lines = [l.split(",    ") for l in lines]

    all_songs = parse_by_song(lines)
    print(all_songs)

    for song in all_songs:
        for i, url in enumerate(song):
            # 一番最初は曲名。保存用Dirを作成し、終了。
            if i == 0:
                downloader = Downloader(_song_name=url, out_path=_outdir)
                # 既に存在していたらこの曲はスキップ
                if downloader.is_downloaded():
                    break
                else:
                    continue

            # 2番目以降はURLなので、ダウンロード。
            # 2番目はoriginalとして名前を指定する。
            elif i == 1:
                save_name = "original"
            # 以降はランダムなIDを作成。
            else:
                save_name = str(generate_id)

            downloader.download_by_url(_url=url, _save_name=save_name)
    return

class Downloader:
    def __init__(self, _song_name: str, out_path: str):
        # 空白はめんどくさいので、アンダーバーへ置換。
        self.song_name = _song_name.replace(" ", "_")
        self.output_dir = os.path.join(out_path, _song_name)
        return None

    def is_downloaded(self):
        if os.path.exists(self.output_dir):
            return True
        else:
            os.makedirs(self.output_dir)
            return False

    # URLと保存名を指定して、mp3をダウンロード。
    # {outdir}/{曲名}/{save_name}.mp3 になる。
    def download_by_url(self, _url, _save_name):
        save_path = os.path.join(self.output_dir, _save_name)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl':  f"{save_path}" + '.%(ext)s',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'},
                #{'key': 'FFmpegMetadata'},
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([_url])
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("outdir", default="./")

    args = parser.parse_args()

    download_main(args.file, args.outdir)
