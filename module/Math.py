import math

def roundUpHundred(x):
  return int(math.ceil(x / 100.0)) * 100  

def calculateSellingPrice(price, collab=False, preorder=False):
  multipyFactor = 1.15
  additionalValue = 0
  if preorder == False:
    additionalValue = 300
  if collab == True:
    multipyFactor = 1.60
  sellingPrice = roundUpHundred((price + additionalValue) * multipyFactor) - 1
  return sellingPrice