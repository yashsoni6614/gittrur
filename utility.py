import os 
import configparser
#here i am gonna make the class for the repository

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
        cf = repo_file(self,"config")

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


def repo_path(repo,*path):
    #basically for joining the path 
    return os.path.join(repo.gitdir,*path)

#if the mkdir is false and the path exists and this path is not the directory then raise exception otherwise return path
#if the mkdir is true and the path exists and this path is not the directory then raise exception otherwise return path and if the path doesnt exists then make the directory of that path 
def repo_dir(repo,*path,mkdir=False):
    path = repo_path(repo,*path)
    if (os.path.exists(path)):
        if(os.path.isdir(path)):
            return path
        else:
            raise Exception(f"Not a directory {path}")
    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_file(repo,*path,mkdir=False):
    #check if the path one level above exists or not if yes only then return the whole path 
    if repo_dir(repo,*path[:-1],mkdir=mkdir):
        return repo_path(repo,*path)
    else:
        return None


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
    repo = GitRepository(path,True)
    #now we will check whether the worktree is a valid directory and if it exists or not 
    #here if thedirectory is already existing then what we gotta do is we gotta check if the corresponding git dire is also there and if there is then we have to make sure that it is empty cuz we dont want to overwrite  the existing gitdir
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception(f"{path}is not a directory!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            raise Exception(f"{path} is not empty") #here it means that the git repo alrready exists so why we are overwriting it with out own repo
    else:
        os.makedirs(repo.worktree)
    
    assert repo_dir(repo,"branches",mkdir=True)
    assert repo_dir(repo,"objects",mkdir=True)
    assert repo_dir(repo,"refs","tags",mkdir=True)
    assert repo_dir(repo,"refs","heads",mkdir=True)

    #open and write a description 
    with open(repo_file(repo,"description"),"w") as f:
        f.write("Unnamed repository; if u want to name this repo u can edit this file. \n")
    
    #open the Head and write something in there 
    with open(repo_file(repo,"HEAD"),"w") as f:
        f.write("ref: refs/heads/master\n")
    
    with open(repo_file(repo,"config"),"w") as f:
        config = repo_default_config()
        config.write(f)



#Today i will be writing the repo_find() function its job is to find the root directory which means it is gonna find the path where the .git folder is gonnna exist 
#if we are gonna find such of the path then we are gonna return the gitRepo object 

def repo_find(path = ".",required = True):
    path = os.path.realpath(path)

    if(os.path.isdir(os.path.join(path,".git"))):
        return GitRepository(path)
    
    parent = os.path.realpath(os.path.join(path,".."))

    if(parent == path): #this is our edge case which means we have reached the root directory 
        if required:
            raise Exception("No git directory")
        else :
            return None
    
    return repo_find(parent , required)


#here i will be making a commit parser whose job is to parse the keyvaluelist with message type files and parse them into the objects

def kvlm_parse(raw,start = 0,dct=None): #basically we cant pass the dict as the default arguement because on every function calls it is gonna use the same dict which we dont want 
    if dct is None:
        dct = dict()
    
    spc = raw.find(b' ',start)
    nl = raw.find(b'\n',start)
    
    #now we have to identify the base case in here which means the base case will be the case when either no space is found which means that the commit file hit that last blank line without any space below it is the commit message or either the index of the space is greater than the index of the new line 
    if (spc<0) or(nl<spc):
        assert nl == start
        dct[None] = raw[start+1:] #inserting the commit message  and storing it in the None key to avoid any name key conflicts  
        return dct
    
    key = raw[start:spc]

    end = start
    #this thing we are doing in order to handle the pgp signature msg with leading spaces
    while True:
        end = raw.find(b'\n',end+1)
        if raw[end+1] != ord(' ') :
            break
    
    value = raw[spc+1:end].replace(b'\n ',b'\n') #removing the leading spaces in the pgp lines 

    #since there can be duplicate keys we have to handle this part as well 
    if key in dct:
        if type(dct[key]) == list:
            dct[key].append(value)
        else:
            dct[key] = [dct[key],value] #otherwise we make it a list first 
    else :
        dct[key] = value
    
    #now the recursive call 
    return kvlm_parse(raw,start = end+1,dct=dct)
    

#now there is the ned to make the function which will basically write the given object just as the obj_read and the obj_write ones 
def kvlm_serialize(kvlm_dict):
    ret = b'' #we have to initialize the variable nameed ret we will be adding everything here 

    for k in kvlm_dict.keys():
        if k == None : continue #we are not handling the case where there is this 
        val = kvlm_dict[k]
        if type(val) != list:
            val = [val]
        for v in val:
            ret += k + b' ' + (v.replace(b'\n',b' \n')) + b'\n'
        
    ret += b'\n'+kvlm_dict[None]

    return ret

    

