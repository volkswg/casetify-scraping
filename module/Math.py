import math
from module import Logger, GlobalVar

def roundUpHundred(x):
  return int(math.ceil(x / 100.0)) * 100  

def calculateSellingPrice(price, preorder=False, colab=False):
  try:
    return GlobalVar.databaseInstance.getSellingPrice(price, colab)
  except:
    multiplyFactor = 1.50 if colab else 1.31
    additionalValue = 0 if preorder else 300
    return roundUpHundred((price + additionalValue) * multiplyFactor) - 1
