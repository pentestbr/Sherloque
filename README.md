# Sherloque - a custom password list crafter

Sherloque is a **python3** script for **generating target-specific password lists**. This tool should be used only after having tried the usual common wordlists such as "rockyou.txt" or "SecLists/common.txt" and if you have **a good knowledge of the target**.

Sherloque has been released under the famous beerware license so feel free to use it however you like.

This tool has been named after the eponymous character from the TV show "The Flash", who can be seen as the french cheap version of Sherlock Holmes.

## Requirements

**Python3** should be installed on your computer. Do not try to run this program with Python2.7 or it won't be fully functional.
Python3 can be downloaded from this source [https://www.python.org/downloads/](https://www.python.org/downloads/).

## Basic Usage

Sherloque allows the user to specify general information about a specific target. Once all the information has been filled in, the list of passwords can be generated. 

```bash
$ ./sherloque.py -h
usage: ./sherloque.py [-h] [-v] [-j JSON] [-o OUTPUT] [-e EXPORT]

Sherloque is a tool for generating target-specific password lists.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -j JSON, --json JSON  Import a json file containing information about the
                        target.
  -o OUTPUT, --output OUTPUT
                        Output file for the generated password list.
  -e EXPORT, --export EXPORT
                        Export target information as a json file when
                        generating the wordlist (for future reuse).
```

Target information are stored as a json object within the application. It is possible to **import a json file** in order to avoid re-entering all details manually each time you use it.
Target information can also be exported from within the application, using the **export** option.

If no output file is specified, the password list will be **printed on the standard output**.

The provided json file **example.json** can be used to give an overview of the generated password lists. It should be imported as follows:

```bash
$ ./sherloque.py -j example.json
```

## Interactive menu

The main menu is divided into several topics related with the target. It is possible to browse to a topic by entering its index.
Once inside a topic, each field can be modified by entering its index and attributing it a new value.

![Sherloque demo](https://raw.githubusercontent.com/BoiteAKlou/Sherloque/master/data/screenshots/demo.gif)


## TODO

The following improvements are in the pipeline and will be implemented soon:
* Adapt the list according the target's security awareness.
* Support multiple values in fields like "Kid's name".
* Add common password prefixes to the existing wordlist.
* Add trivial alpha-numerical combinations to the existing wordlist.
* Adapt the wordlist according to the targeted service (e.g. PIN number).

## Feedback and contributions

Any feedback is highly appreciated and motivating :). Also, feel free to contact me if you wish to contribute to this tool!
