# newsubs
Find new subdomains of different bug bounty programs from Chaos.

<a href="https://www.github.com/heydc7"><img align="center" src="https://raw.githubusercontent.com/heydc7/heydc7/a496f2a26065fc9aa0fac7c60ce0d8e3f432e6eb/images/logo-color.png"/></a>


### Install
```bash
git clone https://github.com/heydc7/newsubs.git
cd newsubs
pip3 install -r requirements.txt
python3 newsubs.py -h
```
### Usage
```bash
newsubs.py [-h] {show,fetch,compare,difference,union}

Find new subdomains

positional arguments:
  {show,fetch,compare,difference,union}
    show                Show program list from Chaos
    fetch               Fetch subdomains from a program
    compare             Compare subdomains of a program
    difference          List uncommon items from files
    union               Combine both files uniquely

options:
  -h, --help            show this help message and exit
```

### Commands
"newsubs" offers several commands to assist in subdomain discovery. Here's an overview of the available commands:

**1. Command Help**
```bash
newsubs.py <command> -h
```

**2. Show**
The show command displays a list of all Bug Bounty programs available on [Chaos](https://chaos.projectdiscovery.io/#/). You can optionally filter the programs using the -g flag and save the output to a file using the -o flag:

```bash
newsubs.py show [-h] [-g GREP] [-o OUTPUT]

options:
  -h, --help     show this help message and exit
  -g, --grep     Filter programs using grep
  -o, --output   Output file name/path
```

For example, to find programs related to Sony, you can use:
```bash
newsubs.py show -g sony
```

**3. Fetch**
The fetch command downloads subdomains associated with a specific Bug Bounty program from [Chaos](https://chaos.projectdiscovery.io/#/). You'll need to provide the index number of the program using the `-i` flag:

```bash
newsubs.py fetch [-h] -i INDEX

options:
  -h, --help      show this help message and exit
  -i, --index     Index number of the program
```

This command will create a new directory for the program within the data/ folder, using the current date as the folder name. It stores the fetched subdomains in this directory.

```bash
newsubs.py fetch -i 608
```

**4. Compare**
The compare command helps you compare different versions of subdomain folders fetched for a program. It identifies and displays new subdomains between two versions:

```bash
newsubs.py compare [-h] -p PROGRAM -f1 FILE1 -f2 FILE2 [-o OUTPUT]

options:
  -h, --help      show this help message and exit
  -p, --program   Name of program
  -f1, --file1    Old folder name/path
  -f2, --file2    New folder name/path
  -o, --output    Output file name/path
```

For example, to compare archived versions of the "Sony" program fetched on different dates:

```bash
newsubs.py compare -p sony -f1 2023-09-25 -f2 2023-09-28
```

**5. Difference**
The difference command is used to find uncommon items (subdomains) between two files:

```bash
newsubs.py difference [-h] -f1 FILE1 -f2 FILE2 [-o OUTPUT]

options:
  -h, --help      show this help message and exit
  -f1, --file1    Old file name/path
  -f2, --file2    New file name/path
  -o, --output    Output file name/path
```

This command can be handy when performing subdomain recon to identify changes between two sets of subdomains.

```bash
newsubs.py difference -f1 amass.txt -f2 subfinder.txt
```

**6. Union**
The union command combines the contents of two files into a single file, retaining unique values:

```bash
newsubs.py union [-h] -f1 FILE1 -f2 FILE2 [-o OUTPUT]

options:
  -h, --help     show this help message and exit
  -f1, --file1   First file name/path
  -f2, --file2   Second file name/path
  -o, --output   Output file name/path
```

This command is useful for merging subdomains obtained from different sources or tools.
```bash
newsubs.py union -f1 amass.txt -f2 subfinder.txt
```



