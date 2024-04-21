import json
import sqlite3

from helper.get_download_folder import get_download_folder

DATABASE = "preset/preset.db"
DEFAULT_PRESET_FILE_NAME = "preset/default_presets.json"

def convert_data_tuples_to_dictionaries(lst):
    keys = ['id', 'name', 'include_video', 'include_audio', 'split_video_and_audio', 'split_by_chapters', 'resolution', 'max_file_size', 'subtitle', 'thumbnail', 'sponsorblock', 'output_path', 'editable']
    boolean_keys = ('include_video', 'include_audio', 'split_video_and_audio', 'split_by_chapters', 'subtitle', 'thumbnail', 'sponsorblock', 'editable')
    result = [{keys[i]: bool(el[i]) if keys[i] in boolean_keys else el[i] for i in range(len(keys))} for el in lst]
    return result

def get_all():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preset")
    result = cursor.fetchall()
    connection.close()
    return convert_data_tuples_to_dictionaries(result)

def insert(preset):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    with connection:
        cursor.execute("INSERT INTO preset (name, include_video, include_audio, split_video_and_audio, split_by_chapters, resolution, max_file_size, subtitle, thumbnail, sponsorblock, output_path, editable) VALUES (:name, :include_video, :include_audio, :split_video_and_audio, :split_by_chapters, :resolution, :max_file_size, :subtitle, :thumbnail, :sponsorblock, :output_path, :editable)", preset)
    connection.close()

def update(preset):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    with connection:
        cursor.execute("UPDATE preset SET name = :name, include_video = :include_video, include_audio = :include_audio, split_video_and_audio = :split_video_and_audio, split_by_chapters = :split_by_chapters, resolution = :resolution, max_file_size = :max_file_size, subtitle = :subtitle, thumbnail = :thumbnail, sponsorblock = :sponsorblock, output_path = :output_path, editable = :editable WHERE id = :id", preset)
    connection.close()

def delete(preset_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    with connection:
        cursor.execute("DELETE from preset WHERE id = :id", {"id": preset_id})
    connection.close()

def setup():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS preset(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                include_video INTEGER NOT NULL,
                include_audio INTEGER NOT NULL,
                split_video_and_audio INTEGER NOT NULL,
                split_by_chapters INTEGER NOT NULL,
                resolution TEXT,
                max_file_size REAL,
                subtitle INTEGER NOT NULL,
                thumbnail INTEGER NOT NULL,
                sponsorblock INTEGER NOT NULL,
                output_path TEXT,
                editable INTEGER NOT NULL
            )""")
    
    presets = get_all()
    if len(presets) == 0:
        download_folder = get_download_folder()
        with open(DEFAULT_PRESET_FILE_NAME, "r") as f:
            default_presets = json.load(f)
        for preset in default_presets:
            preset["output_path"] = download_folder
            insert(preset)
        
    connection.close()
