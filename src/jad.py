import os
import glob
import zipfile
import asyncio

import aiofiles


class JarDecompile:
    @staticmethod
    async def unzip_jar(jar):
        with zipfile.ZipFile(jar) as file:
            extract_path = os.path.splitext(jar)[0]
            for file_info in file.infolist():
                extracted_path = os.path.join(extract_path, file_info.filename)
                if file_info.is_dir():
                    os.makedirs(extracted_path, exist_ok=True)
                else:
                    os.makedirs(os.path.dirname(extracted_path), exist_ok=True)
                    async with aiofiles.open(extracted_path, 'wb') as f:
                        await f.write(file.read(file_info.filename))

    @staticmethod
    async def look_for_jar(path):
        tasks = []
        for currentFile in glob.glob(os.path.join(path, "*")):
            if os.path.isdir(currentFile):
                tasks.append(JarDecompile.look_for_jar(currentFile))
            elif os.path.splitext(currentFile)[1] == '.jar':
                tasks.append(JarDecompile.unzip_jar(currentFile))
        await asyncio.gather(*tasks)