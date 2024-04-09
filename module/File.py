import shutil
import os 
import json

def readFile(file_name, mode='r'):
  result = []
  with open(file_name, mode=mode) as f:
    lines = f.readlines()
    for line in lines:
      if line.__len__() > 1:
        result.append(line.replace('\n', ''))
  return result
      
def writeFile(file_name, data, mode):
  with open(file_name, mode=mode) as file:
    file.write(data)
    
def copyFile(src, des): 
  return shutil.copyfile(src, des)

def readJSON(filepath):
  f = open(filepath)
  data = json.load(f)
  return data


# backup function 
def createDirIfNotExsit(path_dir):
  if not os.path.exists(path_dir):
    os.makedirs(path_dir)

  