import math
from module import Logger, Database

def roundUpHundred(x):
  return int(math.ceil(x / 100.0)) * 100  

def calculateSellingPrice(price, preorder=False, colab=False):
  sellingPrice = price
  try:
    sellingPrice = Database.getSellingPrice(price, colab)
  except:
    multipyFactor = 1.15
    additionalValue = 0
    if preorder == False:
      additionalValue = 300
    if colab == True:
      multipyFactor = 1.60
    sellingPrice = roundUpHundred((price + additionalValue) * multipyFactor) - 1
  # Logger.logDebug(f"price = {price} => {sellingPrice}")
  return sellingPrice