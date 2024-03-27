from module import Logger

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
  
  deviceOptionList = ['iP15', 'iP15 Pro', 'iP15 ProMax', 'iP14', 'iP14 Pro', 'iP14 ProMax', 'iP13', 'iP13 Pro', 'iP13 ProMax', 'อื่นๆ ทักแชทเลย']
  
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
        sheet['L' + str(rowNumber)] = opt['caseType'] # reset
        sheet['M' + str(rowNumber)] = opt['imageSrc'] # reset
        sheet['N' + str(rowNumber)] = "รุ่น" # reset
        sheet['O' + str(rowNumber)] = deviceOpt # reset
        sheet['P' + str(rowNumber)] = opt['price'] # price
        sheet['Q' + str(rowNumber)] = '10' # quantiry
        # add image 
        imageList = eProduct['imageList']
        picColumn = ['T','U','V','W','X','Y','Z','AA','AB']
        try:
          for imgListIndex, eImage in enumerate(imageList):
            sheet[picColumn[imgListIndex] + str(rowNumber)] = eImage
        except:
          Logger.logDebug('Image Exceed Limit')
        sheet['AC' + str(rowNumber)] = '0.3'
        sheet['AD' + str(rowNumber)] = '12'
        sheet['AE' + str(rowNumber)] = '22'
        sheet['AF' + str(rowNumber)] = '3'
        sheet['AG' + str(rowNumber)] = 'เปิด'
        # sheet['AC' + str(rowNumber)] = 'เปิด'
        rowNumber += 1
  xfile.save(filename)
  xfile.close()


#  backup function 
def cleanUpTemplateFile(template_file_name):
  xfile = openpyxl.load_workbook(template_file_name)
  sheet = xfile['แบบฟอร์มการลงสินค้า']
  startIndex = 7
  endIndex = 100
  for index in range(startIndex,endIndex):
    sheet['A'+str(index)] = '' # category id 
    sheet['B'+str(index)] = '' # product name
    sheet['C'+str(index)] = '' # product detail
    sheet['E'+str(index)] = '' # reset
    sheet['F'+str(index)] = '' # reset
    sheet['G'+str(index)] = '' # reset
    sheet['H'+str(index)] = '' # reset
    sheet['K'+str(index)] = '' # price
    sheet['L'+str(index)] = '' # quantiry
    # add image 
    picColumn = ['O','P','Q','R','S','T','U','V','W']
    for columnName in picColumn:
      sheet[columnName + str(index)] = ''
    sheet['X'+str(index)] = ''
    sheet['Y'+str(index)] = ''
    sheet['Z'+str(index)] = ''
    sheet['AA'+str(index)] = ''
    sheet['AB'+str(index)] = ''
    sheet['AC'+str(index)] = ''
  xfile.save(template_file_name)
  xfile.close()