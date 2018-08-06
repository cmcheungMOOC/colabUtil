# -*- coding: utf-8 -*-
"""colabUtil.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KX9x-rqyj0XfUkLtfOVh8t8T_kW0hs0u

#Colab Util
This is a collection of utility functions that simplifies data science researchin using colab.  I wrote this while working through *Deep Learning with Python* by Francisco Chollet.

Most of creatPyDrive is from https://gist.github.com/rdinse/159f5d77f13d03e0183cb8f7154b170a

##Usage
###Pull in py files into colab.  The content will be in colabUtil folder.
```python
!pip install -U -q PyDrive
!git clone https://github.com/cmcheungMOOC/colabUtil.git
  ```
###Add colab directory to module path
```python
import sys
sys.path.insert(0, '/content/colabUtil')
```
###Share and enjoy!
```python
import colabUtil as cu
cu.setupGlove()
cu.setupAclImdb()
cu.setupKaggleCatsAndDogs()
cu.restore('CNN_Results')
cu.save('CNN_Results')
```

##Assumptions
I have made the following assumptions to allow me to simplify my code.  This code is not meant for general usage.
*   Colab VMs are reliable
*   Colab VMs will be recycled

These assumptions simply means that you can count on the VM to do work correctly while it is still assigned to you, but the VM will be yanked from under you.  So, it is necessary to backup intermediate state information to persistent storage such as a Google drive.

The transient nature of you Colab work space means that there is little reason for complicated directory hierarchies.  After all, anything you built up will vanish overnight.  This means that a simple directory hierarchy supporting the tasks at hand is all you need.

##Directory Hierarchy
Colab workspace is rooted at /content.  This is our defaull directory.  In addition, we use /content/dataset to store downloaded datasets.  Intermediate states of a ML algorithm is written onto /content.  All top level content /content can be zipped up and saved.  The content can be restored when needed.  Note that only the latest state persists in the Google drive.  Unfortuately, I know of no easy way to get the title of a Jupyter notebook. So, a user defined name need to be chosen for the backup zip file.

## Utility Functions
"""

#@title Download Dataset
import requests, os

def download(url, overwrite=False):    
  baseName = os.path.basename(url)
  path = os.path.join(os.getcwd(), baseName)
  print('Downloading', url, 'to', path)
  
  if os.path.isfile(path):
    if not overwrite:
      print(path, 'already exists')
      return path
  
  r = requests.get(url, allow_redirects=True)
  open(path, 'wb').write(r.content)
  return path

#@title Test Download { run: "auto", vertical-output: true }
url = "" #@param ["", "http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz", "http://nlp.stanford.edu/data/glove.6B.zip"]
overwrite = False #@param {type:"boolean"}

if url != "":
  download(url, overwrite)
  os.listdir()

"""###Untar Dataset into Current Working Directory
Currently, untar only support *.tar.gz.  This will be extended only if there is a real use case.
"""

import tarfile, os, shutil

def untar(gzName, dstDir='', skipIfDstDirExists=False):  
  if dstDir == '':
    dstDir = os.path.dirname(gzName)
    if dstDir == '':
      dstDir = os.getcwd()
    
  if skipIfDstDirExists and os.path.isdir(dstDir):
    print(dstDir, 'exists')
    return dstDir  
    
  print('Extracting', gzName, 'to', dstDir)

  t = tarfile.open(name=gzName, mode='r:gz')
  #topLevelDirInTar = os.path.commonprefix(t.getnames())
  #print('topLevelDirInTar', topLevelDirInTar)  
  t.extractall(dstDir)
  return dstDir

#@title Test Untar { run: "auto", vertical-output: true }
gzName = "" #@param ["", "aclImdb_v1.tar.gz"]
dstDir = "" #@param ["", ".", "/content/dataset"]

if  gzName != "":
  d = untar(gzName, dstDir)
  print(d)
  print(os.listdir(d))

#@title Zip Up Content of a Specified Directory
import zipfile, os

def zip(srcDir='.', mode='w'):
  print('zip', srcDir, mode)
  if not os.path.isdir(srcDir):
    print(srcDir, 'is not a dir')
    return None
  
  if srcDir == '.':
    srcDir = os.getcwd()

  zipName = srcDir + '.zip'
  print('Creating', zipName, 'from', srcDir)
  
  with zipfile.ZipFile(zipName, mode=mode) as zf:
    compression = zipfile.ZIP_DEFLATED
    for fname in os.listdir(srcDir):
      if os.path.isdir(fname):
        print('Skipping', fname)
        continue
        
      _, ext = os.path.splitext(fname)
      if ext.lower() in ['.zip', '.gz']:
        print('Skipping', fname)
        continue
        
      path = os.path.join(srcDir, fname)
      zf.write(path, compress_type=compression)
      print(path, 'is added to', zipName)
      
  return zipName

#@title Test Zip { run: "auto" }
srcDir = "" #@param ["", ".", "/content", "/content/datalab"]

if srcDir != '':
  if not os.path.isdir(srcDir):
    os.mkdir(srcDir)
  print(zip(srcDir))

#@title Unzip Content
import os, zipfile, shutil

def unzip(zipName, dstDir = '', skipIfDstDirExists=False):  
  if dstDir == '':
    dstDir = os.path.dirname(zipName)
    
  if skipIfDstDirExists and os.path.isdir(dstDir):
    print(dstDir, 'exists')
    return dstDir
    
  print('Extracting', zipName, 'to', dstDir)
  
  z = zipfile.ZipFile(zipName, 'r')
  z.extractall(dstDir)
  return dstDir

#@title Test Unzip { run: "auto", vertical-output: true }
zipName = "" #@param ["", "glove.6B.zip", "/content/datalab.zip"]
dstDir = "" #@param ["", ".", "/content/dataset/glove.6B", "/content/dataset", "datalab", "a/b", "dataset/tmp"]

if  zipName != "":
  d = unzip(zipName, dstDir)
  print(d)
  print(os.listdir(d))
  os.listdir(d)

#@title Setup GLOVE
def setupGlove():
  zipFile = download('http://nlp.stanford.edu/data/glove.6B.zip')
  unzip(zipFile, dstDir='/content/dataset/glove.6B', skipIfDstDirExists=True)

#@title Test GLOVE Setup { run: "auto", vertical-output: true }
test = False #@param {type:"boolean"}

if test:
  setupGlove()

#@title Setup ACLIMDB
def setupAclImdb():
  gzFile = download('http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz')
  untar(gzFile, dstDir='/content/dataset/aclImdb_v1', skipIfDstDirExists=True)

#@title Test ACLIMDB Setup { run: "auto", vertical-output: true }
test = False #@param {type:"boolean"}

if test:
  setupAclImdb()

#@title Setup Kaggle Cats and Dogs
def setupKaggleCatsAndDogs():
  zipFile = download('https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_3367a.zip')
  unzip(zipFile, dstDir='/content/dataset/kagglecatsanddogs_3367a',
        skipIfDstDirExists=True)

#@title Test Kaggle Cats and Dogs Setup { run: "auto", vertical-output: true }
test = False #@param {type:"boolean"}

if test:
  setupKaggleCatsAndDogs()

"""##Pydrive Utilities
https://gsuitedevs.github.io/PyDrive/docs/build/html/index.html

Content of a specified directory is saved to or restored from a Google drive.

Most of creatPyDrive is from https://gist.github.com/rdinse/159f5d77f13d03e0183cb8f7154b170a
"""

#@title Authenticate and Create the PyDrive Client
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

def createPyDrive():
  print('createPyDrive')
  mycreds_file = 'mycreds_file.json'
  gauth = GoogleAuth()
  
  # https://stackoverflow.com/a/24542604/5096199
  # Try to load saved client credentials
  gauth.LoadCredentialsFile(mycreds_file)
  if gauth.credentials is None:
    # Authenticate if they're not there
    auth.authenticate_user()
    gauth.credentials = GoogleCredentials.get_application_default()
    print(gauth.credentials)
  elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
  else:
    # Initialize the saved creds
    gauth.Authorize()
  # Save the current credentials to a file
  gauth.SaveCredentialsFile(mycreds_file)
  return GoogleDrive(gauth)

#@title Test CreatePyDrive { run: "auto", vertical-output: true }
test = False #@param {type:"boolean"}
if test:
  drive = createPyDrive()
  os.listdir()

#@title Create & Upload a File
def uploadFile(drive, fname):
  print('uploadFile', fname)
  uploaded = drive.CreateFile({'title': fname})
  uploaded.SetContentFile(fname)
  uploaded.Upload()
  print('Uploaded {} with ID {}'.format(fname, uploaded.get('id')))

#@title Test UploadFile to Google Drive { run: "auto", vertical-output: true }
fname = "" #@param ["", "a.txt"]

if fname != '':
  if not os.path.exists(fname):
    print('Creating', fname)
    with open(fname, 'w') as fp:
      fp.write('abc')
  uploadFile(drive, fname)

#@title Find a File by Name in the Google Drive
def findFile(drive, fname):
  file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
  for file1 in file_list:
    if file1['title'] == fname:
      print('title: %s, id: %s' % (file1['title'], file1['id']))
      return file1

#@title Test Find File in Google Drive { run: "auto", vertical-output: true }
fname = "" #@param ["", "a.txt"]

if fname != '':
  findFile(drive, fname)

#@title Download a File and Optionally Trash it
def downloadFile(drive, fname, trashIt=False):
  print('downloadFile', fname)
  file1 = findFile(drive, fname)
  if not file1:
    print(fname, 'not found')
    return None
  
  downloaded = drive.CreateFile({'id': file1['id']})
  downloaded.GetContentFile(fname)
  
  if trashIt:
    downloaded.Trash()
    print(fname, 'is moved to trash')
    
  return file1['title']

#@title Test Download from Google Drive { run: "auto", vertical-output: true }
fname = "" #@param ["", "a.txt"]
trashIt = False #@param {type:"boolean"}

if fname != '':
  print(downloadFile(drive, fname, trashIt))

#@title Google Drive Class
class GDrive:
  def __init__(self):
    self.drive = createPyDrive()
    
  def upload(self, fname):
    uploadFile(self.drive, fname)
    
  def download(self, fname, trashIt=True):
    return downloadFile(self.drive, fname, trashIt)

#@title Test Google Drive Class { run: "auto", vertical-output: true }
fname = "" #@param ["", "a.txt"]

if fname != '':
  if not os.path.exists(fname):
    with open(fname, 'w') as fp:
      fp.write('abc')
  gd = GDrive()
  gd.upload(fname)
  gd.download(fname)

"""###Save and Restore the Content of a Directory"""

#@title Save Directory to Google Drive
def save(srcDirName):
  if '/' in srcDirName:
    print('Use only the name of the dir, not the path to it')
    return

  zipName = zip(srcDirName)
  gd = GDrive()
  gd.upload(zipName)

#@title Test Directory Save { run: "auto", vertical-output: true }
srcDirName = "" #@param ["", "datalab", "/content/datalab"]

if srcDirName != '':
  if not os.path.isdir(srcDirName):
    os.mkdir(srcDirName)
    
  path = os.path.join(srcDirName, 'abc.txt')
  if not os.path.exists(path):
    with open(path, 'w') as fp:
      fp.write('abc')
  save(srcDirName)

#@title Restore Directory from Google Drive
import os

def restore(dstDirName):
  if '/' in srcDirName:
    print('Use only the name of the dir, not the path to it')
    return  
  
  if os.path.isdir(dstDirName):
    print(dstDirName, 'already exists')
    return
  
  zipName = dstDirName + '.zip'
  gd = GDrive()
  zf = gd.download(zipName)
  unzip(zf, '.')

#@title Test Restore Directory { run: "auto", vertical-output: true }
dstDirName = "" #@param ["", "datalab"]

import shutil

if dstDirName != '':
  if os.path.isdir(dstDirName):
    print('rmtree', dstDirName)
    shutil.rmtree(dstDirName)
  restore(dstDirName)
  print(os.listdir(dstDirName))