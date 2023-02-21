import os
import sys
import time
import getopt
import urllib3
import requests
import shutil
from datetime import date
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

# INIT
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
argumentList = sys.argv[1:]
today = date.today()
file1 = []
file2 = []
outputFile = ""
newFiles = []
outputResult = []
#programs = ["https://chaos-data.projectdiscovery.io/4chan.zip", "https://chaos-data.projectdiscovery.io/84codes.zip", "https://chaos-data.projectdiscovery.io/8x8.zip", "https://chaos-data.projectdiscovery.io/aax.zip"]

def loadFile(file):
  try:
    with open(file) as f:
      lines = [line.rstrip('\n') for line in f]
      return lines
  except:
    print("Error: the file " + file + " does not exist.")


def convertResult(result):
  return str(result) + '\n'


def writeFile(file, result):
  try:
    f = open(file, "w")
    f.writelines(list(map(convertResult, result)))
    f.close()
    print("\nResults saved: " + file)
  except:
    print("Error: unable to save results in " + file)


def helpMenu():
  print("""
  Usage: newsubs [-f] <file> [-s] <file> [-o] <filename>
  -h: Help
  -c: Compare data(Format: -c date1:date2)
  -f: First File
  -s: Second File
  -u: Update chaos
  -o: Output file name/path
  """)

def findNew(f1, f2):
  result = []
  for i in f2:
    if (i not in f1):
      result.append(i)
  return result

def showResult(result):
  for i in result:
    print(i)

def downloadFile(url, path):
  try:
    req = requests.get(url)
    filename = path + '/' + url.split('/')[-1]
    with open(filename, 'wb') as output_file:
      output_file.write(req.content)
  except Exception as e:
    print(e)
    print(f"Failed to download: {url}")

def unZip(path):
  entries = os.listdir(path + '/')
  for entry in entries:
    try:
      file = path + '/' + entry
      with ZipFile(file, 'r') as zip:
        zip.extractall(path)
      os.remove(file)
    except Exception as e:
      print("Failed to extract: " + entry + "\n Error" + e)
  print("Extraction Completed")
  
def updateChaos():
  programs = loadFile("programs.txt")
  path = f"data/{today}"
  if os.path.exists(path):
    shutil.rmtree(path)
  os.mkdir(path)
  print("Downloading New Data")
  for p in programs:
    downloadFile(p, path)
    time.sleep(3)
  print("Download Completed")
  unZip(path)

def compare(arr1, arr2):
  for i in arr2:
    if i not in arr1:
      print(i)
      outputResult.append(i)
  
def findNewSubs(d1, d2):
  dir1 = f'data/{d1}'
  dir2 = f'data/{d2}'
  if os.path.isdir(dir1) and os.path.isdir(dir2):
    files1 = os.listdir(dir1 + '/')
    files2 = os.listdir(dir2 + '/')
    for i in files2:
      if i in files1:
        oldSubs = loadFile(f"{dir1}/{i}")
        newSubs = loadFile(f"{dir2}/{i}")
        compare(oldSubs, newSubs)
      else:
        newFiles.append(f"{dir2}/{i}")
  else:
    print("Directory not found!")
    return   

try:
  opts, args = getopt.getopt(argumentList, "c:f:h:s:u:o:")
  for opt, arg in opts:
    if opt in ['-h']:
      helpMenu()
      sys.exit()
    elif opt in ['-u']:
      updateChaos()
    elif opt in ['-c']:
      if ':' not in arg:
        helpMenu()
        sys.exit(2)
      dates = arg.split(':')
      findNewSubs(dates[0], dates[1])
    elif opt in ['-f']:
      file1 = loadFile(arg)
    elif opt in ['-s']:
      file2 = loadFile(arg)
      outputResult = findNew(file1, file2)
      showResult(outputResult)
    elif opt in ['-o']:
      outputFile = arg

  if (outputFile != ""):
    writeFile(outputFile, outputResult)

except getopt.GetoptError:
  helpMenu()
  sys.exit(2)
