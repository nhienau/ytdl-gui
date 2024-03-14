import yt_dlp

class Logger:
    def debug(self, msg):
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


async def extract(url, cookies_from_browser):
    ydl_opts = {
        "extract_flat": True,
        "logger": Logger(),
    }
    if cookies_from_browser != "":
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser, )

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        result = ydl.sanitize_info(info)
    return result
