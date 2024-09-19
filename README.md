[![works on my machine badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.4.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

# Локализатор для модов Minecraft

## Функционал
- Автоматически переводит моды с английского на русский, используя бесплатный план Microsoft Translator Text API на RapidAPI

## Запуск

Python version: 3.10+

Installing virtual env: \
`pip install virtualenv` \
`cd <project_dir>` \
`python -m venv venv`


Activating: 
 - Mac/Linux - `source venv/bin/activate` 
 - Windows - `.\venv\Scripts\activate` 

Installing all dependencies: \
`pip install -r requirements.txt`

Run main script: \
`python main.py`

## Результаты
`logs/` - Директория с логами \
`./` - Родительская директория с переведенными модами

## FAQ

- Q - Где получить новый `api_key` если тот, который находится в коде закончится?
- A - https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/microsoft-translator-text -> регистрируешься и выбираешь `Basic plan`. Он полностью бесплатный, не требует ввода платежной информации и тп. Остается только скопировать `X-RapidAPI-Key` и вставить его в поле `api_key` в `config.py`

## Credits

- Я использовал и немного модифицировал модуль JadPY от Mike Arpaia, чтобы декомпилировать `.jar` файлы в моем проекте, https://github.com/marpaia/jadPY. 
