
isDebug = False

def log(tag, msg):
    if isDebug:
        print("LOG: " + tag + " | " +msg)

def err(tag, err):
    if isDebug:
        print("ERROR: " + tag + " | " + err)

def info(tag, msg):
    if isDebug:
        print("INFO: " + tag + " | " +msg)
