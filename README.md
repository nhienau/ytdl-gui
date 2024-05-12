# ytdl-gui

## A GUI wrapper for yt-dlp

## Features

- Extract URL (video, playlist, channel). Best compatible with Facebook, YouTube URL
- Extract private video using browser cookies
- Set download options for URL
- Save download options as a preset
- Download URLs one by one

## Libraries

- [yt-dlp](https://github.com/yt-dlp/yt-dlp): a command-line downloader
- [CustomTkinter](https://customtkinter.tomschimansky.com/): a UI library for building desktop application in Python
- [tksheet](https://github.com/ragardner/tksheet): a tkinter widget for displaying tabular data

## Installation

1. Install Python (version >= 3.10.12)

2. Clone the repository

```BASH
git clone https://github.com/nhienau/ytdl-gui
```

3. Go to the project directory & activate the virtual enviroment

```
cd ytdl-gui
```

For Windows:

```BASH
.venv\Scripts\activate.bat
```

For Linux/macOS:

```BASH
source .venv/bin/activate
```

4. Install packages

```BASH
pip install -r requirements.txt
```

5. Run application

```BASH
python3 main.py
```

## Screenshots

### Main GUI

![main gui](https://imgur.com/GrQCAfw)

### Extract video URL

![extract video](https://imgur.com/XTaO2B6)

### Extract playlist

![extract playlist](https://imgur.com/5m3MGnv)

### Options, preset

![preset](https://imgur.com/5QBYymb)

### Downloading

![downloading](https://imgur.com/pJaD5Eg)
