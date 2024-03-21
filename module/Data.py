def transformProdOpt(product_options):
  firstProdOpt = product_options[0]
  caseTypeMapper = {
    "Ultra Bounce Case MS": "",
    "Bounce Case MS": "",
    "Impact Ring Stand Case MS": "",
    "Impact Case MS": "ImpactCaseMS",
    "Clear Case MS": "ClearCaseMS",
    "Mirror Case MS": "MirrorCaseMS",
    "Impact Case": "ImpactCase"
  }
  prodOptList = [{k: v for k, v in d.items() if k != 'title' and k != 'description'} for d in product_options]
  result = []
  for eProdOpt in prodOptList:
    caseType = eProdOpt["caseType"]
    caseTypeOptName = caseTypeMapper[caseType]
    if caseTypeOptName != "":
      eProdOpt['caseType'] = caseTypeOptName
      result.append(eProdOpt)
  return {
    'productName': firstProdOpt['title'],
    'description': firstProdOpt['description'],
    'options': result
  }
