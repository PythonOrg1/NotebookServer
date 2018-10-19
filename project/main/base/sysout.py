
isDebug = True

def log(tag, msg):
    if isDebug:
        print("LOG: " + tag + " | " + str(msg))

def err(tag, err):
    if isDebug:
        print("ERROR: " + tag + " | "+ str(err))

def info(tag, msg):
    if isDebug:
        print("INFO: " + tag + " | "+ str(msg))
