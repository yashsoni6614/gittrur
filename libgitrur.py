import argparse #this is for parsing the arguements which will be recieved from the commandline
import configparser #this is gonna be used for parsing and structuring the future configurations of my project git 
from datetime import datetime #basic date and time module
try:
    import grp,pwd #since concept of group and user id exists only in the unix based systems we using the try catch here 
except ModuleNotFoundError:
    pass
from fnmatch import fnmatch #this is for easily matching the file type 
import hashlib #for the encryption 
from math  import ceil 
import os #this is for the interaction with the hardware via os (eg for creating the directory and other things)
import re #will be used for regular expressions
import sys #for actually getting the command line arguements 
import zlib #for the compression of the logs


#now since this is done now we have to handle the arguements from the command line for this we have to initialize the arguement parser
def setup_parser():
    argparser = argparse.ArgumentParser(description="GitRuR A Version Control system")
    argsubparser = argparser.add_subparsers(title = "Commands",dest="command")
    argsubparser.required = True
    argsubparser.add_parser("init",help="To initialize the repository",description="This command is used to initialize the repository")
    commit_parser = argsubparser.add_parser("commit",help="to commit the changes",description="To commit the changes")
    commit_parser.add_argument("-m",help="Commit message",required=True)
    return argparser


# Bridge Functions 
def cmd_add(arg):
    print("Logic for: git add")

def cmd_cat_file(arg):
    print("Logic for: git cat-file")

def cmd_check_ignore(arg):
    print("Logic for: git check-ignore")

def cmd_checkout(arg):
    print("Logic for: git checkout")

def cmd_commit(arg):
    print(f"Logic for: git commit with message: {arg.message if hasattr(arg, 'message') else 'No message'}")

def cmd_hash_object(arg):
    print("Logic for: git hash-object")

def cmd_init(arg):
    print("Logic for: git init")

def cmd_log(arg):
    print("Logic for: git log")

def cmd_ls_files(arg):
    print("Logic for: git ls-files")

def cmd_ls_tree(arg):
    print("Logic for: git ls-tree")

def cmd_rev_parse(arg):
    print("Logic for: git rev-parse")

def cmd_rm(arg):
    print("Logic for: git rm")

def cmd_show_ref(arg):
    print("Logic for: git show-ref")

def cmd_status(arg):
    print("Logic for: git status")

def cmd_tag(arg):
    print("Logic for: git tag")

# --- Main Execution ---

def main(argv=sys.argv[1:]):

    parser = setup_parser() # Assuming setup_parser is defined elsewhere
    arg = parser.parse_args(argv)
    
    if not arg.command:
        parser.print_help()
        return

    match arg.command:
        case "add":          cmd_add(arg)
        case "cat-file":     cmd_cat_file(arg)
        case "check-ignore": cmd_check_ignore(arg)
        case "checkout":     cmd_checkout(arg)
        case "commit":       cmd_commit(arg)
        case "hash-object":  cmd_hash_object(arg)
        case "init":         cmd_init(arg)
        case "log":          cmd_log(arg)
        case "ls-files":     cmd_ls_files(arg)
        case "ls-tree":      cmd_ls_tree(arg)
        case "rev-parse":    cmd_rev_parse(arg)
        case "rm":           cmd_rm(arg)
        case "show-ref":     cmd_show_ref(arg)
        case "status":       cmd_status(arg)
        case "tag":          cmd_tag(arg)
        case _:              print("Bad command.")


