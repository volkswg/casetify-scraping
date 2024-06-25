from module import File, Logger

class Database:
  def __init__(self):
    self.deviceBrand = "Apple" # default
    self.deviceBrandLowerCase = "apple" # default
    self.caseTypeData = File.readJSON('./Data/caseType.json')
    self.shopListData = File.readJSON('./Data/shop.json')
    self.deviceList = File.readJSON('./Data/deviceList.json')
    self.priceMapper = File.readJSON('./Data/priceMapper.json')
    
  def __getCaseTypeList(self):
    return self.caseTypeData[self.deviceBrandLowerCase]
  
  def __getCaseTypeByDisplayText(self, displayText):
    caseTypeList = self.__getCaseTypeList()
    [filteredCaseTypeInfo] = list(filter(lambda caseTypeInfo: caseTypeInfo['displayText'] == displayText, caseTypeList))
    return filteredCaseTypeInfo
  
  def setDeviceBrand(self, deviceBrand):
    self.deviceBrand = deviceBrand
    self.deviceBrandLowerCase = deviceBrand.lower()
  
  def isRequireCaseType(self, displayText):
    caseTypeInfo = self.__getCaseTypeByDisplayText(displayText)
    return caseTypeInfo['required']
    
  def getCaseTypeOptName(self, displayText):
    caseTypeInfo = self.__getCaseTypeByDisplayText(displayText)
    return caseTypeInfo['optValue']
  
  # def isRequireColor(self, caseTypeDisplayText, colorDisplayText):
  #   caseTypeInfo = self.__getCaseTypeByDisplayText(caseTypeDisplayText)
  #   caseColorList = caseTypeInfo['colorList']
  #   filteredColorInfo = list(filter(lambda colorInfo: colorInfo['displayText'] == colorDisplayText, caseColorList))
  #   if len(filteredColorInfo) < 1:
  #     return False
  #   return True
  
  def getColorInfo(self, caseTypeDisplayText, colorDisplayText):
    caseTypeInfo = self.__getCaseTypeByDisplayText(caseTypeDisplayText)
    caseColorList = caseTypeInfo['colorList']
    filteredColorInfo = list(filter(lambda colorInfo: colorInfo['displayText'] == colorDisplayText, caseColorList))
    if len(filteredColorInfo) < 1:
      return False
    return filteredColorInfo[0]
  
  def getCaseTypeIdByOptName(self, opt_name):
    caseTypeList = self.__getCaseTypeList()
    [filteredCaseTypeInfo] = list(filter(lambda caseTypeInfo: caseTypeInfo['optValue'] == opt_name, caseTypeList))
    return filteredCaseTypeInfo['id']
  
  # ============= shop list ==============
  def getShopList(self):
    return [e['shopName'] for e in  self.shopListData]
  
  def getTemplateFilenameByShopName(self, shop_name):
    shopData = next((eShop for eShop in self.shopListData if eShop['shopName'] == shop_name), None)
    return shopData['templateFile']

  def getProductPredefinedDetialByShopName(self, shop_name):
    shopData = next((eShop for eShop in self.shopListData if eShop['shopName'] == shop_name), None)
    return shopData['product']
  
  # ============= device list ==============
  def getDeviceList(self):
    newDeviceList = self.deviceList[self.deviceBrandLowerCase]
    newDeviceList.sort(key=lambda x: x['order'])
    return newDeviceList
  
  # ============= price mapper ==============
  def getSellingPrice(self, ogPrice, isColab):
    queryText = 'normal'
    if isColab == True:
      queryText = 'colab'
    return self.priceMapper[queryText][f"{ogPrice}"]