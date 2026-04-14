import os 

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
