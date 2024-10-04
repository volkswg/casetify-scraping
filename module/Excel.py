from module import Logger, Database, GlobalVar

import openpyxl

def editExcelfile(filename, product_list):
  columnMapper = {
    "categoryId": 'A',
    "productName": 'B',
    "productDetail": 'C',
    "optionRefNumber": "J",
    "optName1": 'K',
    "optValue1": 'L',
    "opt1Img": 'M',
    "optName2": 'N',
    "optValue2": 'O',
    "price": 'P',
    "quantity": 'Q',
    "weight": 'AC',
    "length": 'AD',
    "width": 'AE',
    "height": 'AF',
    "standardDelivery": 'AG',
    "instantDelivery": 'AH'
  }
  xfile = openpyxl.load_workbook(filename)
  sheet = xfile['แบบฟอร์มการลงสินค้า']
  
  deviceOptionList = GlobalVar.databaseInstance.getDeviceList()
  
  templateStartRow = 7
  # loop through product list
  rowNumber = templateStartRow
  for prodIdx, eProduct in enumerate(product_list):
    # loop through product option list (case type)
    for opt in eProduct['options']:
      for deviceOpt in deviceOptionList:
        sheet['A' + str(rowNumber)] = '100490' # category id 
        sheet['B' + str(rowNumber)] = eProduct['productName'] # product name
        sheet['C' + str(rowNumber)] = eProduct['description'] # product detail
        sheet['J' + str(rowNumber)] = prodIdx + 1 # product detail
        sheet['K' + str(rowNumber)] = "ชนิดเคส" # reset
        sheet['L' + str(rowNumber)] = f"{opt['caseType']} {opt["caseColor"]}".strip() # reset
        sheet['M' + str(rowNumber)] = opt['imageSrc'] # reset
        sheet['N' + str(rowNumber)] = "รุ่น" # reset
        sheet['O' + str(rowNumber)] = deviceOpt['name'] # reset

        quantity = 10
        caseTypeId = GlobalVar.databaseInstance.getCaseTypeIdByOptName(opt["caseType"])
        match caseTypeId:
          case 'msimpact':
            match opt["caseColor"]:
              case 'Blue':
                if deviceOpt['id'] not in ['dvip15pro', 'dvip15promax', 'dvetc']:
                  quantity = 0
              case 'Candy':
                if deviceOpt['id'] not in ['dvip15', 'dvip15pro', 'dvip15promax', 'dvip15plus','dvip14pro', 'dvip14promax', 'dvetc']:
                  quantity = 0
          case 'msclear':
            if opt['caseColor'] == 'Pink':
              if deviceOpt['id'] not in ['dvip15', 'dvip15pro', 'dvip15promax', 'dvip15plus', 'dvetc']:
                quantity = 0
          case 'impact':
            if opt["caseColor"] == 'Candy':
              if deviceOpt['id'] not in ['dvip15', 'dvip15pro', 'dvip15promax', 'dvip15plus', 'dvetc']:
                quantity = 0
          
        sheet['P' + str(rowNumber)] = opt['price'] # price
        sheet['Q' + str(rowNumber)] = quantity # quantiry
        # add image 
        imageList = eProduct['imageList']
        picColumn = ['U','V','W','X','Y','Z','AA','AB', 'AC']
        try:
          for imgListIndex, eImage in enumerate(imageList):
            sheet[picColumn[imgListIndex] + str(rowNumber)] = eImage
        except:
          Logger.logDebug('Image Exceed Limit')
        sheet['AD' + str(rowNumber)] = '0.3'
        sheet['AE' + str(rowNumber)] = '12'
        sheet['AF' + str(rowNumber)] = '22'
        sheet['AG' + str(rowNumber)] = '3'
        sheet['AH' + str(rowNumber)] = 'เปิด'
        # sheet['AC' + str(rowNumber)] = 'เปิด'
        rowNumber += 1
  xfile.save(filename)
  xfile.close()


#  backup function 
def cleanUpTemplateFile(template_file_name):
  xfile = openpyxl.load_workbook(template_file_name)
  sheet = xfile['แบบฟอร์มการลงสินค้า']
  startIndex, endIndex = 7, 100
  columns_to_clear = ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'K', 'L', 'X', 'Y', 'Z', 'AA', 'AB', 'AC']
  picColumns = ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
  
  for index in range(startIndex, endIndex):
    for col in columns_to_clear + picColumns:
      sheet[f'{col}{index}'] = ''
  
  xfile.save(template_file_name)
  xfile.close()
