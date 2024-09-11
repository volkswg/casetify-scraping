import shutil
import os
import json

def readFile(file_name, mode='r'):
  with open(file_name, mode=mode) as f:
    return [line.strip() for line in f if line.strip()]

def writeFile(file_name, data, mode='w'):
  with open(file_name, mode=mode) as file:
    file.write(data)

def copyFile(src, des):
  shutil.copyfile(src, des)

def readJSON(filepath):
  with open(filepath) as f:
    return json.load(f)


# backup function
def createDirIfNotExist(path_dir):
    os.makedirs(path_dir, exist_ok=True)
