import sys
import json
import requests
from urllib.parse import urlsplit, urlunsplit
import subprocess

def download_video(url, video_id, output):
    scheme, netloc, path, query, fragment = urlsplit(url)
    path_parts = path.split('/')
    path_parts[3] = 'parcel'
    path_parts[4] = f'video/{video_id}.mp4'
    new_path = '/'.join(path_parts[0:5])
    download_url = urlunsplit((scheme, netloc, new_path, '', ''))
    print(download_url)

    response = requests.get(download_url, stream=True)

    with open(f"{output}.mp4", "wb") as video_file:
        for chunk in response.iter_content(chunk_size=8192):
            video_file.write(chunk)

    print(f"Video {video_id}.mp4 -> {output}.mp4 descargado exitosamente.")

def download_audio(url, audio_id, output):
    scheme, netloc, path, query, fragment = urlsplit(url)
    path_parts = path.split('/')
    path_parts[3] = 'parcel'
    path_parts[4] = f'audio/{audio_id}.mp4'
    new_path = '/'.join(path_parts[0:5])
    download_url = urlunsplit((scheme, netloc, new_path, '', ''))
    print(download_url)
    response = requests.get(download_url, stream=True)
    with open(f"{output}-audio.mp4", "wb") as video_file:
        for chunk in response.iter_content(chunk_size=8192):
            video_file.write(chunk)

    print(f"Audio {audio_id}.mp4 -> {output}.mp4 descargado exitosamente.")

def main(url, output):
    response = requests.get(url)
    data = json.loads(response.text)
    video_id = data['video'][0]['id']
    audio_id = data['audio'][0]['id']
    download_video(url, video_id, output)
    download_audio(url, audio_id, output) # only needed in some cases
    command = ['C:/Users/Oscar/Downloads/ffmpeg-2024-05-08-git-e8e84dc325-full_build/bin/ffmpeg.exe', '-i', f'{output}.mp4', '-i', f'{output}-audio.mp4', '-c:v', 'copy', '-c:a', 'copy', f'{output}-mixed.mp4']
    subprocess.run(command)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python3 main.py <URL>, <output>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])
