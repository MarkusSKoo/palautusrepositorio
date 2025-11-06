# tehdään alussa importit

from logger import logger
from summa import summa
from erotus import erotus

logger("aloitetaan ohjelma") # muutos mainissa

x = int(input("luku 1: "))
y = int(input("luku 2: "))
print(f"{summa(x, y)}") # muutos mainissa
print(f"{erotus(x, y)}") # muutos mainissa

logger("lopetetaan ohjelma")
<<<<<<< HEAD
=======
print("goodbye!") # lisäys bugikorjaus-branchissa
>>>>>>> bugikorjaus
