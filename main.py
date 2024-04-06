from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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

caseTypeMapper = {
  "Ultra Bounce Case MS": { 
    "isSelected": False, 
    "optValue": "",
    "displayText": "เคส Ultra Bounce รองรับ MagSafe"
  },
  "Bounce Case MS": { 
    "isSelected": False, 
    "optValue": "",
    "displayText": "เคสกันกระแทก Bounce"
  },
  "Pride Impact Case MS": { 
    "isSelected": False,
    "optValue": "",
    "displayText": "เคส MagSafe Pride"
  },
  "Impact Ring Stand Case MS": {
    "isSelected": False,
    "optValue": "MagSafe/RingStand",
    "displayText": "เคส Impact พร้อมห่วงตั้งรองรับ Magsafe"
  },
  "Impact Case MS": {
    "isSelected": True,
    "optValue": "MagSafe/Impact",
    "displayText": "เคสกันกระแทกรองรับ Magsafe"
  },
  "Clear Case MS": {
    "isSelected": True,
    "optValue": "MagSafe/Clear",
    "displayText": "เคสใสรองรับ Magsafe"
  },
  "Mirror Case MS": { 
    "isSelected": True,
    "optValue": "MagSafe/Mirror",
    "displayText": "เคสกระจกรองรับ Magsafe"
  },
  "Leather Case MS": { 
    "isSelected": True,
    "optValue": "MagSafe/Leather",
    "displayText": ""
  },
  "Impact Case": {
    "isSelected": True,
    "optValue": "Impact",
    "displayText": ""
    
  },
  "Impact Ring Stand Case": { 
    "isSelected": False,
    "optValue": "RingStand",
    "displayText": ""
    
  },
  "Clear Case": {
    "isSelected": True,
    "optValue": "Clear",
    "displayText": ""
    
  },
  "Mirror Case": {
    "isSelected": True,
    "optValue": "Mirror",
    "displayText": ""
    
  },
}

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

def getProductDetail(case_type_mapper, is_preorder = False):
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
  [addToCartBtn] = driver.find_elements(By.XPATH, '//div[@action-type="ADD_TO_CART"]')
  SB.scrollToElement(driver, addToCartBtn)
  addToCartBtn.click()
  
  # check cart is ready to copy data 
  SB.findElements(driver, By.XPATH, '//div[contains(@class, "cart-item-container")]/div/div[not(contains(@class, "disable"))]')
  
  priceElem = SB.findElements(driver, By.XPATH, '//div[contains(@class, "cart-item-container")]//div[contains(@class,"item-price")]')
  price = String.convertPriceToInt(priceElem[0].text)
  finalPrice = Math.calculateSellingPrice(price, is_preorder, IS_COLABS)
  
  cartContainer = driver.find_elements(By.XPATH, '//div[contains(@class, "cart-item-container")]//div[contains(@class,"product-info")]')
  productInfoText = String.replaceForbiddenWord(cartContainer[0].text)
  extactedDetail = String.extractProductDetail(productInfoText)
  
  return {
    'title': extactedDetail['productName'],
    'description': 'description',
    'price': finalPrice,
    'caseType': extactedDetail['caseType'],
    'deviceName': extactedDetail['deviceName'],
    'color': extactedDetail['color'],
    'imageSrc': srcUrl
  }
  
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
    # caseTypeBtnList = SB.findElements(driver, By.XPATH, '//div[contains(@class,"with-product-selector")]//div[contains(@class, "product-selector")]//div[contains(@class, "item")]')
    caseTypeBtnList = SB.findElements(driver, By.XPATH, '//div[contains(@class,"with-product-selector")]/div[contains(@class, "product-selector")]//div[@class="item"]')
    prodOptList = []
    caseTypeBtnListLen = caseTypeBtnList.__len__()
    for eBtn in caseTypeBtnList:
      if caseTypeBtnListLen > 1:
        SB.scrollToElement(driver, eBtn)
        eBtn.click()
        [caseTypeDescElem] = SB.findElements(driver, By.XPATH, '//div[@data-label="selected-case-type-name"]/span')
        
        needData = True
        for eKey in list(caseTypeMapper.keys()):
          eCaseType = caseTypeMapper[eKey]

          if eCaseType['displayText'] == caseTypeDescElem.text:
            if eCaseType['isSelected'] == False:
              needData = False
              break
        if needData == False:
          continue
      time.sleep(1)
      detail = getProductDetail(caseTypeMapper, is_preorder)
      if detail != False:
        prodOptList.append(detail)
        # close cart
        cartCollapseBtn = SB.findElements(driver, By.XPATH,'//a[contains(@class, "cart-collapse")]')
        ActionChains(driver).move_to_element_with_offset(cartCollapseBtn[0], -50, 200).perform()
        clickCurrentLocation()
    # transform product data
    transformedProdOpts = Data.transformProdOpt(prodOptList, caseTypeMapper, SHOP_NAME, is_preorder)
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
