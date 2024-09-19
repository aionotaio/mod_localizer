import os
import asyncio

import aiofiles
import ujson
import fake_useragent
import aiohttp

from src.jad import JarDecompile


class Client:
    def __init__(self) -> None:
        self.user_agent = fake_useragent.UserAgent().random

    async def look_for_modlist(self, path: str) -> list:
        mod_list = next(os.walk(path))[2]
        del mod_list[0]
        if len(mod_list) == 0:
            return False
        else:
            await JarDecompile.look_for_jar(path)
            return mod_list

    async def load_file_for_translate(self, path: str) -> dict:
        async with aiofiles.open(path, mode='r') as file:
            content = await file.read()
            return ujson.loads(content)

    async def translate_request(self, api_key: str, from_: str, to_: str, loaded_json: dict) -> dict:
        url = "https://microsoft-translator-text.p.rapidapi.com/translate"
        querystring = {
            "from": from_,
            "to": to_,
            "api-version": "3.0",
            "profanityAction": "NoAction",
            "textType": "plain"
        }
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
            "Content-Type": "application/json",
            "user-agent": self.user_agent
        }
        
        async with aiohttp.ClientSession() as session:
            payload = [{"Text": val} for val in loaded_json.values()]
            async with session.post(url, json=payload, headers=headers, params=querystring) as response:
                data = await response.json()
                
        for i, (key, _) in enumerate(loaded_json.items()):
            loaded_json[key] = data[i]['translations'][0]['text']
        
        return loaded_json

    async def dump_translated_file(self, path: str, dictionary: dict):
        async with aiofiles.open(path / 'ru_ru.json', 'w', encoding='utf-8') as f:
            await f.write(ujson.dumps(dictionary, ensure_ascii=False))

    async def change_extension(self, path: str):
        try:
            os.rename(path, path.with_suffix('.jar'))
        except FileExistsError:
            return None