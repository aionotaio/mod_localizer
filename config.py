import os
import sys
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

API_KEY = '6ddc8535dcmsh2f969065ad53e3bp1ed842jsn235cf35637b1'

# Do not change
LANG_FROM = 'en'
MOD_PATH = os.path.join(ROOT_DIR, 'files')
LANG_TO = 'ru'

