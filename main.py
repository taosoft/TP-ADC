from multiprocessing import Pool
import time
import numpy as np
import struct
import hashlib

from commonfunctions import Ticker, try_match_bytes, printHashBinary

letras = "MA"
letras_bytes = letras.encode('ascii')
# Tiempos de intervalos internos
internalTick = Ticker()
# Tiempos totales
tickTotal = Ticker()

# Intervalo de reporte cada 
interval= 348692 # hashes

# Crear un numero entero sin signo de 32 bits.
# Rango de uint32: 0 - 4294967295
# hagan la prueba de colocar el valor máximo para ver los bytes
n = np.uint32(0)
exitFlag = False
n2 = 0
while (n <= 4294967295 and exitFlag == False):
  # Extraer bytes, los guarda en b
  b = struct.pack('I', n)

  h = hashlib.sha256()
  h.update(b)
  digesto = h.digest()
  exitFlag = try_match_bytes(digesto, letras_bytes)
  if (exitFlag):
    print("EXITO!!!!!!!!")
    print("Hash SHA256(", n,") = ", end='')
    for i in range(len(letras_bytes)):
        print(chr(digesto[i]), end='') 
    print("...")
    printHashBinary(digesto, ' ')
      
  if (n % interval == 0):
    di = internalTick()
    dn = n - n2
    print("Hashes calculados:", n, " rate: ", round(dn/di, 1), " h/s")  
    n2 = n
  n+=1

# final imprime sumario
d = tickTotal()
print("Tiempo requerido para computar ", n, " hashes fue de: ", round(d, 2), " segundos")
print("Hash rate: ", round(n/d, 1), " hashes/seg")
print("Tiempo estimado en el cual se alcance el maximo rango del nonce entero de 32 bits")
print( round((4294967295 / (n/d))/3600, 2), " horas")