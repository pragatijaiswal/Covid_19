
import subprocess
import os

def get_johns_hopkins():
    ''' Get data by a git pull request, the source code has to be pulled first
        Result is stored in the predifined csv structure
    '''
    if os.path.isdir("data/raw/COVID-19/"):
        git_pull = subprocess.Popen( "git pull origin master" ,
                             cwd = os.path.dirname( 'data/raw/COVID-19/' ),
                             shell = True,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE )
        (out, error) = git_pull.communicate()
    else:
        git_clone = subprocess.Popen( "git clone https://github.com/CSSEGISandData/COVID-19.git" ,
                             cwd = os.path.dirname( 'data/raw/' ),
                             shell = True,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE )
        (out, error) = git_clone.communicate()


    print("Error : " + str(error))
    print("out : " + str(out))
    print("got the data")



    
if __name__ == '__main__':
    get_johns_hopkins()
    pass