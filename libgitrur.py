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

#now since this is done now we have to handle the arguements from the command line for this we have to initialize the arguement parser
def setup_parser():
    argparser = argparse.ArgumentParser(description="GitRuR A Version Control system")
    argsubparser = argparser.add_subparsers(title = "Commands",dest="command")
    argsubparser.required = True
    init_parser = argsubparser.add_parser("init",help="To initialize the repository",description="This command is used to initialize the repository")
    init_parser.add_argument("path",help="Specify the folder path",nargs="?",default=".")
    commit_parser = argsubparser.add_parser("commit",help="to commit the changes",description="To commit the changes")
    commit_parser.add_argument("-m",help="Commit message",required=True)
    return argparser


#for default config file this is how it is gonna look like 
def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core","repositoryformatversion","0")
    ret.set("core","filemode","false")
    ret.set("core","bare","false")

    return ret


#this is for creating a new Repo
def create_repo(path):
    #first we will get the repo object 
    repo = git_repo.GitRepository(path,True)

    #now we will check whether the worktree is a valid directory and if it exists or not 
    #here if thedirectory is already existing then what we gotta do is we gotta check if the corresponding git dire is also there and if there is then we have to make sure that it is empty cuz we dont want to overwrite  the existing gitdir
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path}is not a directory!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty") #here it means that the git repo alrready exists so why we are overwriting it with out own repo
    else:
        os.makedirs(repo.worktree)
    
    assert utility.repo_dir(repo,"branches",mkdir=True)
    assert utility.repo_dir(repo,"objects",mkdir=True)
    assert utility.repo_dir(repo,"refs","tags",mkdir=True)
    assert utility.repo_dir(repo,"refs","heads",mkdir=True)

    #open and write a description 
    with open(utility.repo_file(repo,"description"),"w") as f:
        f.write("Unnamed repository; if u want to name this repo u can edit this file. \n")
    
    #open the Head and write something in there 
    with open(utility.repo_file(repo,"HEAD"),"w") as f:
        f.write("ref: refs/heads/master\n")
    
    with open(utility.repo_file(repo,"config"),"w") as f:
        config = repo_default_config()
        config.write(f)



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
    create_repo(arg.path)

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


