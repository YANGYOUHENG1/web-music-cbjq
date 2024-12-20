import os
import json
from mutagen.mp3 import MP3


def get_mp3_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.mp3')]


def get_png_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.png')]


def get_file_duration(file_path):
    audio = MP3(file_path)
    duration = int(audio.info.length)
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes}:{seconds:02d}"


def sort_files(mp3_files):
    def sort_key(file):
        name = os.path.splitext(file)[0]
        if 'OST' in name:
            return (1, name)
        elif 'ASMR' in name:
            return (2, name)
        elif '1.1' in name:
            return (3, name)
        elif any(f'1.{i}' in name for i in range(2, 10)):
            return (4, name)
        elif any(f'2.{i}' in name for i in range(1, 4)):
            return (5, name)
        else:
            return (6, name)

    return sorted(mp3_files, key=sort_key)


def create_music_json(mp3_dir, png_dir, output_file):
    mp3_files = get_mp3_files(mp3_dir)
    png_files = get_png_files(png_dir)

    sorted_mp3_files = sort_files(mp3_files)

    music_data = []

    for mp3_file in sorted_mp3_files:
        mp3_name = os.path.splitext(mp3_file)[0]
        for png_file in png_files:
            png_name = os.path.splitext(png_file)[0]
            if mp3_name in png_name or png_name in mp3_name:
                music_data.append({
                    "name": mp3_name,
                    "audio_url": f"./music/{mp3_file}",
                    "singer": "尘白禁区",
                    "album": "西山居",
                    "cover": f"./picture/{png_file}",
                    "time": get_file_duration(os.path.join(mp3_dir, mp3_file))
                })
                break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(music_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    create_music_json('./music', './picture', './music.json')
