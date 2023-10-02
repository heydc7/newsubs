import os
import sys
import argparse
import requests
from datetime import date
from program import Program
from zipfile import ZipFile

source = "https://chaos-data.projectdiscovery.io/index.json"

argumentList = sys.argv[1:]
today = date.today()
programs = []

def loadFile(file):
    subdomains = set()
    with open(file, 'r') as file:
        for line in file:
            subdomain = line.strip()
            subdomains.add(subdomain)
    return subdomains

def convertResult(result):
    return str(result) + "\n"

def printResult(result):
    for line in result:
        print(line)

def writeCompareFile(program, file, result):
    try:
        newPath = 'data/' + program + '/results'
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        f = open(newPath + '/' + str(today) + '-' + file, "w")
        f.writelines(list(map(convertResult, result)))
        f.close()
        print("\nResults saved: " + file)
    except Exception as e:
        print("Error: unable to save results in " + file + "\n Error: " + e)

def writeFile(file, result):
    try:
        newPath = 'data/' + program + '/results'
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        f = open(newPath + '/' + str(today) + '-' + file, "w")
        f.writelines(list(map(convertResult, result)))
        f.close()
        print("\nResults saved: " + file)
    except Exception as e:
        print("Error: unable to save results in " + file + "\n Error: " + e)

def downloadFile(url, path):
  try:
    req = requests.get(url)
    filename = path + '/' + str(date.today()) + '.zip'
    with open(filename, 'wb') as output_file:
      output_file.write(req.content)
    return filename
  except Exception as e:
    print(e)
    print(f"Failed to download: {url}")

def unZip(path, file):
    try:
        newPath = path + '/' + str(date.today())
        if not os.path.exists(newPath):
            os.makedirs(newPath)
        with ZipFile(file, 'r') as zip:
            zip.extractall(newPath)
        os.remove(file)
    except Exception as e:
        print("Failed to extract: " + newPath + "\n Error: " + e)

def fetchChaos():
    data = requests.get(source).json()
    for d in data:
        programs.append(Program.from_json(d))

def showPrograms(outputFile=None):
    for i in range(len(programs)):
        print(str(i) + ". " + programs[i].name)
    if outputFile != None:
        writeFile(outputFile, programs)

def compareProgram(name, date1, date2, outputFile=None):
    outputResult = set()
    path1 = 'data/' + name + '/' + date1
    path2 = 'data/' + name + '/' + date2
    if os.path.exists(path1) and os.path.exists(path2):
        dir1 = os.listdir(path1)
        dir2 = os.listdir(path2)
        for d in dir2:
            if d in dir1:
                sub1 = loadFile(path1 + '/' + d)
                sub2 = loadFile(path2 + '/' + d)
                newsubs = sub2 - sub1
                outputResult.update(newsubs)
            else:
                newsubs = loadFile(path2 + '/' + d)
                outputResult.update(newsubs)
        printResult(outputResult)
        if outputFile != None:
            writeCompareFile(name, outputFile, outputResult)
    else:
        print("Error: Directories doesn't exist.")

def findDifference(path1, path2, outputFile=None):
    file1 = loadFile(path1)
    file2 = loadFile(path2)

    diff1 = file1 - file2
    diff2 = file2 - file1

    diff = diff1.union(diff2)
    printResult(diff)
    if outputFile != None:
        writeFile(outputFile, diff)

def unite(path1, path2, outputFile=None):
    file1 = loadFile(path1)
    file2 = loadFile(path2)

    uni = file1.union(file2)
    printResult(uni)
    if outputFile != None:
        writeFile(outputFile, uni)

def fetchSubdomains(index):
    program = programs[index]
    newPath = 'data/' + program.name.lower()
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    filename = downloadFile(program.URL, newPath)
    unZip(newPath, filename)

def main():
    # FETCH PROGRAM LIST FROM CHAOS
    fetchChaos()

    # PARSE
    parser = argparse.ArgumentParser(description="Find new subdomains")
    subparser = parser.add_subparsers(dest='command')
    
    # SECTIONS
    show = subparser.add_parser('show', help='Show program list from Chaos')
    fetch = subparser.add_parser('fetch', help='Fetch subdomains from a program')
    compare = subparser.add_parser('compare', help='Compare subdomains of a program')
    diff = subparser.add_parser('difference', help='List uncommon items from files')
    uni = subparser.add_parser('union', help='Combine both files uniquely')

    # COMPARE
    compare.add_argument('-p', '--program', type=str, required=True, help='Name of program')
    compare.add_argument('-f1', '--file1', type=str, required=True, help='Old folder name/path')
    compare.add_argument('-f2', '--file2', type=str, required=True, help='New folder name/path')
    compare.add_argument('-o', '--output', type=str, help='Output file name/path')
    
    # DIFFERENCE
    diff.add_argument('-f1', '--file1', type=str, required=True, help='Old file name/path')
    diff.add_argument('-f2', '--file2', type=str, required=True, help='New file name/path')
    diff.add_argument('-o', '--output', type=str, help='Output file name/path')

    # UNION
    uni.add_argument('-f1', '--file1', type=str, required=True, help='First file name/path')
    uni.add_argument('-f2', '--file2', type=str, required=True, help='Second file name/path')
    uni.add_argument('-o', '--output', type=str, help='Output file name/path')

    # SHOW PARSER
    show.add_argument('-o', '--output', type=str, help='Output file name/path')

    # FETCH PARSE
    fetch.add_argument('-i', '--index', type=int, required=True, help='Index number of the program')

    args = parser.parse_args()

    match args.command:
        case 'show':
            showPrograms(args.output)
        case 'fetch':
            fetchSubdomains(args.index)
        case 'compare':
            compareProgram(args.program, args.file1, args.file2, args.output)
        case 'difference':
            findDifference(args.file1, args.file2, args.output)
        case 'union':
            unite(args.file1, args.file2, args.output)
        case default:
            print("Error: Recheck your command")

if __name__ == "__main__":
    main()
