import os



print("CADU TA SOLTO!!!!!!!")


print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
i = input("s")            
with open("usu.txt","r",encoding="utf-8") as ca:
    p = ca.readline()
    print(p)
    
    
    


