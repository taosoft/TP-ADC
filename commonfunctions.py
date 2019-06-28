import time
import numpy as np
import struct
import hashlib

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

# Prueba matchear los bytes del digesto contra las letras a colisionar
def try_match_bytes (digesto, match_bytes):
    for i in range(len(match_bytes)):
        if (digesto[i] != match_bytes[i]):
            return False
    return True

# Imprime el Hash en binario
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

# Retorna el string ingresado para probar colisión
def getLetrasBytes():
    while True:
        letras = input("Ingrese un string de máx 32 caracteres: ")
        if len(letras) <= 32:            
            # ascii -> 1 byte (8 bits)
            return letras.encode('ascii')
        print("Ingrese menos de 32 caracteres!") 

# Retorna la cantidad de procesos a crear
def getProcessesQuantity():
    while True:
        cantidadProcesos = input("Ingrese la cantidad de procesos con la que desea calcular: ")
        try:
            val = int(cantidadProcesos)
            if (val < 0 or val > 8):
                return 1
            return val
        except ValueError:
            print("Ingrese un número SIN caracteres")

# (minValue, maxValue, letras, arrayMemoriaCompartida[6], valorMemoriaCompartida)
# -arrayMemoriaCompartida (CantHashPorIntervalo, HayColisionConHashLetras, n, IntervaloFinalizado, TerminarProceso, ProcesoTerminado)
# -valueMemoriaCompartida -> hash/s
def findCollision(minValue, maxValue, letras_bytes, arrayP, valueP):
    # Tiempos de intervalos internos
    internalTick = Ticker()
    # Intervalo de reporte cada X hashes
    interval= 348692
    
    n = np.uint32(minValue)
    if n == 0:
        n = 1
    exitFlag = False
    n2 = minValue

    arrayP[0] = 0
    arrayP[1] = False
    arrayP[3] = False
    arrayP[4] = False
    arrayP[5] = False

    while (n <= maxValue and exitFlag == False):
        # Extrae bytes de n y los guarda en b
        b = struct.pack('I', n)

        h = hashlib.sha256()
        h.update(b)
        digesto = h.digest()
        exitFlag = try_match_bytes(digesto, letras_bytes)
        if (exitFlag):
            arrayP[1] = exitFlag       
            arrayP[2] = n
            arrayP[4] = exitFlag        
        
        if (n % interval == 0):
            if arrayP[4] == True:
                exitFlag = True    
            di = internalTick()            
            dn = n - n2
            valueP.value = dn/di
            arrayP[0] = (n - n2)
            arrayP[3] = True
            n2 = n
        n+=1

    if exitFlag == False:
        arrayP[5] = True
        
# Imprime el hash encontrado por colisión
def printCollision(n, letras_bytes, numProcess):
    b = struct.pack('I', n)

    h = hashlib.sha256()
    h.update(b)
    digesto = h.digest()

    print("¡Exito! Colisión de letras contra hash en el proceso #", numProcess)
    print("Hash SHA256(", n,") = ", end='')
    for i in range(len(letras_bytes)):
        print(chr(digesto[i]), end='')
    print("...")
    printHashBinary(digesto, ' ')