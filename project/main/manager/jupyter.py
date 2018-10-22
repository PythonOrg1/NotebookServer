from config import config
from system import shell

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor



def start():
    shell.execute('jupyter notebook --port ' + config.ns_port + ' --no-browser')


def convertNb(form, nbName):
    if form is None:
        # form = 'HTML'
        shell.execute('jupyter nbconvert ' + nbName)
    else:
        shell.execute('jupyter nbconvert --to ' + form + nbName)


#
#nb -- contains file path
#kernel --- kernel of the system
#
def executingNb(path, nbName, kernel):
    if kernel is None:
        kernel = 'python3'
    runPath = path
    with open(path+'/'+nbName) as f:
        nbook = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel)
    (nbd, res) = ep.preprocess(nbook, {'metadata': {'path': runPath}})



