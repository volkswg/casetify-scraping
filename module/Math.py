import math
from module import Logger

def roundUpHundred(x):
  return int(math.ceil(x / 100.0)) * 100  

def calculateSellingPrice(price, preorder=False, collab=False):
  priceMapper = {
    'collab':{
      '2099': 3150,
      '2299': 3250
    },
    'normal':{
      '2099': 2799,
      '2299': 2899
    }
  }
  collabText = 'collab'
  if collab == False:
    collabText = 'normal'

  sellingPrice = price
  try:
    sellingPrice = priceMapper[collabText][f"{price}"]
  except:
    multipyFactor = 1.15
    additionalValue = 0
    if preorder == False:
      additionalValue = 300
    if collab == True:
      multipyFactor = 1.60
    sellingPrice = roundUpHundred((price + additionalValue) * multipyFactor) - 1
  # Logger.logDebug(f"price = {price} => {sellingPrice}")
  return sellingPrice