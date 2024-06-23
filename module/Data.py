from module import Logger, GlobalVar
def transformProdOpt(product_options, shop_name, is_preorder = False):
  firstProdOpt = product_options[0]
  prodOptList = [{k: v for k, v in d.items() if k != 'title' and k != 'description'} for d in product_options]

  preDefineProdData = GlobalVar.databaseInstance.getProductPredefinedDetialByShopName(shop_name)
  prefixProdTitle = preDefineProdData['namePrefix']
  suffixProdTitle = preDefineProdData['nameSuffix']
  description = preDefineProdData['description']
  
  if is_preorder == True:
    prefixProdTitle = ''

  return {
    'productName': f"{prefixProdTitle}{firstProdOpt['title']}{suffixProdTitle}",
    'description': description,
    'options': prodOptList
  }
