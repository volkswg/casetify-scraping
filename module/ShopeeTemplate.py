import os, os.path
from module import File, Logger

def generateNewSimpleMassUploadFile(original_filename):
  DIR = 'Mass_Upload_File'
  fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
  Logger.logDebug('fileCount')
  Logger.logDebug(fileCount)
  newFileName = f"{DIR}/{original_filename}_{fileCount + 1}.xlsx"
  newFilePath = File.copyFile(f'File_Template/{original_filename}', newFileName)
  Logger.logSuccess('New Mass Upload File Created: ' + newFilePath)
  return newFilePath