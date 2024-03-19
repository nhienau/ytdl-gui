from datetime import datetime

def to_duration_string(seconds):
    if seconds is None:
        return ""

    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        duration = f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        duration = f"{minutes:02}:{seconds:02}"

    return duration

def to_date_string(date_string):
    date = datetime.strptime(date_string, "%Y%m%d")
    return date.strftime("%b %d, %Y")
