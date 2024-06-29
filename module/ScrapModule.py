from module import Logger, String, Data, Math, SeleniumBootstrap as SB, GlobalVar
from selenium.webdriver.common.by import By
import time

def checkNewCaseTypeReady(driver):
  isImageLoaded = False
  while isImageLoaded == False:
    Logger.logDebug("loading image...")
    imageElems = SB.findElements(driver, By.XPATH, '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img')
    imageLoadedComplate = imageElems[0].get_attribute('complete')
    if imageLoadedComplate == 'true':
      isImageLoaded = True

def getProductTitle(driver):
  titleElem = driver.find_elements(By.XPATH, '//div[@data-label="artwork-name"]//span')
  productTitle = titleElem[0].get_attribute('innerHTML')
  return productTitle

def selectDeviceBrand(driver, brand = 'Apple'):
    # waiting for device dropdown rendered
  SB.findElements(driver,By.XPATH, '//div[contains(@class, "device-resolver-drop-down-container")]')
  deviceBrandSelectorElem = SB.findElements(driver, By.XPATH, '//div[contains(@class, "brand-drop-down-container")]', is_waiting=False)
  if deviceBrandSelectorElem.__len__() < 1:
    Logger.logWarn('This product only has 1 brand')
  else:
    # select device brand
    deviceBrandSelectorElem = deviceBrandSelectorElem[0]
    deviceBrandSelectorElem.click()
    
    [optionElem] = SB.findElements(driver, By.XPATH, f"//div[contains(@class, \"brand-drop-down-container\")]//option[text()[contains(., \"{brand}\")]]")
    optionElem.click()

def getProductDetail(driver, product_title, case_type_btn, case_type_display_txt, is_colabs, is_preorder = False):
  # check item is not available
  waitListContainer = driver.find_elements(By.XPATH, '//div[contains(@class, "waitlist-form-container")]')
  isWaitingList = waitListContainer.__len__() > 0
  if isWaitingList == True:
    return False
  # download case type image
  productImageContainer = SB.findElements(driver, By.XPATH, '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img')
  imageContanerLen = productImageContainer.__len__()
  
  if imageContanerLen < 1 :
    Logger.logError('Something Error on fetch option image')
    
  srcUrl = productImageContainer[0].get_attribute('src')
  srcUrl = String.removeExtraFileExt(srcUrl)
  
  # addToCartBtn = driver.find_elements(By.XPATH, '//div[@id="PRODUCT_ACTION"]/div[contains(@class, "product-action-btn-container")]/button[contains(@class, "shopping-cart-button")]')
  
  # fetch product title here
  productTitle = product_title
  
  priceElem = case_type_btn.find_element(By.XPATH, './/div[@data-label="case-type-item-price"]')
  price = String.convertPriceToInt(priceElem.text)
  finalPrice = Math.calculateSellingPrice(price, is_preorder, is_colabs)
  
  # fetch color
  colorItems = SB.findElements(driver, By.XPATH, '//ul[@class="items-container color"]//div[contains(@class, "item")]')
  
  productDetailList = []
  if len(colorItems) > 1:
    for eColorBtn in colorItems:
      SB.scrollToElement(driver, eColorBtn)
      # if 'active' not in eColorBtn.get_attribute('class'):
      eColorBtn.click()
        
      colorDidplayTextElem = driver.find_element(By.XPATH, '//div[@data-label="selected-color-name"]')
      colorInfo = GlobalVar.databaseInstance.getColorInfo(case_type_display_txt, colorDidplayTextElem.text)
      # Logger.logDebug(colorInfo != False)
      if colorInfo != False:
        
        # fetch image =====
        productImageContainer = SB.findElements(driver, By.XPATH, '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img')
        imageContanerLen = productImageContainer.__len__()
        
        if imageContanerLen < 1 :
          Logger.logError('Something Error on fetch option image')
          
        srcUrl = productImageContainer[0].get_attribute('src')
        srcUrl = String.removeExtraFileExt(srcUrl)
        # fetch image =====
        # Logger.logDebug(colorInfo['optValue'])
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
  retryLimit = 5
  retryCount = 0
  while retryCount < retryLimit:
    try:
      SB.scrollToElement(driver, element)
      element.click()
      return
    except:
      retryCount += 1
  raise Exception("Error Retry Exceed")

def getCaseTypeDisplayText(driver):
  [caseTypeDisplayTextElem] = SB.findElements(driver, By.XPATH, '//div[@data-label="selected-case-type-name"]/span')
  return caseTypeDisplayTextElem.text

def getCoverImage(driver): 
  Logger.logDebug('getCoverImage called')
  productImageContainer = SB.findElements(driver, By.XPATH, '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img')
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
  # Logger.logDebug(prodCoverImgUrlList)
  return prodCoverImgUrlList
    
def getCaseDataFromUrl(driver, url, shope_name, is_colabs, is_preorder = False, brand = 'Samsung'):
  driver.get(url)
  
  productTitle = getProductTitle(driver)
  Logger.logDebug(f'[Start] Fetching "{productTitle}"')
  
  # waiting for device dropdown rendered
  selectDeviceBrand(driver, brand)
  prodImgUrlList = getCoverImage(driver)
  
  # get all product option
  caseTypeBtnList = SB.findElements(driver, By.XPATH, '//div[contains(@class,"with-product-selector")]/div[contains(@class, "product-selector")]//div[@class="item"]')
  prodOptList = []
  caseTypeBtnListLen = caseTypeBtnList.__len__()
  for eBtn in caseTypeBtnList:
    if caseTypeBtnListLen > 1:
      clickCaseType(driver, eBtn)
      checkNewCaseTypeReady(driver)
    caseTypeDisplayText = getCaseTypeDisplayText(driver)
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
  