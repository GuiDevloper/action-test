import os, sys, requests, geckodriver_autoinstaller, pexpect
from time import sleep
from selenium.webdriver import Keys, ActionChains, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from shutil import rmtree
from pathlib import Path
from pyvirtualdisplay import Display
from getter import doFiles, doCred, doRequest, getTime

geckodriver_autoinstaller.install()

options = Options()
options.add_argument("--lang=en")
options.add_argument("--disable-gpu")
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)
options.set_capability("pageLoadStrategy", "eager")

def clearTemp():
  tempPath = "/tmp/"
  for p in Path(tempPath).glob("rust_mozprofile*"):
    rmtree(p, ignore_errors=False)
  print('cleaned!')

started = False
def start(id, retry = False):
  try:
    child = pexpect.spawn(DATA["cmds"]["up"].replace("{n}", str(id)))
    child.expect([pexpect.TIMEOUT, DATA["expects"]["up"]])
  except:
    return start(id)
  tested = test()
  if not tested:
    print('not started')
    if retry:
      return False
    return start(id, True)
  global started
  started = child
  return True

def close():
  started.close()

def test():
  tested = False
  for _ in range(10):
    try:
      curReal = getReal()
      if curReal != real:
        print(f'.{curReal.split(".")[3]}')
        tested = True
        break
    except: print('bad')
    sleep(1)
  return tested

def prepare(prepares):
  for prepare in prepares:
    pexpect.spawn(prepare, timeout=50).read()

def getReal():
  return requests.get(DATA["rls"]["z"]).text.replace("\n", "")

def genDriver():
  driver = Firefox(options=options)
  driver.set_window_size(800, 800)
  return driver

def runX(driver, i):
  return driver.execute_script(DATA["x1"].replace("{x}", DATA["rls"]["x"][i]))

w = 0
get_errors = 0
def load(driver, i):
  step = f'getting - {getTime()}'
  try:
    driver.get(DATA["rls"]["v2"])
  except:
    print(f'Error: {step}')
    global get_errors
    get_errors += 1
    if get_errors > 1:
      get_errors = 0
      return 'get'
    return True
  runX(driver, i)
  step = 'got!'
  try:
    WebDriverWait(driver, 35).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, DATA["tgs"]["c"]))
    )
    driver.execute_script(DATA["scripts"]["p"])
    step = 'app!'

    driver.execute_script(
      DATA["scripts"]["r"].replace("{tag}", DATA["tgs"]["v"])
    )
    step = 'acc!'

    driver.execute_script(DATA["scripts"]["b"])
    WebDriverWait(driver, 150).until(
      EC.invisibility_of_element_located((By.CSS_SELECTOR, DATA["tgs"]["c"]))
    )
    sleep(2.3)
    driver.execute_script(DATA["scripts"]["p"])

    global w
    w += 1
    print(f'w: {w} - {getTime()}')
    try: doRequest(API, KEY)
    except: print('req error')
    return False
  except:
    print(f'Error: {step}')
    return True

def run_session():
  errors = 0
  i = 0
  while errors < 5:
    driver = genDriver()
    error = load(driver, i)
    driver.quit()
    if error == 'get': return error
    if error: errors += 1
    else: errors = 0
    i += 1
    if i > len(DATA["rls"]["x"]) - 1:
      i = 0

def startDisplay():
  global display
  display = Display(visible=False, size=(800, 800))
  display.start()

print(f'> started - {getTime()}')

try:
  KEY = os.environ["SECRET_KEY"]
  API = os.environ["API"]
except:
  print('404 key')
  sys.exit(1)

DATA = requests.get(f"{API}{KEY}").json()

prepare(DATA["prepares"])
doFiles(DATA["files"], DATA["cmds"]["fname"])
doCred(DATA["cmds"])

real = getReal()
print(real)
startDisplay()
def MAIN():
  for id, _ in enumerate(DATA["files"]):
    started = start(id)
    if not started: break
    error = run_session()
    close()
    clearTemp()
    if error == 'get':
      print('restarting!')
      continue
  display.stop()


MAIN()
print(f'> exited {getTime()}')
