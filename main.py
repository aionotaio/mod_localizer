import json, shutil, jad, os, requests, fake_useragent
from pathlib import Path


# Рандомный юзерагент
user_agent = fake_useragent.UserAgent().random

directory = '.\mods'

# Декомпилирует все .jar в папку
jad.lookforjars(directory)

dir_list = next(os.walk(directory))[2]
i = 0
while i < len(dir_list):
	print(f"Decompiled {dir_list[i].split('.jar')[0]}")

	en_us_path = next(Path(f".\mods\{dir_list[i].split('.jar')[0]}").rglob('en_us.json'))
	lang_path = en_us_path.parents[0]

	d = {}

	url = "https://microsoft-translator-text.p.rapidapi.com/translate"

	params = {
    	"from":"en",
    	"to":"ru",
    	"api-version":"3.0",
    	"profanityAction":"NoAction",
    	"textType":"plain"
    	}

	with open(en_us_path) as f:
		j = json.load(f)
		for key, val in j.items():
			payload = [{"Text": val}]
			headers = {
				"x-rapidapi-key": "6ddc8535dcmsh2f969065ad53e3bp1ed842jsn235cf35637b1",
				"x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
				"Content-Type": "application/json",
    			"user-agent": user_agent,
			}

			response = requests.post(url, json=payload, headers=headers, params=params)
			d[key] = response.json()[0]['translations'][0]['text']
		print(f"Translated {dir_list[i].split('.jar')[0]}")

	# Создает файл локализации ru_ru.json
	with (lang_path / 'ru_ru.json').open('x') as file:
		json.dump(d, file)

	# Создает zip-архив из папки
	shutil.make_archive(f"{dir_list[i].split('.jar')[0]}", 'zip', f".\mods\{dir_list[i].split('.jar')[0]}")

	# Удаляет папку
	shutil.rmtree(f".\mods\{dir_list[i].split('.jar')[0]}")

	# Меняет расширение на .jar 
	p = Path(f"{dir_list[i].split('.jar')[0]}.zip")
	p.rename(p.with_suffix('.jar'))
	print(f"Done {dir_list[i].split('.jar')[0]}. Localized mod is in the parent folder.")
	i += 1