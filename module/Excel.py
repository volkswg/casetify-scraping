from module import Logger

import openpyxl

def editExcelfile(filename, product_list):
  columnMapper = {
    "categoryId": 'A',
    "productName": 'B', 
    "productDetail": 'C',
    "optionRefNumber": "E",
    "optName1": 'F',
    "optValue1": 'G',
    "opt1Img": 'H',
    "optName2": 'I',
    "optValue2": 'J',
    "price": 'K',
    "quantity": 'L',
    "weight": 'X',
    "length": 'Y',
    "width": 'Z',
    "height": 'AA',
    "standardDelivery": 'AB',
    "instantDelivery": 'AC'
  }
  xfile = openpyxl.load_workbook(filename)
  sheet = xfile['แบบฟอร์มการลงสินค้า']
  
  templateStartRow = 7
  # loop through product list
  rowNumber = templateStartRow
  for prodIdx, eProduct in enumerate(product_list):
    # loop through product option list (case type)
    for opt in eProduct['options']:
      sheet['A' + str(rowNumber)] = '100490' # category id 
      sheet['B' + str(rowNumber)] = eProduct['productName'] # product name
      sheet['C' + str(rowNumber)] = eProduct['description'] # product detail
      sheet['E' + str(rowNumber)] = prodIdx + 1 # product detail
      sheet['F' + str(rowNumber)] = "ชนิดเคส" # reset
      sheet['G' + str(rowNumber)] = opt['caseType'] # reset
      sheet['H' + str(rowNumber)] = opt['imageSrc'] # reset
      sheet['I' + str(rowNumber)] = "รุ่น" # reset
      sheet['J' + str(rowNumber)] = "iPhone 15 ProMax" # reset
      sheet['K' + str(rowNumber)] = opt['price'] # price
      sheet['L' + str(rowNumber)] = '10' # quantiry
      # add image 
      imageList = eProduct['imageList']
      picColumn = ['O','P','Q','R','S','T','U','V','W']
      for imgListIndex, eImage in enumerate(imageList):
        sheet[picColumn[imgListIndex] + str(rowNumber)] = eImage
      sheet['X' + str(rowNumber)] = '0.3'
      sheet['Y' + str(rowNumber)] = '12'
      sheet['Z' + str(rowNumber)] = '22'
      sheet['AA' + str(rowNumber)] = '3'
      sheet['AB' + str(rowNumber)] = 'เปิด'
      sheet['AC' + str(rowNumber)] = 'เปิด'
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