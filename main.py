import sys
import getopt
import urllib3

# INIT
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
argumentList = sys.argv[1:]
file1 = []
file2 = []
outputFile = ""

def loadFile(file):
  try:
    with open(file) as f:
      lines = [line.rstrip('\n') for line in f]
      return lines
  except:
    print("Error: the file "+ file + " does not exist.")

def convertResult(result):
  return str(result) + '\n'

def writeFile(file, result):
  try:
    f = open(file,"w")
    f.writelines(list(map(convertResult, result)))
    f.close()
    print("\nResults saved: " + file)
  except:
    print("Error: unable to save results in "+ file)

def helpMenu():
  print("""
  Usage: newsubs [-f] <file> [-s] <file> [-o] <filename>
  -h: Help
  -f --first: First File
  -s --second: Second File
  -o --output: Output file name/path
  """)

def findNew(f1, f2):
  result = []
  for i in f2:
    if(i not in f1):
      result.append(i)
  return result

def showResult(result):
  for i in result:
    print(i)
    
try:
  opts, args = getopt.getopt(argumentList,"f:s:o:",["first=", "second=","output="])

  for opt, arg in opts:
    if opt == '-h':
      helpMenu()
      sys.exit()
    elif opt in ("-f","--first"):
      file1 = loadFile(arg)
    elif opt in ("-s","--second"):
      file2 = loadFile(arg)
    elif opt in ("-o", "--output"):
      outputFile = arg

  outputResult = findNew(file1, file2)
  showResult(outputResult)
  if(outputFile != ""):
    writeFile(outputFile, outputResult)
  
except getopt.GetoptError:
  helpMenu()
  sys.exit(2)