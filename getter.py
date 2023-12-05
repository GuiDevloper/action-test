import os

def doFiles(files, fname):
  os.makedirs('files', exist_ok=True)
  for id, file in enumerate(files):
    f = open(f'./{fname.replace("{id}", str(id))}', 'w')
    f.write(file)
    f.close()

def doCred(cmds):
  f = open(f"./{cmds['pname']}", 'w')
  f.write(cmds['cred'])
  f.close()