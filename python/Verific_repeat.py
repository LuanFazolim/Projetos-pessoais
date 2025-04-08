import os
import shutil

Lista_1 = []
Lista_2 = []
Repetidas = []



def repeat_verify():
    Cont = 0
    for num,item_1 in enumerate(Lista_1):
        for item_2 in Lista_2:
            '''if "." in item_1[0]:
                print("..ARQUIVO..")
            else:
                print("---PASTA---")'''
            if item_1[0] == item_2[0]:
                #print(f"\n  {item_1[0]}     =====      {item_2[0]}")
                Repetidas.append([item_1[1],item_2[1],item_1[0],item_2[0],])

                Cont +=1
            #else:
                #print(f"\n  {item_1[0]}     =XXXXX=      {item_2[0]}")
    print(20*"\n")
    #for item in Repetidas:
        #print(f"{item[0]}      ====        {item[1]}         ({item[2]} == {item[3]})\n\n")
    print(f"\n\n UM TOTAL DE === {Cont} ===\n")
    print(f"--= Diretorio {Diret_1} Contem == {len(Lista_1)} == itens =--\n")
    print(f"--= Diretorio {Diret_2} Contem == {len(Lista_2)} == itens =--")
            
    
        
    
def add_list(Diret,num):
    try:
        for item in os.listdir(Diret):
            caminho_item = os.path.join(Diret, item)
            caminho_item_nome = caminho_item.split("\\")
            if num == 1:
                Lista_1.append([caminho_item_nome[-1],caminho_item])
            elif num == 2:
                Lista_2.append([caminho_item_nome[-1],caminho_item])
    except PermissionError as e:
        return 
        #print(f"Arquivo não permitido ignorado: {Diret} - {e}")
    except Exception as e:
        return
        #print(f"Erro ao acessar {Diret}: {e}")
    

    
    
Diret_1 = "C:\\TESTE\C"
Diret_2 = "C:\\TESTE\E"

add_list(Diret_2,2)
add_list(Diret_1,1)
for item in Lista_1:
    if "." not in item[0]:
    
        Diret_1 = item[1]
        add_list(Diret_1,1)
            
for item in Lista_2:
    if "." not in item[0]:
    
        Diret_2 = item[1]
        add_list(Diret_2,2)


repeat_verify()

    
print(f"\n\n Lista 1 = {Lista_1}")
print(f"\n Lista 2 = {Lista_2}\n\n")
print(f"\n\n Repetidas = {Repetidas}")

#python Verific_repeat.py