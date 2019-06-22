import time

# Clase ticker
#-------------------------------------------
class Ticker:
    def __init__(self):
        self.start_time = time.time()

    # retorna delta tiempo en segundos
    def __call__(self):
        dt = time.time() - self.start_time
        self.start_time = time.time()
        return dt
#-------------------------------------------

#
def try_match_bytes (digesto, match_bytes):
    for i in range(len(match_bytes)):
        if (digesto[i] != match_bytes[i]):
            return False
    return True

# 
def printHashBinary(digesto, spacer='', breakOn=4):
    hstr = ""
    pos = 0
    for x in digesto:
        pos += 1
        hstr += format(x, '08b') + spacer 
        if breakOn != 0 and pos%breakOn == 0 and pos<(len(digesto)):
          hstr += '\n'

    print('-------- BEGIN HASH BINARY --------')
    print(hstr)
    print('--------- END HASH BINARY ---------')