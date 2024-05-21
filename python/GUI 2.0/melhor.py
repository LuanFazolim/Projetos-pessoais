from PySimpleGUI import PySimpleGUI as sg  

line = []
with open("dados.txt","r", encoding="utf-8") as arquvo_L_dados:
        ler_dados = arquvo_L_dados.read().strip()
        line = list(ler_dados[:])
        line = "".join(line)
#Loyout
sg.theme("DarkGrey9")

layout= [
    [sg.Text("Usuario",size=(6,1)),sg.Input(key="usuario")],
    [sg.Text("Senha",size=(6,1)),sg.Input(key="senha",password_char="*")],
    [sg.Text(" ", size = (1,1))],
    [sg.Button("Fazer Login",size=(8,1)),sg.Text("      ",size=(30,1)), sg.Button("Entrar", size=(5,2))],
    
]

#janela

janela = sg.Window("Tela de Login", layout)

#ler eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    
    elif eventos == "Fazer Login" :
        print(line)
       
        if (valores["usuario"]) in line:     
         print("voce ja tem uma conta")
        
        else:
            with open("dados.txt","a") as usu:
                usu.write(f"{valores["usuario"]}\n")
                print("conta criada")
                with open("dados.txt","r", encoding="utf-8") as arquvo_L_dados:
                    ler_dados = arquvo_L_dados.read().strip()
                    line = list(ler_dados[:])
                    line = "".join(line)
          
         
                
                
                
    elif eventos == "Entrar":
         if (valores["usuario"]) in line:
                print("Entrando...")
         else:
            print("seu nome ou sua senha esta incrreto!!")
            
                
            
            
            
    
        
          
                
         
            
        