#here i am gonna make the class for the repository
import os
import configparser
import utility
class GitRepository (object) :
    #it is a git repository which will structure the git thing 
    worktree = None #this is for the main directory 
    gitdir = None #this is for the git directory inside the main directory
    conf = None #this is the main configuration file 

    def __init__(self,path,force = False):
        self.worktree = path #this is gonna specify the path of the main directory 
        self.gitdir = os.path.join(path,".git") #this will be the path of the git directory 

#firstly we have to make sure that the git folder actually exist when the force is false 
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git Repository {path}")
        self.conf = configparser.ConfigParser()

#now after this check we gotta handle the config file in there        
        cf = utility.repo_file(self,"config")

#if the path to the config file exists only it can parse the config file otherwise raise thee exception 
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Config file is missing")

#it is to check if the repository format version is 0 or not it will only work for the version 0
        if not force:
            vers = int(self.conf.get("core","repositoryformatversion"))
            if vers != 0:
                raise Exception(f"The repository format is not supported : {vers}")


        



