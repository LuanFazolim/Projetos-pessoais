import os
# Diretório que você deseja definir como o novo diretório de trabalho
novo_diretorio = "C:\python\salvamento\listas"

# Alterar o diretório de trabalho
os.chdir(novo_diretorio)





 
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
            

sn = "s"
total = list()
corda = list()
cont = 0
con = 0
err = 1

#add dados a lista 
with open("usu.txt","r",encoding="utf-8") as usu:
    for o in usu:
        ler = usu.readline().strip()
        corda.append(ler)
        cont+=1
        if cont >=2:
            cont = 0
            total.append(corda[:])
            corda.clear()


with open("usu.txt","a") as esc:
        while sn == "s":
            if err == 1:
                nome = input("nome: ")
                senha = input("senha: ")
                corda.append(nome)
                corda.append(senha)

            
            for i in total: 
                    if nome == total[con][0]:
                        err == 1
                        
                        con == 0
                        print(f"{nome}  ==  {total[con][0]}")
                        print("Nome ja utilizado")
                        break
                    else:
                        print(f"{nome}  !=  {total[con][0]}")
                        err = 0
                    con+=1



                    
            else:
                total.append(corda[:])
                corda.clear()
                abr = esc.write(f"\n{nome}\n\n{senha}\n")
                sn = str(input("continuar: ")).lower()
                err = 1
                print("login Feito")




            
            
        



print(f"Corda: {corda[:]}")
print("\n")
print(f"Total: {total[:]}")
i = input("")