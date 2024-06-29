import math
from module import Logger, GlobalVar

def roundUpHundred(x):
  return int(math.ceil(x / 100.0)) * 100  

def calculateSellingPrice(price, preorder=False, colab=False):
  sellingPrice = price
  try:
    sellingPrice = GlobalVar.databaseInstance.getSellingPrice(price, colab)
  except:
    multipyFactor = 1.31
    additionalValue = 0
    if preorder == False:
      additionalValue = 300
    if colab == True:
      multipyFactor = 1.50
    sellingPrice = roundUpHundred((price + additionalValue) * multipyFactor) - 1
  # Logger.logDebug(f"price = {price} => {sellingPrice}")
  return sellingPrice