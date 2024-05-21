#loyout
import time
import sys
def espacos():
    print(100*"=")
    print(220*"\n")

VTX= 20*("=")



loyout = 0
loy_voltar  = "s"
loy_voltar_entrar = 2


while not loyout  ==  5:

    if loy_voltar == "s":
        loy_voltar = "n"
        print(f"""
    {VTX}- BANCO DE DADOS -{VTX}

    [1] Entrar
    [2] Fazer Login
    [3] Mostrar dados
    [4] Apagar dados
    [5] Sair
        \n\n\n\n\n\n\n""")
        
        loyout = int(input("---> "))
        while 5 < loyout or loyout < 1  :
            loyout = int(input("---> "))
            print("Digite um valor valido!!")
            print()
                
        
        espacos()
        
        
        
       
    else:
        while loy_voltar == "n":
            espacos()
                        
            
              #Entrar
            if loyout == 1:
             
                print(VTX,"ENTRAR",VTX)
                entrar_nome = input("Nome: ")
                entrar_senha = input("Senha: ")
                with open ('usuario.txt','r',encoding="utf-8") as usuario_var:
                    ler_arquivo = usuario_var.read().count(entrar_nome)
             
                    
                    if ler_arquivo == 1:
                        print()                       
                        print("Entrando...")
                        s = input("")
                     
                        
                    else:
                        espacos()
                        print("Nome ou senha errados!!!")
                      

                        while True:
                            print("\nVoltar Para\n\n[1] Menu\n[2] Aba Entrar\n\n\n\n")
                            
                            loy_voltar_entrar = str(input("--> "))
                            if loy_voltar_entrar == "1" or loy_voltar_entrar == "2" :
                                if loy_voltar_entrar == "1":
                                    loy_voltar = "s"
                                break
                             
                            else:
                                print('Digite um valor valido!!')
           
        
              #Login
            elif loyout == 2:
                
                print(VTX,"LOGIN",VTX)
                login_nome = input("Digite seu Nome: ")
                login_senha = input("Digite uma Senha: ")
                with open ('usuario.txt','r',encoding="utf-8") as usuario_var:
                    ler_arquivo = usuario_var.read().count(login_nome)
                    if ler_arquivo >= 1:    
                        espacos()
                        print("Nome existente!!")
                    else:
                        with open ("usuario.txt", "a") as usuario_ler:
                            usuario_ler.write(f"\nNome: {login_nome}\nSenha: {login_senha}\n")
                        print("Login feito com sucesso!!")
                      
                        print("\n\n\n\n")
                

                        login_descricao = input ("Digite suas anotacoes:\n\n")
                
                
                while True:
                    
                    loy_voltar = str(input("Voltar [S/N]?: ")).lower()
                    if loy_voltar == "s" or loy_voltar == 'n':
                        break
                    else:
                        print('Digite um valor valido!!')
            elif loyout == 3:
                with open("usuario.txt","r",encoding="utf-8") as ler_arquivo:
                    ler = ler_arquivo.read()
                    print(ler)
                    print("\n\n\n\n")
                    while True:
                    
                        loy_voltar = str(input("Voltar [S/N]?: ")).lower()
                        if loy_voltar == "s" or loy_voltar == 'n':
                            break
                        else:
                            print('Digite um valor valido!!')
                    
                    
                                    
            elif loyout == 4:
             
               
                for ponto in range(4):
                    sys.stdout.write("\r{}{}".format("Excluindo Dados", "." * ponto))
                    sys.stdout.flush()
                    time.sleep(1)
                with open("usuario.txt","w") as apagar:
                    
                    pass
                loy_voltar = "s"
             
        espacos()                    
                    
                        
               
             
            
            