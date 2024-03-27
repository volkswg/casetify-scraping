from module import Logger

def addCharacterToFit(text):
  txtLen = text.__len__()
  result = text
  if txtLen < 60:
    result += '​' * (60 - txtLen) 
  return result

def replaceForbiddenWord(text):
  result = text.replace('MagSafe', 'MS').replace('Compatible', '')
  # fill txt to fit len >= 60
  txtLen = text.__len__()
  if txtLen < 60:
    result += '​' * (60 - txtLen)
  return addCharacterToFit(result)

def removeExtraFileExt(filename, ext_list = ['.png','.jpg','.jpeg']):
  extIndex = 0
  for eExt in ext_list:
    try:
      extIndex = filename.index(eExt) + eExt.__len__()
      break
    except:
      continue
  if extIndex == 0:
    Logger.logWarn('Not Found Ext')
    return eExt
  return filename[0:extIndex]

def removeFileExt(filename, ext_list = ['.xlsx']):
  extIndex = 0
  for eExt in ext_list:
    try:
      extIndex = filename.index(eExt)
      break
    except:
      continue
  if extIndex == 0:
    Logger.logWarn('Not Found Ext')
    return eExt
  return filename[0:extIndex]

def convertPriceToInt(priceTxt):
  if 'THB' in priceTxt:
    return int(priceTxt.replace('THB', ''))
  elif 'HK$' in priceTxt:
    return int(priceTxt.replace('HK$', '')) * 5
  elif 'S$' in priceTxt:
    return int(priceTxt.replace('S$', '')) * 5
    
def extractProductDetail(prod_detail_text):
  detailSplitted = prod_detail_text.split('\n')
  return {
    'productName': detailSplitted[0],
    'deviceName': detailSplitted[1],
    'caseType': detailSplitted[2].strip(),
    'color': detailSplitted[3]
  }

def extractProductName(url_path = ""):
  splitted_path = url_path.split('/')
  product_name = splitted_path[5]
  return product_name