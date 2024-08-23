# Minecraft Mods Localizer

- Localizes mods for Minecraft using free plan of Microsoft Translator Text API on RapidAPI


## Run

Python version: 3.10+

<<<<<<< HEAD
- Installing virtual env:
```
pip install virtualenv
cd "project_path" // Change directory to project's one (unpack downloaded zip-file, right click on project's folder -> copy as path)
python -m venv venv
```
=======
- Installing virtual env: 
	`pip install virtualenv`
	`cd "project_path"` - Change directory to project's one (right click on downloaded project's folder -> copy as path
	`python -m venv venv`
  
>>>>>>> a73976dd46dc12b46556b2d1226c6f7ec106ab87

- Activating:
	- Mac/Linux - `source venv/bin/activate`
	- Windows - `.\venv\Scripts\activate`

- Installing all dependencies:
`pip install -r requirements.txt`

- Run main script:
`python main.py`

## FAQ

- Q - Where can i get a new API key if that one in the code expires?
- A - Go to the https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/microsoft-translator-text, reg on the website and choose Basic plan. It's absolutely free and the only thing you need to do now is to copy your `X-RapidAPI-Key` and paste it in `api_key` in `config.py`

## Credits

- I used JadPY utility by Mike Arpaia to decompile `.jar` files in my project, https://github.com/marpaia/jadPY. All rights belongs to him.