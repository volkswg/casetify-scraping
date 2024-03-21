class Logger:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKCYAN = '\033[96m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
    
def logWarn(text):
  print(f"{Logger.WARNING}[WARN] {text}{Logger.ENDC}")

def logDebug(text):
  print(f"{Logger.OKBLUE}[DEBUG] {text}{Logger.ENDC}")

def logError(text):
  print(f"{Logger.FAIL}[ERROR] {text}{Logger.ENDC}")

def logSuccess(text):
  print(f"{Logger.OKGREEN}[SUCCESS] {text}{Logger.ENDC}")
  