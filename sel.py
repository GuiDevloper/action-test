import os, sys, geckodriver_autoinstaller, requests, pexpect
from time import sleep
from datetime import datetime
from selenium.webdriver import Keys, ActionChains, Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from shutil import rmtree
from pathlib import Path
from threading import Thread
from pyvirtualdisplay import Display
from getter import doFiles, doCred

geckodriver_autoinstaller.install()

options = Options()
options.add_argument('--lang=en')
options.add_argument('--disable-gpu')
options.set_preference("browser.cache.disk.enable", False)
options.set_preference("browser.cache.memory.enable", False)
options.set_preference("browser.cache.offline.enable", False)
options.set_preference("network.http.use-cache", False)

def prepare(prepares):
  for prepare in prepares:
    pexpect.spawn(prepare, timeout=50).read()

def clearTemp():
  tempPath = "/tmp/"
  for p in Path(tempPath).glob("rust_mozprofile*"):
    rmtree(p, ignore_errors=False)
  print('cleaned!')

def start(id):
  try:
    child = pexpect.spawn(DATA['cmds']['up'].replace('{n}', str(id))) 
    child.expect([pexpect.TIMEOUT, DATA['expects']['up']])
  except:
    return start(id)
  tested = test()
  if not tested:
    close(child)
    return False
  return child

def close(started):
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

def getReal():
  return requests.get(DATA['rls']['z']).text.replace('\n', '')

def genDriver():
  driver = Firefox(options=options)
  driver.set_window_size(800, 800)
  return driver

def resetBrowser(driver):
  try:
    driver.delete_all_cookies()
    driver.execute_script('window.localStorage.clear()')
  except: False

def readyState(driver):
  return driver.execute_script("return (document.readyState == 'complete')")

def keepP(driver):
  driver.execute_script(DATA['scripts']['b'])

w = 0
def load(driver, v):
  step = f'getting - {datetime.now().time()}'
  try:
    driver.get(f'{DATA["rls"]["v"]}{v}')
    resetBrowser(driver)
    WebDriverWait(driver, 45).until(readyState)
    step = 'got!'
    WebDriverWait(driver, 35).until(
      EC.visibility_of_element_located((By.CSS_SELECTOR, DATA['tgs']['c']))
    )
    step = 'app!'

    keepP(driver)
    driver.execute_script(
      DATA['scripts']['r'].replace('{tag}', DATA['tgs']['v'])
    )
    step = f'acc! - {datetime.now().time()}'
    WebDriverWait(driver, 400).until(
      EC.invisibility_of_element_located((By.CSS_SELECTOR, DATA['tgs']['c']))
    )
    global w
    w += 1
    print(f'w: {w} - {datetime.now().time()}')
    sleep(1)
    resetBrowser(driver)
    return False
  except:
    resetBrowser(driver)
    print(step)
    return True

global_errors = 0
def run_session(i2):
  driver = genDriver()
  errors = 0
  for i in range(100):
    hasError = load(driver, DATA['rand'][i2])
    if hasError: errors += 1
    else: errors = 0

    if errors > 15:
      global global_errors
      global_errors += 1
      break
  driver.quit()

def startDisplay():
  global display
  display = Display(visible=False, size=(800, 800))
  display.start()

print(f'> started - {datetime.now().time()}')

try:
  KEY = os.environ['SECRET_KEY']
  API = os.environ['API']
  CHOICE = os.environ['CHOICE']
except:
  print('404 key')
  sys.exit(1)

print(CHOICE)

DATA = requests.get(f'{API}{CHOICE}/{KEY}').json()

prepare(DATA['prepares'])
doFiles(DATA['files'], DATA['cmds']['fname'])
doCred(DATA['cmds'])

def errored_globally():
  global global_errors
  return global_errors > 10 or global_errors >= len(DATA['order'])

real = getReal()
print(real)
def MAIN():
  startDisplay()
  for i1 in range(len(DATA['order'])):
    print(f'> {i1 + 1}')
    started = start(DATA['order'][i1])
    if not started: continue

    run_session(0)
    clearTemp()
    close(started)

    if errored_globally():
      print('nomore!')
      requests.get(f'{API}next/{CHOICE}/{KEY}')
      break
  display.stop()


MAIN()
if not errored_globally():
  requests.get(f'{API}new/{CHOICE}/{KEY}')
print(f'> exited {datetime.now().time()}')
