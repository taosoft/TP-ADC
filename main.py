import multiprocessing
from commonfunctions import Ticker, try_match_bytes, printHashBinary, getLetrasBytes, getProcessesQuantity, findCollision, printCollision

if __name__ == '__main__':
  # String de "letras" a colisionar contra uint32
  letras_bytes = getLetrasBytes()

  # Cantidad de procesos a crear
  processesQuantity = getProcessesQuantity()

  # Tiempo total de cómputo
  tickTotal = Ticker()

  # Máx número entero sin signo de 32 bits. Rango de uint32: 0 - 4294967295
  maxValue = 4294967295

  # Array de datos de procesos a crear (minValue, maxValue, letras, arrayP, valueP, process)
  arrayOfProcesses = []

  # Ingresa datos para los procesos a crear
  valorAnterior = 0
  for i in range(processesQuantity):
    arrayOfProcesses.append([valorAnterior, round((maxValue/processesQuantity)*(i+1)), letras_bytes, multiprocessing.Array('I', 6), multiprocessing.Value('d', 0.0)])
    valorAnterior = round((maxValue/processesQuantity)*(i+1))

  # Crea los procesos con sus respectivos datos
  a = arrayOfProcesses
  for i in range(processesQuantity):
    arrayOfProcesses[i].append(multiprocessing.Process(target=findCollision, args=(a[i][0], a[i][1], a[i][2], a[i][3], a[i][4])))

  # Inicia los procesos
  for i in range(processesQuantity):
    arrayOfProcesses[i][5].start()

  # "Analiza" datos pasados por memoria compartida entre procesos
  cantHash = 0
  cantTime = 0.0
  cantProcess = 0
  cantFinalizados = 0
  contador = 0
  contadorInterno = 0
  stopVar = False
  stopVar2 = False
  while stopVar == False:
    for i in range(processesQuantity):
      if (arrayOfProcesses[i][3])[3] == True:        
        cantHash += (arrayOfProcesses[i][3])[0]
        cantTime += arrayOfProcesses[i][4].value
        (arrayOfProcesses[i][3])[3] = False
        cantProcess += 1
      
      if contador == 4000000:
        if (arrayOfProcesses[i][3])[5] == True:
          cantFinalizados += 1
        contadorInterno += 1
        if contadorInterno == processesQuantity:
          contador = 0
      else:        
        contador += 1

      if (arrayOfProcesses[i][3])[1] == True:
        stopVar2 = True
        (arrayOfProcesses[i][3])[1] = False
        printCollision((arrayOfProcesses[i][3])[2], letras_bytes, i + 1)

    if cantFinalizados == processesQuantity:
      stopVar = True
      print("No se encontró ningún hash que colisione con la palabra ingresada")
      print("¡Programa finalizado!")

    if cantProcess == processesQuantity:      
      print("Hashes calculados entre", processesQuantity,"procesos:", cantHash , "- rate:", round(cantTime, 1), "hash/s")  
      cantProcess = 0
      cantTime = 0.0
      if stopVar2 :
        stopVar = True

  # Carga el valor de referencia para terminar el proceso (en la memoria compartida)
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