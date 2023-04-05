import os

def execute(n_keys):

    os.system('python keygen.py -n '+ str(n_keys)) 
    os.system('python sign.py -af')
    os.system('python aggSign.py')
    os.system('python aggVerify.py')
