import os
from pathlib import Path
import traceback
import yt_dlp

from helper.custom_exception import DownloadStoppedException

class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)

    def info(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def extract_options(preset, cookies):
    # Initial options
    options = {
        "outtmpl": {
            "default": "%(title)s.%(ext)s"
        },
        "format_sort": ["ext"],
        "postprocessors": [
            {
                "key": "FFmpegConcat",
                "only_multi_video": True,
                "when": "playlist"
            },
        ]
    }

    if preset["include_video"] and not preset["include_audio"]:
        options["format"] = "bv"
    elif not preset["include_video"] and preset["include_audio"]:
        options["format"] = "ba"

    options["keepvideo"] = preset["split_video_and_audio"]

    if preset["split_by_chapters"]:
        options["postprocessors"].append(
            {
                "force_keyframes": False,
                "key": "FFmpegSplitChapters"
            }
        )
    
    if preset["resolution"] is not None:
        options["format_sort"].append(f"res:{preset['resolution'][:-1]}")

    if preset["max_file_size"] is not None:
        options["format_sort"].append(f"filesize~{preset['max_file_size']:.2f}M")

    options["writesubtitles"] = preset["subtitle"]
    options["writethumbnail"] = preset["thumbnail"]

    if preset["thumbnail"]:
        options["postprocessors"].append(
            {
                "format": "png",
                "key": "FFmpegThumbnailsConvertor",
                "when": "before_dl"
            }
        )

    options["paths"] = {
        "home": preset["output_path"]
    }

    if cookies != "":
        options["cookiesfrombrowser"] = (cookies,)

    return options

    
def cleanup_partial_files(path):
    print("Cleaning up partial files")
    directory = Path(path)
    if not directory.exists() or not directory.is_dir():
        print(f"Output path {path} is not a directory or cannot be found.")
        return
    for filename in os.listdir(directory):
        if filename.endswith((".part", ".ytdl")):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Removed file: {file_path}")


def download(stop_event, tuple_urls, callback):
    on_url_start_downloading = callback["on_url_start_downloading"]
    progress_callback = callback["progress"]
    postprocessing_callback = callback["postprocessing"]
    on_download_error = callback["on_download_error"]
    on_download_stopped = callback["on_download_stopped"]
    on_all_urls_finished = callback["on_all_urls_finished"]

    for index, entry in tuple_urls:
        url = entry.get("webpage_url") or entry.get("url")
        url_options = extract_options(entry["preset"], entry["cookies"])
        url_options.update({
            "logger": Logger(),
            "progress_hooks": [lambda d: progress_callback(d, stop_event, entry, index)],
            "postprocessor_hooks": [lambda d: postprocessing_callback(d, stop_event, entry, index)],
        })
        with yt_dlp.YoutubeDL(url_options) as ydl:
            if not stop_event.is_set():
                try:
                    on_url_start_downloading(entry, index)
                    ydl.download(url)
                except Exception as e:
                    print(e)
                    if isinstance(e, DownloadStoppedException):
                        cleanup_partial_files(entry["preset"]["output_path"])
                        on_download_stopped(entry, index)
                    else:
                        on_download_error(entry, index)
                        print(traceback.format_exc())
                    break
    if not stop_event.is_set():
        on_all_urls_finished()

