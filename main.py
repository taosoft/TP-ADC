import multiprocessing
from commonfunctions import Ticker, try_match_bytes, printHashBinary, getLetrasBytes, getProcessesQuantity, findCollision, printCollision

if __name__ == '__main__':
  # String de "letras" a colisionar contra uint32
  letras_bytes = "UAD"#getLetrasBytes()
  letras_bytes = letras_bytes.encode('ascii') #borrar
  # Cantidad de procesos a crear
  processesQuantity = 2#getProcessesQuantity()

  # Tiempo total de cómputo
  tickTotal = Ticker()

  # Máx número entero sin signo de 32 bits. Rango de uint32: 0 - 4294967295
  maxValue = 4294967295

  # Array de datos de procesos a crear (minValue, maxValue, letras, arrayP, valueP, process )
  arrayOfProcesses = []

  # Ingresa datos para los procesos a crear
  valorAnterior = 0
  for i in range(processesQuantity):
    arrayOfProcesses.append([valorAnterior, round((maxValue/processesQuantity)*(i+1)), letras_bytes, multiprocessing.Array('I', 5), multiprocessing.Value('i', 0)])
    valorAnterior = round((maxValue/processesQuantity)*(i+1))

  # Crea los procesos con sus respectivos datos
  a = arrayOfProcesses
  for i in range(processesQuantity):
    arrayOfProcesses[i].append(multiprocessing.Process(target=findCollision, args=(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4])))

  # Inicia los procesos
  for i in range(processesQuantity):
    arrayOfProcesses[i][5].start()

  # "Analiza" datos pasados por memoria compartida entre procesos
  internalTick = Ticker()
  cantHash = 0
  cant = 0
  n2 = 0
  stopVar = False
  while stopVar is False:
    for i in range(processesQuantity):
      if (arrayOfProcesses[i][3])[3] == 1:        
        cantHash += (arrayOfProcesses[i][3])[0]
        (arrayOfProcesses[i][3])[3] = 0
        cant += 1

      if (arrayOfProcesses[i][3])[1] == True:
        stopVar = True        
        printCollision((arrayOfProcesses[i][3])[2],letras_bytes)

    if cant == processesQuantity:
      di = internalTick()
      dn = cantHash - n2
      cant = 0
      print("HASHES CALCULADOS:", cantHash , " rate: ", round(dn/di, 1), " hash/s")  
      n2 = cantHash

  for i in range(processesQuantity):
    (arrayOfProcesses[i][3])[4] = True

  # Tiempo total de trabajo
  d = tickTotal()

  # Espera que finalicen los procesos creados
  for i in range(processesQuantity):
    arrayOfProcesses[i][5].join()

  print("Tiempo requerido para computar ", cantHash, " hashes fue de: ", round(d, 2), " segundos")
  print("Hash rate: ", round(cantHash/d, 1), " hashes/seg")

  print("Tiempo estimado en el cual se alcance el maximo rango del nonce entero de 32 bits")
  print( round((4294967295 / (cantHash/d))/3600, 2), " horas")