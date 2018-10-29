
isDebug = True

def log(tag, msg):
    if isDebug:
        try:
            print("LOG: " + tag + " | " + str(msg))
        except Exception as e:
            print('Exception:')
            print(e)

def err(tag, err):
    if isDebug:
        try:
            print("ERROR: " + tag + " | "+ str(err))
        except Exception as e:
            print('Exception:')
            print(e)


def info(tag, msg):
    if isDebug:
        try:
            print("INFO: " + tag + " | "+ str(msg))
        except Exception as e:
            print('Exception:')
            print(e)

