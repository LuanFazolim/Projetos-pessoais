import os
# Diretório que você deseja definir como o novo diretório de trabalho
novo_diretorio = "E:\Python luan\python\Salvamento\lista"

# Alterar o diretório de trabalho
os.chdir(novo_diretorio)




 
print("Diretório atual:", os.getcwd())
print("Arquivos no diretório:", os.listdir())
            
arquivo_local = "usu.txt"
total = list()
corda = list()
cont_addlist = 0
sn = "s"
temlogin = 0
lgf_nmex = ""


#mandar arquivo para lista
abrir_r_arquivo = open(arquivo_local,"r",)
quantidade_de_linhas = sum(1 for _ in abrir_r_arquivo)
abrir_r_arquivo.seek(0)

for h in range(1,quantidade_de_linhas+1): 
    ler_arquivo = abrir_r_arquivo.readline().strip()
    if h%2 == 0:
       
        corda.append(ler_arquivo)
        total.append(corda[:])
        corda.clear()
 
    else:
        corda.append(ler_arquivo)


    print(ler_arquivo)
abrir_r_arquivo.close()
#Fazer o login
while sn == "s":
    nome = input("nome: ")
    senha = input("senha: ")
    for h in range(0,quantidade_de_linhas):
      
        print(total[h][0])
        if nome in [linha[0] for linha in total]:
            lgf_nmex = "Nome em uso"
            break
        else:
            
            lgf_nmex = "Login feito"
            i = input("")                                                                        
            s = input("else")
            with open(arquivo_local,"a") as abrir_w_arquivo:
                escrever_arquivo = abrir_w_arquivo.write(f"\n{nome}\n{senha}")
                corda.append(nome)
                corda.append(senha)
                total.append(corda[:])
                print(corda)
                print(total)
                corda.clear()
            break
                
    print(lgf_nmex)
    sn = str(input("Continuar [s/n]: ")).lower()

                
            
            







            
            
        



print(f"Corda: {corda[:]}")
print("\n")
print(f"Total: {total[:]}")
i = input("")