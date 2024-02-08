import requests
import json
import os
from aiogram import types
from pathlib import Path
from dotenv import load_dotenv
from main import bot


load_dotenv()
API_KEY_ID = os.getenv("API_KEY_ID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
LANG = "ru"
RESULT_TYPE = 1
headers = {"keyId": API_KEY_ID, "keySecret": API_KEY_SECRET}


def create(file_path):
    files = {}
    create_url = "https://api.speechflow.io/asr/file/v1/create"
    create_url += "?lang=" + LANG
    files['file'] = open(file_path, "rb")
    response = requests.post(create_url, headers=headers, files=files)
    if response.status_code == 200:
        create_result = response.json()
        if create_result["code"] == 10000:
            task_id = create_result["taskId"]
        else:
            task_id = ""
    else:
        task_id = ""
    return task_id


def query(task_id):
    query_url = "https://api.speechflow.io/asr/file/v1/query?taskId=" + \
        task_id + "&resultType=" + str(RESULT_TYPE)
    while (True):
        response = requests.get(query_url, headers=headers)
        if response.status_code == 200:
            query_result = response.json()
            if query_result["code"] == 11000:
                return query_result
                break
            elif query_result["code"] == 11001:
                continue
        else:
            print('query request failed: ', response.status_code)


def translated_voice_to_text(file_path):
    task_id = create(file_path=file_path)
    if (task_id != ""):
        json_res = query(task_id)
        result_json = json.loads(json_res['result'])
        transcribed_text = " ".join([sentence['s']
                                    for sentence in result_json['sentences']])
        return transcribed_text
    return "Текст не распознан"


async def handle_file(file: types.File, file_name: str, path: str):
    destination_folder = Path(path)
    destination_folder.mkdir(parents=True, exist_ok=True)
    full_path = destination_folder / file_name
    await bot.download_file(file_path=file.file_path, destination=str(full_path))
    return str(full_path)
