import os

import ujson
import fake_useragent
import requests

from src.jad import JarDecompile


class Client:
    def __init__(self) -> None:
        self.user_agent = fake_useragent.UserAgent().random

    def look_for_modlist(self, path: str) -> list:
        mod_list = next(os.walk(path))[2]
        del mod_list[0]
        if len(mod_list) == 0:
            return False
        else:
            JarDecompile.look_for_jar(path)
            return mod_list

    def load_file_for_translate(self, path: str) -> dict:
        with open(path) as file:
            j = ujson.load(file)
            return j

    def translate_request(self, api_key: str, from_: str, to_: str, loaded_json: dict) -> dict:
        for key, val in loaded_json.items():
            url = "https://microsoft-translator-text.p.rapidapi.com/translate"
            querystring = {
                "from": from_,
                "to": to_,
                "api-version": "3.0",
                "profanityAction": "NoAction",
			    "textType": "plain"
            }
            payload = [{"Text": val}]
            headers = {
                "x-rapidapi-key": api_key,
                "x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
                "Content-Type": "application/json",
			    "user-agent": self.user_agent
            }
            response = requests.post(url, json=payload, headers=headers, params=querystring)
            loaded_json[key] = response.json()[0]['translations'][0]['text']
        return loaded_json

    def dump_translated_file(self, path: str, dictionary: dict):
        with (path / 'ru_ru.json').open('x', encoding='utf-8') as f:
            ujson.dump(dictionary, f, ensure_ascii=False)

    def change_extension(self, path: str):
        try:
            path.rename(path.with_suffix('.jar'))
        except FileExistsError:
            return None