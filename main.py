from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.common.keys import Keys

from module import Logger, File, Excel, ShopeeTemplate, ScrapModule, Database, SeleniumBootstrap as SB

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

  driver.get("https://www.casetify.com/")
  acceptCookies()
  closeSignUpIframe()

  for idx, e_link_path in enumerate(prodUrlList):
    productDetail = ScrapModule.getCaseDataFromUrl(driver,e_link_path, SHOP_NAME, IS_COLABS, 'apple')
    Logger.logDebug(productDetail)
    productList.append(productDetail)
  
  newMassUploadFile = ShopeeTemplate.generateNewSimpleMassUploadFile(SHOP_NAME)
  Excel.editExcelfile(newMassUploadFile, productList)
