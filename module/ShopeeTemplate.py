import os, os.path
from module import File, Logger, String

def generateNewSimpleMassUploadFile(original_filename):
  DIR = 'Mass_Upload_File'
  fileCount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
  filenameWOExt = String.removeFileExt(original_filename, ['.xlsx'])
  newFileName = f"{DIR}/{filenameWOExt}_{fileCount + 1}.xlsx"
  newFilePath = File.copyFile(f'File_Template/{original_filename}', newFileName)
  Logger.logSuccess('New Mass Upload File Created: ' + newFilePath)
  return newFilePath