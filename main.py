from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.keys import Keys

from module import Logger, String, Math, File, Excel, ShopeeTemplate, Data, Database, SeleniumBootstrap as SB

import time
import inquirer

PRODUCT_LINK_FILENAME = "productUrlList.txt"
IS_COLABS = False
NEED_LOGIN = False
SHOP_NAME = ''

def clickCurrentLocation():
  action = ActionBuilder(driver)
  action.pointer_action.pointer_down(MouseButton.LEFT)
  action.pointer_action.pointer_up(MouseButton.LEFT)
  action.perform()

def acceptCookies():
  acceptCookiesBtn = SB.findElements(driver, By.XPATH, "//div[contains(@class, 'cookie-option')]//div[contains(@class, 'button-container')]")
  if acceptCookiesBtn.__len__() == 1:
    Logger.logSuccess('Accepted Cookies')
    acceptCookiesBtn[0].click()
  else:
    Logger.logError('Accept Cookies Button Not Found')

def closeSignUpIframe():
  [signUpIframe] = SB.findElements(driver, By.ID, "cms-popup-iframe")
  driver.switch_to.frame(signUpIframe)
  iframeCloseBtn = driver.find_element(By.CLASS_NAME, 'close')
  iframeCloseBtn.click()
  driver.switch_to.default_content()
  Logger.logSuccess('Closed Sign Up Popup')

def getProductDetail(case_type_btn, case_type_display_txt, is_preorder = False):
  Logger.logDebug('Get Product detail')
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
  titleElem = driver.find_elements(By.XPATH, '//div[@data-label="artwork-name"]//span')
  productTitle = titleElem[0].get_attribute('innerHTML')
  
  priceElem = case_type_btn.find_element(By.XPATH, './/div[@data-label="case-type-item-price"]')
  price = String.convertPriceToInt(priceElem.text)
  finalPrice = Math.calculateSellingPrice(price, is_preorder, IS_COLABS)
  
  # fetch color
  colorItems = SB.findElements(driver, By.XPATH, '//ul[@class="items-container color"]//div[contains(@class, "item")]')
  
  productDetailList = []
  if len(colorItems) > 1:
    for eColorBtn in colorItems:
      SB.scrollToElement(driver, eColorBtn)
      if 'active' not in eColorBtn.get_attribute('class'):
        eColorBtn.click()
        
      colorDidplayTextElem = driver.find_element(By.XPATH, '//div[@data-label="selected-color-name"]')
      colorInfo = Database.getColorInfo(case_type_display_txt, colorDidplayTextElem.text)
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
          'caseType': f"{Database.getCaseTypeOptName(case_type_display_txt)}",
          'caseColor': f"{colorInfo['optValue']}",
          'imageSrc': srcUrl
        })
  else:
    productDetailList.append({
      'title': productTitle,
      'description': 'description',
      'price': finalPrice,
      'caseType': Database.getCaseTypeOptName(case_type_display_txt),
      'caseColor': f"{colorInfo['optValue']}",
      'imageSrc': srcUrl
    })
  
  return productDetailList
  
def LoginFunction(username, password):
  driver.get('https://www.casetify.com/sign_up_page')
  signInBtn = SB.findElements(driver, By.XPATH,'//a[contains(@class, "action-link")]')
  signInBtn[1].click()
  SB.findElements(driver, By.ID,'log-in-email')[0].send_keys(username)
  SB.findElements(driver, By.ID,'log-in-password')[0].send_keys(password)
  SB.findElements(driver, By.ID,'log-in-password')[0].send_keys(Keys.ENTER)
  time.sleep(10)
  driver.get('https://casetifycolab.page.link/doraemon')
  time.sleep(5)

def clickCaseType(driver, element):
  retryLimit = 5
  retryCount = 0
  while retryCount < retryLimit:
    try:
      Logger.logDebug(f"loop {retryCount}")
      SB.scrollToElement(driver, element)
      element.click()
      return
    except:
      retryCount += 1
  raise Exception("Error Retry Exceed")

def getProductData(url, first_time_popup, is_preorder = False):
    driver.get(url)
    if first_time_popup == True:
      acceptCookies()
      closeSignUpIframe()
    productImageContainer = SB.findElements(driver, By.XPATH, '//div[contains(@class, "slider-container")]/div[contains(@class,"view-port")]/div/img')
    imageContanerLen = productImageContainer.__len__()
    
    if imageContanerLen < 1 :
      Logger.logError('Something Error on fetch image')
      print(productImageContainer)

    print('[Start] Download image main product image')
    prodImgUrlList = []
    for imageElem in productImageContainer:
      srcUrl = imageElem.get_attribute('src')
      srcUrl = String.removeExtraFileExt(srcUrl)
      prodImgUrlList.append(srcUrl)
    print('[End] Download Cover image')
    
    # get all product option
    caseTypeBtnList = SB.findElements(driver, By.XPATH, '//div[contains(@class,"with-product-selector")]/div[contains(@class, "product-selector")]//div[@class="item"]')
    prodOptList = []
    caseTypeBtnListLen = caseTypeBtnList.__len__()
    for eBtn in caseTypeBtnList:
      if caseTypeBtnListLen > 1:
        clickCaseType(driver, eBtn)
      [caseTypeDisplayTextElem] = SB.findElements(driver, By.XPATH, '//div[@data-label="selected-case-type-name"]/span')
      caseTypeDisplayText = caseTypeDisplayTextElem.text
      isRequiredCaseType = Database.isRequireCaseType(caseTypeDisplayText)
      if isRequiredCaseType == False:
        continue
      detailList = getProductDetail(eBtn, caseTypeDisplayText, is_preorder)
      if detailList != False:
        prodOptList = prodOptList + detailList
    # transform product data
    transformedProdOpts = Data.transformProdOpt(prodOptList, SHOP_NAME, is_preorder)
    transformedProdOpts['imageList'] = prodImgUrlList
    return transformedProdOpts

if __name__ == "__main__":
  productList = []
  prodUrlList = File.readFile(PRODUCT_LINK_FILENAME)

  questions = [
    inquirer.List('shopName',
      message="Which Shop do you want?",
      choices=Database.getShopList(),
    ),
    inquirer.Confirm("isColab", message="Is This Co-Labs?", default=True),
    inquirer.Confirm('needLogin', message="Is this session need login?", default=False)
  ]
  answers = inquirer.prompt(questions)
  
  SHOP_NAME = answers["shopName"]
  IS_COLABS = answers['isColab']
  NEED_LOGIN = answers['needLogin']
  driver = webdriver.Chrome()
  
  if NEED_LOGIN == True:
    LoginFunction('passakorn.s@icloud.com','Passakorn2')

  for idx, e_link_path in enumerate(prodUrlList):
    productDetail = getProductData(e_link_path, idx == 0)
    productList.append(productDetail)
  
  newMassUploadFile = ShopeeTemplate.generateNewSimpleMassUploadFile(SHOP_NAME)
  Excel.editExcelfile(newMassUploadFile, productList)
