import shutil
import time
from pathlib import Path
import os

from loguru import logger

from src.client import Client
from config import MOD_PATH, API_KEY, LANG_FROM, LANG_TO


logger.add('.\\logs\\logs.txt', format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}', rotation="100 MB")


def main():
	client = Client()
	time1 = time.time()

	loc_mod_list = []
	unloc_mod_list = []
	
	task1 = client.look_for_modlist(path=MOD_PATH)
	if task1 == False:
		logger.error(f"Моды не найдены в папке {MOD_PATH}. Вы не забыли их добавить?")
	else:
		logger.info(f"Успешно декомпилированы {task1}")

	for index, value in enumerate(task1):
		try:
			en_us_path = next(Path(f"{os.path.join(MOD_PATH, value.split('.jar')[0])}").rglob('en_us.json'))
			lang_path = en_us_path.parents[0]
		except StopIteration:
			logger.error(f"{value.split('.jar')[0]} не имеет папки .\\lang. Этот мод не может быть переведен")
			shutil.rmtree(f"{os.path.join(MOD_PATH, value.split('.jar')[0])}")
			unloc_mod_list.append(value.split('.jar')[0])
			continue
		
		try:
			next(Path(f"{os.path.join(MOD_PATH, value.split('.jar')[0])}").rglob('ru_ru.json'))
		except StopIteration:
			task2 = client.load_file_for_translate(path=en_us_path)
			task3 = client.translate_request(api_key=API_KEY, from_=LANG_FROM, to_=LANG_TO, loaded_json=task2)
			logger.info(f"Успешно переведен {value.split('.jar')[0]}")

			task4 = client.dump_translated_file(path=lang_path, dictionary=task3)
			logger.info(f"Успешно создан файл локализации для {value.split('.jar')[0]}")

			shutil.make_archive(f"{value.split('.jar')[0]}",'zip', f"{os.path.join(MOD_PATH, value.split('.jar')[0])}")
			shutil.rmtree(f"{os.path.join(MOD_PATH, value.split('.jar')[0])}")
			path_to_mod = Path(f"{value.split('.jar')[0]}.zip")

			task5 = client.change_extension(path=path_to_mod)
			logger.info(f"Успешно скомпилирован {value.split('.jar')[0]}")
			loc_mod_list.append(value.split('.jar')[0])
		else:
			shutil.rmtree(f"{os.path.join(MOD_PATH, value.split('.jar')[0])}")
			logger.warning(f"{value.split('.jar')[0]} уже переведен")
			unloc_mod_list.append(value.split('.jar')[0])

	logger.success(f"Готово. Все локализованные моды находятся в родительской директории. Всего локализовано модов - {len(loc_mod_list)}. Не удалось локализовать модов - {len(unloc_mod_list)}")
	time2 = time.time()
	print(f"Итого времени: {time2 - time1} сек.")


if __name__ == "__main__":
	main()