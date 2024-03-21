from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton

from module import Logger, String, Math, File, Excel, ShopeeTemplate, Data

import time

PRODUCT_LINK_FILENAME = "productUrlList.txt"
TEMPLATE_FILENAME = 'shopee_simple_template_2Usneaker.xlsx'

def clickCurrentLocation():
  action = ActionBuilder(driver)
  action.pointer_action.pointer_down(MouseButton.LEFT)
  action.pointer_action.pointer_up(MouseButton.LEFT)
  action.perform()

def waitUntilVisible(locator):
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))

def findElement(selector_type, selector_value):
  waitUntilVisible((selector_type, selector_value))
  return driver.find_elements(selector_type, selector_value)

def acceptCookies():
  acceptCookiesBtn = findElement(By.CLASS_NAME, "button-container")
  if acceptCookiesBtn.__len__() == 1:
    Logger.logSuccess('Accepted Cookies')
    acceptCookiesBtn[0].click()
  else:
    Logger.logError('Accept Cookies Button Not Found')

def closeSignUpIframe():
  [signUpIframe] = findElement(By.ID, "cms-popup-iframe")
  driver.switch_to.frame(signUpIframe)
  iframeCloseBtn = driver.find_element(By.CLASS_NAME, 'close')
  iframeCloseBtn.click()
  driver.switch_to.default_content()
  Logger.logSuccess('Closed Sign Up Popup')

def getProductDetail():
  Logger.logDebug('Get Product detail')
  # check item is not available
  waitListContainer = driver.find_elements(By.XPATH, '//div[contains(@class, "waitlist-form-container")]')
  isWaitingList = waitListContainer.__len__() > 0
  if isWaitingList == True:
    return False
  # download case type image
  productImageContainer = findElement(By.XPATH, '//div[contains(@class, "slider-container")]/div[@class="view-port"]/div/img')
  imageContanerLen = productImageContainer.__len__()
  
  if imageContanerLen < 1 :
    Logger.logError('Something Error on fetch option image')
    
  srcUrl = productImageContainer[0].get_attribute('src')
  srcUrl = String.removeExtraFileExt(srcUrl)
  
  addToCartBtn = driver.find_elements(By.XPATH, '//div[@id="PRODUCT_ACTION"]/div[contains(@class, "product-action-btn-container")]/button[contains(@class, "shopping-cart-button")]')
  ActionChains(driver).scroll_to_element(addToCartBtn[0]).perform()
  addToCartBtn[0].click()
  
  # check cart is ready to copy data 
  findElement(By.XPATH, '//div[contains(@class, "cart-item-container")]/div/div[not(contains(@class, "disable"))]')
  
  priceElem = findElement(By.XPATH, '//div[contains(@class, "cart-item-container")]//div[contains(@class,"item-price")]')
  price = String.convertPriceToInt(priceElem[0].text)
  finalPrice = Math.calculateSellingPrice(price)
  
  cartContainer = driver.find_elements(By.XPATH, '//div[contains(@class, "cart-item-container")]//div[contains(@class,"product-info")]')
  productInfoText = String.replaceForbiddenWord(cartContainer[0].text)
  extactedDetail = String.extractProductDetail(productInfoText)
  
  return {
    'title': f"CASETiFY | {extactedDetail['productName']}",
    'description': productInfoText,
    'price': finalPrice,
    'caseType': extactedDetail['caseType'],
    'deviceName': extactedDetail['deviceName'],
    'color': extactedDetail['color'],
    'imageSrc': srcUrl
  }

def getProductData(url, first_time_popup):
    driver.get(url)
    if first_time_popup == True:
      acceptCookies()
      closeSignUpIframe()
    productImageContainer = findElement(By.XPATH, '//div[contains(@class, "slider-container")]/div[@class="view-port"]/div/img')
    imageContanerLen = productImageContainer.__len__()
    
    Logger.logDebug("productImageContainer length: " + str(imageContanerLen))
    if imageContanerLen < 1 :
      Logger.logError('Something Error on fetch image')
      print(productImageContainer)
      
    # createDirIfNotExsit("Case/" + product_name)

    print('[Start] Download image main product image')
    prodImgUrlList = []
    for imageElem in productImageContainer:
      srcUrl = imageElem.get_attribute('src')
      srcUrl = String.removeExtraFileExt(srcUrl)
      prodImgUrlList.append(srcUrl)
    print('[End] Download Cover image')
    
    # get all product option
    caseTypeBtnList = findElement(By.XPATH, '//div[contains(@class, "case-type")]/div[contains(@class, "row")]/div/div')
    prodOptList = []
    for eBtn in caseTypeBtnList:
      ActionChains(driver).scroll_to_element(eBtn).perform()
      eBtn.click()
      time.sleep(1)
      detail = getProductDetail()
      if detail != False:
        prodOptList.append(detail)
        # close cart
        cartCollapseBtn = findElement(By.XPATH,'//a[contains(@class, "cart-collapse")]')
        ActionChains(driver).move_to_element_with_offset(cartCollapseBtn[0], -50, 200).perform()
        clickCurrentLocation()
    # transform product data
    transformedProdOpts = Data.transformProdOpt(prodOptList)
    transformedProdOpts['imageList'] = prodImgUrlList
    Logger.logDebug(transformedProdOpts)
    return transformedProdOpts

if __name__ == "__main__":
  productList = []
  prodUrlList = File.readFile(PRODUCT_LINK_FILENAME)
  driver = webdriver.Chrome()

  for idx, e_link_path in enumerate(prodUrlList):
    productDetail = getProductData(e_link_path, idx == 0)
    productList.append(productDetail)
  
  # Logger.logDebug(productList)
  
  newMassUploadFile = ShopeeTemplate.generateNewSimpleMassUploadFile(TEMPLATE_FILENAME)
  Excel.editExcelfile(newMassUploadFile, productList)
  
