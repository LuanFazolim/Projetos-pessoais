import os
 
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
            


total = list()
corda = list()
cont = 0

with open("usu.txt","r",encoding="utf-8") as usu:
    for o in usu:
        ler = usu.readline().strip()
        cont+=1
        while cont <= 2:
            corda.append(ler)
        else:
            total.append(corda[:])
            cont = 0
            
            
        
        print(o)
        
import os

    

    




    

print(f"Corda: {corda[:]}")
print("\n")
print(f"Total: {total[:]}")
i = input("")