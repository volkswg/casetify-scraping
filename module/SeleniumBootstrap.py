from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def waitUntilVisible(driver, locator):
  WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
  
def findElements(driver, selector_type, selector_value):
  waitUntilVisible(driver ,(selector_type, selector_value))
  return driver.find_elements(selector_type, selector_value)

def scrollToElement(driver, element):
  ActionChains(driver).scroll_to_element(element).perform()
  