#now i have to deal with the objects i will be makning the abstract base class for the interface 
import os
import utility
import zlib
import hashlib
class GitObject(object) :
    def __init__(self,data = None):
        if not (data == None):
            self.deserialize(data)
        else:
            self.init()
    
    def serialize(self): #these are purely virtual functions whose implementation will be done in the subclassses
        raise Exception("Unimplemented function")
    
    def deserialize(self,data):
        raise Exception("Unimplemnted")
    
    def init():
        pass #just an empty object 


#read object function for reading the files and returning the corresponding 

class GitBlob(GitObject):                                                   
    fmt = b'blob'                                              
                                                    
    def serialize(self):      
        return self.blobdata                        

    def deserialize(self,data):    
        self.blobdata = data

class GitTree(GitObject):
    fmt = b'Tree'
    def serialize(): {}
    def deserialize() :{}



class GitCommit(GitObject):
    fmt = b'Tree'
    def serialize(): {}
    def deserialize() :{}



class GitTag(GitObject):
    fmt = b'Tree'
    def serialize(): {}
    def deserialize() :{}



def object_find(repo,name,fmt = None , follow = True):
    return name

def object_read(repo,sha):
    #we havd to serialize this thing in here 
    path = utility.repo_file(repo,"objects",sha[0:2],sha[2:]) #finding the path of the file from the sha value 
    if not os.path.isfile(path) :
        return None
    
    with open(path , "rb") as f:
        raw = zlib.decompress(f.read()) #this gonna decompress the provided data
        #the header of every type of object file looks like this objTypeSPACEBARCONTENTSIZENULLTERMINATORCONTENT
        x = raw.find(b' ') 
        fmt = raw[0:x]

        #now reading the size
        y = raw.find(b'\x00',x) #this is searching for the appearance of the null terminator 
        size = int(raw[x:y].decode("ascii"))
        if size != len(raw) -(y+1):
            raise Exception(f"Malformed object {sha}: bad length")

        #now the main work of picking up the constructor is there 
        match fmt:
            case b'commit' : c= GitCommit
            case b'tree'   : c = GitTree
            case b'tag'    : c = GitTag
            case b'blob'   : c = GitBlob
            case _:
                raise Exception (f"Unknown Type {fmt.decode("ascii")} for the object")
        
        #here the object is being created
        return c(raw[y+1:])


def object_write(obj , repo = None):

    data = obj.serialize()

    #adding the header
    result = obj.fmt + b' ' + str(len(data)).encode() +b'\x00' + data

    #now we have to compute the hash of the data 
    sha = hashlib.sha1(result).hexdigest()

    if repo:
        path = utility.repo_file(repo,"objects",sha[0:2],sha[2:],mkdir = True)
        if not os.path.exists(path):
            with open(path,"wb") as f:
                f.write(zlib.compress(result))
    
    return sha





