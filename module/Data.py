from module import Database
def transformProdOpt(product_options, case_type_mapper, shop_name, is_preorder = False):
  firstProdOpt = product_options[0]
  prodOptList = [{k: v for k, v in d.items() if k != 'title' and k != 'description'} for d in product_options]
  result = []
  for eProdOpt in prodOptList:
    caseType = eProdOpt["caseType"]
    
    caseTypeOptInfo = case_type_mapper[caseType]
    if caseTypeOptInfo["isSelected"] == True:
      eProdOpt['caseType'] = caseTypeOptInfo["optValue"]
      result.append(eProdOpt)
  
    preDefineProdData = Database.getProductPredefinedDetialByShopName(shop_name)
  
    prefixProdTitle = preDefineProdData['namePrefix']
    suffixProdTitle = preDefineProdData['nameSuffix']
    description = preDefineProdData['description']
  if is_preorder == True:
    prefixProdTitle = ''
  return {
    'productName': f"{prefixProdTitle}{firstProdOpt['title']}{suffixProdTitle}",
    'description': description,
    'options': result
  }
