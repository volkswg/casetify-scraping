from module import Logger, String, Data, Math, SeleniumBootstrap as SB, GlobalVar
from selenium.webdriver.common.by import By
import time

XPATH_ELEMS = {
  "ARTWORK_TITLE": '//div[@data-label="artwork-name"]/span',
  "ARTWORK_IMAGES": '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img',
  "DEVICE_DROPDOWN_CONTAINER": '//div[contains(@class, "device-resolver-container")]',
  "DEVICE_DROPDOWN_OPTIONS": '//div[contains(@class, "brand-drop-down-container")]',
  "WAITLIST_FORM_CONTAINER": '//div[contains(@class, "waitlist-form-container")]',
  "PRODUCT_ACTION_BUTTON": '//div[@id="PRODUCT_ACTION"]/div[contains(@class, "product-action-btn-container")]/button[contains(@class, "shopping-cart-button")]',
  "CASE_TYPE_ITEM_PRICE": '//div[contains(@class, "product-container position-relative current")]//div[@data-label="case-type-item-price"]',
  "COLOR_ITEMS": '//ul[@data-label="color-items"]//div[contains(@class, "item")]',
  "SELECTED_COLOR_NAME": '//div[@data-label="selected-color-name"]',
  "CASE_TYPE_NAME": '//div[contains(@class, "product-container position-relative current")]//div[@data-label="case-type-name"]/span',
  "CASE_TYPE_ITEMS": '//div[@data-label="case-type-items"]//div[contains(@class, "item")]'
}

def checkNewCaseTypeReady(driver):
  while True:
    imageElems = SB.findElements(driver, By.XPATH, XPATH_ELEMS['ARTWORK_IMAGES'])
    if imageElems and imageElems[0].get_attribute('complete') == 'true':
      break

def getProductTitle(driver):
  title_elem = driver.find_element(By.XPATH, XPATH_ELEMS['ARTWORK_TITLE'])
  return title_elem.get_attribute('innerHTML')

def selectDeviceBrand(driver, brand = 'Apple'):
  # Wait for device dropdown to render
  SB.findElements(driver, By.XPATH, XPATH_ELEMS['DEVICE_DROPDOWN_CONTAINER'])
  deviceBrandSelectorElems = SB.findElements(driver, By.XPATH, XPATH_ELEMS['DEVICE_DROPDOWN_OPTIONS'], is_waiting=False)
  
  if not deviceBrandSelectorElems:
    Logger.logWarn('This product only has 1 brand')
    return
  
  # Select device brand
  deviceBrandSelectorElems[0].click()
  
  [optionElem] = SB.findElements(driver, By.XPATH, f'//div[contains(@class, "brand-drop-down-container")]//option[contains(text(), "{brand}")]')
  optionElem.click()

def getProductDetail(driver, product_title, case_type_btn, case_type_display_txt, is_colabs, is_preorder = False):
  # check item is not available
  waitListContainer = driver.find_elements(By.XPATH, XPATH_ELEMS['WAITLIST_FORM_CONTAINER'])
  isWaitingList = waitListContainer.__len__() > 0
  if isWaitingList == True:
    return False
  # download case type image
  productImageContainer = SB.findElements(driver, By.XPATH, XPATH_ELEMS['ARTWORK_IMAGES'])
  imageContanerLen = productImageContainer.__len__()
  
  if imageContanerLen < 1 :
    Logger.logError('Something Error on fetch option image')
    
  srcUrl = productImageContainer[0].get_attribute('src')
  srcUrl = String.removeExtraFileExt(srcUrl)
  
  # addToCartBtn = driver.find_elements(By.XPATH, XPATH_ELEMS['PRODUCT_ACTION_BUTTON'])
  
  # fetch product title here
  productTitle = product_title
  
  priceElem = case_type_btn.find_element(By.XPATH, XPATH_ELEMS['CASE_TYPE_ITEM_PRICE'])
  price = String.convertPriceToInt(priceElem.text)
  Logger.logDebug(price)
  finalPrice = Math.calculateSellingPrice(price, is_preorder, is_colabs)
  
  # fetch color
  colorItems = SB.findElements(driver, By.XPATH, XPATH_ELEMS['COLOR_ITEMS'])
  productDetailList = []
  if len(colorItems) > 1:
    for eColorBtn in colorItems:
      SB.scrollToElement(driver, eColorBtn)
      eColorBtn.click()
        
      colorDidplayTextElem = driver.find_element(By.XPATH, XPATH_ELEMS['SELECTED_COLOR_NAME'])
      colorInfo = GlobalVar.databaseInstance.getColorInfo(case_type_display_txt, colorDidplayTextElem.text)
      if colorInfo != False:
        
        # fetch image =====
        productImageContainer = SB.findElements(driver, By.XPATH, XPATH_ELEMS['ARTWORK_IMAGES'])
        imageContanerLen = productImageContainer.__len__()
        
        if imageContanerLen < 1 :
          Logger.logError('Something Error on fetch option image')
          
        srcUrl = productImageContainer[0].get_attribute('src')
        srcUrl = String.removeExtraFileExt(srcUrl)
        # fetch image =====
        productDetailList.append({
          'title': productTitle,
          'description': 'description',
          'price': finalPrice,
          'caseType': f"{GlobalVar.databaseInstance.getCaseTypeOptName(case_type_display_txt)}",
          'caseColor': f"{colorInfo['optValue']}",
          'imageSrc': srcUrl
        })
  else:
    productDetailList.append({
      'title': productTitle,
      'description': 'description',
      'price': finalPrice,
      'caseType': GlobalVar.databaseInstance.getCaseTypeOptName(case_type_display_txt),
      'caseColor': "",
      'imageSrc': srcUrl
    })
  
  return productDetailList

def clickCaseType(driver, element):
  for _ in range(5):
    try:
      SB.scrollToElement(driver, element)
      element.click()
      return
    except:
      continue
  raise Exception("Error Retry Exceed")

def getCaseTypeDisplayText(driver):
  [caseTypeDisplayTextElem] = SB.findElements(driver, By.XPATH, XPATH_ELEMS['CASE_TYPE_NAME'])
  return caseTypeDisplayTextElem.text

def getCoverImage(driver): 
  productImageContainer = SB.findElements(driver, By.XPATH, XPATH_ELEMS['ARTWORK_IMAGES'])
  imageContanerLen = productImageContainer.__len__()

  if imageContanerLen < 1 :
    Logger.logError('Something Error on fetch image')
    print(productImageContainer)
    return []
      
  prodCoverImgUrlList = []
  for imageElem in productImageContainer:
    srcUrl = imageElem.get_attribute('src')
    srcUrl = String.removeExtraFileExt(srcUrl)
    prodCoverImgUrlList.append(srcUrl)
  return prodCoverImgUrlList
    
def getCaseDataFromUrl(driver, url, shope_name, is_colabs, is_preorder = False, brand = 'Samsung'):
  driver.get(url)
  
  productTitle = getProductTitle(driver)
  Logger.logDebug(f'[Start] Fetching "{productTitle}"')
  
  # waiting for device dropdown rendered
  # selectDeviceBrand(driver, brand)
  prodImgUrlList = getCoverImage(driver)
  
  # get all product option
  caseTypeBtnList = SB.findElements(driver, By.XPATH, XPATH_ELEMS['CASE_TYPE_ITEMS'])
  prodOptList = []
  caseTypeBtnListLen = caseTypeBtnList.__len__()
  for eBtn in caseTypeBtnList:
    if caseTypeBtnListLen > 1:
      clickCaseType(driver, eBtn)
      checkNewCaseTypeReady(driver)
    caseTypeDisplayText = getCaseTypeDisplayText(driver)
    Logger.logDebug(caseTypeDisplayText)
    isRequiredCaseType = GlobalVar.databaseInstance.isRequireCaseType(caseTypeDisplayText)
    if isRequiredCaseType == False:
      continue
    detailList = getProductDetail(driver, productTitle, eBtn, caseTypeDisplayText, is_colabs, is_preorder)
    if detailList != False:
      prodOptList = prodOptList + detailList
  # transform product data
  transformedProdOpts = Data.transformProdOpt(prodOptList, shope_name, is_preorder)
  transformedProdOpts['imageList'] = prodImgUrlList
  Logger.logSuccess(f'[Finish] Fetching "{productTitle}"')
  return transformedProdOpts
