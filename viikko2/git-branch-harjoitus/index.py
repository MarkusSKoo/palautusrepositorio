# tehdään alussa importit

from logger import logger
from summa import summa
from erotus import erotus
from tulo import tulo

logger("aloitetaan ohjelma") # muutos mainissa

x = int(input("luku 1: "))
y = int(input("luku 2: "))

print(f"{summa(x, y)}") # muutos bugikorjaus-branchissa
print(f"{erotus(x, y)}") # muutos bugikorjaus-branchissa
print(f"{x} * {y} = {tulo(x, y)}") 

logger("lopetetaan ohjelma")
print("goodbye!") # lisäys bugikorjaus-branchissa

