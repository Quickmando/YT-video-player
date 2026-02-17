import os
import cv2
import numpy as np
from pytubefix import YouTube
from time import sleep

# ANSI escape code for RGB foreground color
def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

RESET = "\033[0m"

def frame_to_ascii_rgb(frame, new_width=25):
    h, w, _ = frame.shape
    aspect_ratio = h / w

    # Very compressed height
    new_height = int(aspect_ratio * new_width * 0.2)

    resized = cv2.resize(frame, (new_width, new_height))

    ascii_img = ""
    for row in resized:
        for pixel in row:
            r, g, b = pixel
            ascii_img += rgb(r, g, b) + "▀"
        ascii_img += RESET + "\n"

    return ascii_img

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def download_youtube_video(url, filename="video.mp4"):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(filename=filename)
    return filename

def play_ascii_video(video_path, width=300, fps=30):
    cap = cv2.VideoCapture(video_path)
    delay = 1.0 / fps

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii_rgb(frame, new_width=width)
        clear_terminal()
        print(ascii_frame)
        sleep(delay)

    cap.release()

if __name__ == "__main__":
    youtube_url = input('Insert Youtube URL: ')

    print("Downloading video...")
    video_file = download_youtube_video(youtube_url, "yt_video.mp4")

    print("Playing ULTRA‑HIGH‑RES RGB ASCII video...")
    play_ascii_video(video_file, width=240, fps=60)
