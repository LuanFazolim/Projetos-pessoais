
from PySimpleGUI import PySimpleGUI as sg  

#loyout
sg.theme ("Reddit")
layout = [
    [sg.Text ("Usuario"), sg.Input(key="usuario", size= (18,1)),],
    [sg.Text ("Senha"), sg.Input(key="senha", password_char="*", size= (20,4))],
    [sg.Checkbox ("Salvar o login?")],
    [sg.Button ("Entrar")]
]


#janela

janela = sg.Window("Tela de Login", layout)

#ler eventos
while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break
    elif eventos == "Entrar":
        if valores ["usuario"] == "Luan" and valores["senha"] == "777":
            print("Voce ja tem uma conta!!")
            break
        else:
            print("Bem vindo {}!!\n Sua senha e: {}".format(valores["usuario"], valores["senha"]))
