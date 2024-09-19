import os
import glob
import zipfile


class JarDecompile:
	def unzip_jar(jar):
		file = zipfile.ZipFile(jar)
		file.extractall(os.path.splitext(jar)[0])

	def look_for_jar(path):
		for currentFile in glob.glob(os.path.join(path, "*")):
			if os.path.isdir(currentFile):
				JarDecompile.look_for_jar(currentFile)
			elif os.path.splitext(currentFile)[1] == '.jar':
				JarDecompile.unzip_jar(currentFile)
