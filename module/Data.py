def transformProdOpt(product_options):
  firstProdOpt = product_options[0]
  caseTypeMapper = {
    "Ultra Bounce Case MS": "",
    "Bounce Case MS": "",
    "Pride Impact Case MS": "",
    "Impact Ring Stand Case MS": "MagSafe/RingStand",
    "Impact Case MS": "MagSafe/Impact",
    "Clear Case MS": "MagSafe/Clear",
    "Clear Case": "Clear",
    "Mirror Case MS": "MagSafe/Mirror",
    "Impact Case": "Impact",
    "Leather Case MS": "MagSafe/Leather",
    "Impact Ring Stand Case": "",
    "Mirror Case": "Mirror",
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
    'description': f"✅ จำหน่ายสินค้าแท้จาก Casetify Officials Store\n✅ มีประกันสินค้า 12 เดือน\n✅ ไม่ต้องเสียภาษีนำเข้าเอง\n✅ ได้สินค้าไวแน่นอน",
    'options': result
  }
