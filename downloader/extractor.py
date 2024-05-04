import yt_dlp
from helper.custom_exception import ExtractionStoppedException

class Logger:
    def __init__(self, stop_event):
        self.stop_event = stop_event

    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        if self.stop_event.is_set():
            raise ExtractionStoppedException("Extraction stopped by user")

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


def extract(url, cookies_from_browser, stop_event):
    ydl_opts = {
        "extract_flat": True,
        "logger": Logger(stop_event),
    }
    if cookies_from_browser != "":
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser, )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        result = ydl.sanitize_info(info)
    return result

