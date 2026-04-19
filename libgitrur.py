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
import git_repo
import utility
import objects

#now since this is done now we have to handle the arguements from the command line for this we have to initialize the arguement parser
def setup_parser():
    argparser = argparse.ArgumentParser(description="GitRuR A Version Control system")
    argsubparser = argparser.add_subparsers(title = "Commands",dest="command")
    argsubparser.required = True
    init_parser = argsubparser.add_parser("init",help="To initialize the repository",description="This command is used to initialize the repository")
    init_parser.add_argument("path",help="Specify the folder path",nargs="?",default=".")
    commit_parser = argsubparser.add_parser("commit",help="to commit the changes",description="To commit the changes")
    commit_parser.add_argument("-m",help="Commit message",required=True)
    cat_file_parser = argsubparser.add_parser("cat-file",help="Provide content of the repository object")
    #positional arguements 
    cat_file_parser.add_argument("type",metavar="type",choices=["blob","commit","tag","tree"],help="Specify the type")
    cat_file_parser.add_argument("object",metavar="object",help="The object to display")
    hash_object_parser = argsubparser.add_parser("hash-object",help="Computer object ID and optionally creates a blob from a file")
    hash_object_parser.add_argument("-t",metavar="type",dest = "type" , choices=["blob","commit","tree","tag"],default = "blob",help="Specify the type")
    hash_object_parser.add_argument("-w",dest = "write",action="store_true",help="Actually write the object into the database")
    hash_object_parser.add_argument("path",help="Read object from the <file>")
    return argparser


#these are the main functions 
def cmd_add(arg):
    print("Logic for: git add")

def cat_file(repo,obj,fmt = None):
    obj = objects.object_read(repo,objects.object_find(repo,obj,fmt = fmt))
    sys.stdout.buffer.write(obj.serialize())

def cmd_cat_file(arg):
    repo = utility.repo_find()
    cat_file(repo,arg.object,arg.type.encode())

def cmd_check_ignore(arg):
    print("Logic for: git check-ignore")

def cmd_checkout(arg):
    print("Logic for: git checkout")

def cmd_commit(arg):
    print(f"Logic for: git commit with message: {arg.message if hasattr(arg, 'message') else 'No message'}")



def object_hash(fd,fmt,repo=None):
    data = fd.read()

    match fmt:
        case b"commit" : object = objects.GitCommit(data)
        case b"tree"   : object = objects.GitTree(data)
        case b"blob"   : object = objects.GitBlob(data)
        case b"tag"    : object = objects.GitTag(data)
        case _ : raise Exception(f"Unknown Format Specified {fmt}")
    
    sha = objects.object_write(object,repo)
    return sha



def cmd_hash_object(arg):
    if arg.write:
        repo = utility.repo_find()
    else:
        repo = None
    with open(arg.path,"rb") as fd:
       sha =  object_hash(fd,arg.type.encode(),repo)
       print(sha)

def cmd_init(arg):
    utility.create_repo(arg.path)

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


