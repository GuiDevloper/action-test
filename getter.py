import os, requests
from datetime import datetime

def doFiles(files, fname):
  os.makedirs('files', exist_ok=True)
  for id, file in enumerate(files):
    f = open(f'./{fname.replace("{n}", str(id))}', 'w')
    f.write(file)
    f.close()

def doCred(cmds):
  f = open(f"./{cmds['pname']}", 'w')
  f.write(cmds['cred'])
  f.close()

def doRequest(API, KEY):
  requests.post(f'{API}/a/{KEY}', json={'time': str(getTime())})

def getTime():
  return datetime.now().time()