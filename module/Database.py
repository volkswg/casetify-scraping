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
  