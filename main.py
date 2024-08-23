import json, shutil, jad, os, requests, fake_useragent, logging
from pathlib import Path
from config import api_key

# Настройка логирования
file_log = logging.FileHandler('.\logs\logs.txt')
console_log = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_log), level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# Рандомный юзерагент
user_agent = fake_useragent.UserAgent().random

# Директория с модами
directory = '.\mods'

# Декомпилирует все .jar в папку
jad.lookforjars(directory)

mod_list = next(os.walk(directory))[2]
del mod_list[0]
if len(mod_list) == 0:
	logging.info(f"| Mods haven't found in the .\mods folder. Did you forget to add the mods?")
else:
	logging.info(f"| Successfully decompiled {mod_list}")

loc_mod_list = []
unloc_mod_list = []

i = 0
while i < len(mod_list):
	try:
		en_us_path = next(Path(f".\mods\{mod_list[i].split('.jar')[0]}").rglob('en_us.json'))
	except StopIteration:
		logging.error(f"{mod_list[i].split('.jar')[0]} doesn't have a .\lang folder. This mod can't be translated.")
		shutil.rmtree(f".\mods\{mod_list[i].split('.jar')[0]}")
		unloc_mod_list.append(mod_list[i].split('.jar')[0])
		i += 1
		continue
	lang_path = en_us_path.parents[0]
	d = {}
	try:
		next(Path(f".\mods\{mod_list[i].split('.jar')[0]}").rglob('ru_ru.json'))
	except StopIteration:
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
					"x-rapidapi-key": api_key,
					"x-rapidapi-host": "microsoft-translator-text.p.rapidapi.com",
					"Content-Type": "application/json",
    				"user-agent": user_agent,
				}

				response = requests.post(url, json=payload, headers=headers, params=params)
				d[key] = response.json()[0]['translations'][0]['text']
			logging.info(f"| Successfully translated {mod_list[i].split('.jar')[0]}")

		# Создает файл локализации ru_ru.json
		with (lang_path / 'ru_ru.json').open('x', encoding='utf-8') as file:
			json.dump(d, file, ensure_ascii=False)
			logging.info(f"| Successfully created localization file for {mod_list[i].split('.jar')[0]}")
			
		# Создает zip-архив из папки
		shutil.make_archive(f"{mod_list[i].split('.jar')[0]}", 'zip', f".\mods\{mod_list[i].split('.jar')[0]}")

		# Удаляет папки
		shutil.rmtree(f".\mods\{mod_list[i].split('.jar')[0]}")

		# Меняет расширение на .jar 
		p = Path(f"{mod_list[i].split('.jar')[0]}.zip")
		try:
			p.rename(p.with_suffix('.jar'))
		except FileExistsError:
			logging.warning(f"| File {mod_list[i]} already exists")
			i += 1
			continue
		else:
			logging.info(f"| Successfully compiled {mod_list[i].split('.jar')[0]}")
			loc_mod_list.append(mod_list[i].split('.jar')[0])
	else:
		shutil.rmtree(f".\mods\{mod_list[i].split('.jar')[0]}")
		logging.warning(f"| Mod {mod_list[i].split('.jar')[0]} already localized")
		unloc_mod_list.append(mod_list[i].split('.jar')[0])
		i += 1
		continue
	i += 1
logging.info(f"| Finished. All localized mods are in the parent directory. Total localized mods - {len(loc_mod_list)}. Failed localized mods - {len(unloc_mod_list)}")
