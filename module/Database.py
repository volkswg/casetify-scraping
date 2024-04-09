from module import File

def getShopList():
  shopDataList = File.readJSON('./Data/shop.json')
  shopeNameList =  [e['shopName'] for e in shopDataList]
  return shopeNameList

def getTemplateFilenameByShopName(shop_name):
  shopDataList = File.readJSON('./Data/shop.json')
  shopData = next((eShop for eShop in shopDataList if eShop['shopName'] == shop_name), None)
  return shopData['templateFile']

def getProductPredefinedDetialByShopName(shop_name):
  shopDataList = File.readJSON('./Data/shop.json')
  shopData = next((eShop for eShop in shopDataList if eShop['shopName'] == shop_name), None)
  return shopData['product']

# case type 
def getCaseTypeByDisplayText(displayText):
  caseTypeList = File.readJSON('./Data/caseType.json')
  [filteredCaseTypeInfo] = list(filter(lambda caseTypeInfo: caseTypeInfo['displayText'] == displayText, caseTypeList))
  return filteredCaseTypeInfo

def isRequireCaseType(displayText):
  caseTypeInfo = getCaseTypeByDisplayText(displayText)
  return caseTypeInfo['required']

def getCaseTypeOptName(displayText):
  caseTypeInfo = getCaseTypeByDisplayText(displayText)
  return caseTypeInfo['optValue']

def isRequireColor(caseTypeDisplayText, colorDisplayText):
  caseTypeInfo = getCaseTypeByDisplayText(caseTypeDisplayText)
  caseColorList = caseTypeInfo['colorList']
  filteredColorInfo = list(filter(lambda colorInfo: colorInfo['displayText'] == colorDisplayText, caseColorList))
  if len(filteredColorInfo) < 1:
    return False
  return True
  
def getColorInfo(caseTypeDisplayText, colorDisplayText):
  caseTypeInfo = getCaseTypeByDisplayText(caseTypeDisplayText)
  caseColorList = caseTypeInfo['colorList']
  filteredColorInfo = list(filter(lambda colorInfo: colorInfo['displayText'] == colorDisplayText, caseColorList))
  if len(filteredColorInfo) < 1:
    return False
  return filteredColorInfo[0]

# device list 
def getDeviceList():
  deviceList = File.readJSON('./Data/deviceList.json')
  return deviceList


def getSellingPrice(ogPrice, isColab):
  priceMapper = File.readJSON('./Data/priceMapper.json')
  queryText = 'normal'
  if isColab == True:
    queryText = 'colab'
  return priceMapper[queryText][f"{ogPrice}"]