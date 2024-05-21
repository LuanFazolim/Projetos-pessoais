import colorama
def es():
    print()
def linha():
    print(20*"-")

cont = 0

   



while True:
    
    with open ("usuario.txt","r", encoding="utf-8") as le:
        
        cont = le.read().count("Nome:") +1

    
    es()
    nome = input("Nome: ")
   
    senha = input("Senha: ")  
    
    es()
    exib = str(input("Exibir todos os dados? [S/N]: ")).upper()
    es()
    

    #escrever
    with open("usuario.txt","a") as usu:
        
        usu.write(f"Usuario [{cont}]\nNome: {nome}    \nSenha: {senha} \n\n\n") 
     
   
    #ler
    with open ("usuario.txt","r", encoding="utf-8") as le:
        ler = le.read()
        
 
    while True:
        if exib == "S":
            linha()
            print()
            print(f"\n{ler}\n")
            print()
            linha()
            t = input(f"{colorama.Fore.BLACK}enter para continuar...{colorama.Style.RESET_ALL}")
            print()
            break
            
        elif exib == "N":
            t = input(f"{colorama.Fore.BLACK}enter para continuar...{colorama.Style.RESET_ALL}")
            print()
            break


            
        else:
                print("digite um valor valido!!")
                print(exib)
                es()
                exib = str(input("Exibir todos os dados? [S/N]: ")).upper()
                es()
        
                
   
           
            

    
    
    
        
        
