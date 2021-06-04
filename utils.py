#!/usr/bin/env python3.5

import subprocess
import getpass
import traceback
import re
try:
    import configparser
except ImportError as e: 
    print(e)
    print('configparser not installed! Please run pip3.5 install configparser --user')
    exit(1)

try:
    import jira.client
    JIRA_IMPORTED = True
except ImportError as e:
    print(e)
    JIRA_IMPORTED = False

def stage_area_dirty():
    return len(run_cmd(['git', 'status', '--porcelain']).strip()) != 0

def green(string):
    return '\x1b[0;32;40m' + string + '\x1b[0m'    

def red(string):
    return '\x1b[0;31;40m' + string + '\x1b[0m'    

def yellow(string):
    return '\x1b[0;33;40m' + string + '\x1b[0m'    

def print_exception(e = None):
    print("\n\n" + red("=== EXCEPTION ==="))
    if not e is None:
        print(e)
    else:
        traceback.print_exc()
    print(red("=== END EXCEPTION ==="))

def get_pc_username():
    return run_shell_cmd("echo $USER").strip()

def run_cmd(cmd):
    if isinstance(cmd, list):
        return subprocess.check_output(cmd).decode()
    else:
        return subprocess.check_output(cmd.split(" ")).decode()

def call_cmd(cmd):
    if not isinstance(cmd, list):
        cmd = cmd.split(" ")
    print_string = yellow("RUN COMMAND -- ")  + ' '.join(cmd) + yellow(" --")

    print(print_string)
    return subprocess.call(cmd) == 0
        

def run_shell_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode()


def ask(message):
    message = message if message[-1:] == " " else message + " "
    return input(message)

def ask_yes_no(message, default = True): 
    defstring = "(y/n): " +  ("[y] " if default else "[n] ")
    message = message + defstring if message[-1:] == " " else message + " " + defstring
    answer = ask(message).lower()
    if answer in ['y', 'n']: 
        return answer == 'y'
    elif len(answer) == 0:
        return default
    else:
        return ask_yes_no(message,default)

def ask_not_empty(message):
    res = ask(message)
    if res is None or res == "":
        print("Cannot be empty")
        return ask_not_empty(message)
    return res

def get_current_branch():
    return run_cmd("git rev-parse --abbrev-ref HEAD").replace("\n", "")

def extract_jira_issue_ids(string): 
    return re.findall("[A-Z]{1,}-[0-9]{1,}", string)    

def load_properties(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    return config
