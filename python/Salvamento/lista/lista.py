import os
# Diretório que você deseja definir como o novo diretório de trabalho
novo_diretorio = "E:\Python luan\python\Salvamento\lista"

# Alterar o diretório de trabalho
os.chdir(novo_diretorio)





 
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
            


total = list()
corda = list()
cont = 0



with open("usu.txt","a") as esc:
    nome = input("nome: ")
    senha = input("senha: ")
    abr = esc.write(f"\n{nome}\n\n{senha}\n")

with open("usu.txt","r",encoding="utf-8") as usu:
    for o in usu:
        ler = usu.readline().strip()
        corda.append(ler)
        print(ler)
        cont+=1
        if cont >=2:
            cont = 0
            total.append(corda[:])
            corda.clear()


            
            
        



print(f"Corda: {corda[:]}")
print("\n")
print(f"Total: {total[:]}")
i = input("")