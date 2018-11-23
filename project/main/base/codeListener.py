import inspect

def getCodeLocation():
    ins = inspect.stack()[0]
    file = ins[1]
    lineno = ins[2]
    function = ins[3]
    code = ins[4]
    location = ('NotebookServer' + str(file).split('/NotebookServer')[1], lineno, function + '()', str(code[0]).strip())
    print(location)
    return location

getCodeLocation()