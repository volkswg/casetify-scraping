import os, os.path
from module import File, Logger, String, Database

def generateNewSimpleMassUploadFile(shop_name):
  templateFilePath = Database.getTemplateFilenameByShopName(shop_name)
  templateFileName = templateFilePath.split('/')[-1]
  DIR = 'Mass_Upload_File'
  fileCount = len([filename for filename in os.listdir(DIR) if filename.endswith('.xlsx')])
  Logger.logDebug(fileCount)
  filenameWOExt = String.removeFileExt(templateFileName, ['.xlsx'])
  newFileName = f"{DIR}/{filenameWOExt}_{fileCount + 1}.xlsx"
  newFilePath = File.copyFile(f'{templateFilePath}', newFileName)
  Logger.logSuccess('New Mass Upload File Created: ' + newFilePath)
  return newFilePath