import customtkinter as ctk
from PIL import Image

# Cria a janela principal
app = ctk.CTk()
app.geometry("300x200")
app.title("Botão com Imagem")

# Carrega a imagem
# (use caminho absoluto ou imagem na mesma pasta)
imagem = ctk.CTkImage(
    light_image=Image.open(r"D:\Progamacao\Python\ADT\Test_code\icone.png"),  # imagem modo claro
    dark_image=Image.open(r"D:\Progamacao\Python\ADT\Test_code\icone.png"),   # imagem modo escuro
    size=(100, 100)  # tamanho da imagem no botão
)

# Função do botão
def clicar():
    print("Botão clicado!")

# Cria o botão com imagem
botao = ctk.CTkButton(
    app,
    text="",  # pode deixar "" se quiser só a imagem
    image=imagem,
    compound="left",  # imagem à esquerda do texto ("top", "right", "bottom" também funcionam)
    command=clicar
)
botao.pack(pady=30)

app.mainloop()
