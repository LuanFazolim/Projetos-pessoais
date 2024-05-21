try:
    with open("usuario.txt", "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
        print(conteudo)
except FileNotFoundError:
    print("O arquivo 'usuario.txt' nao foi encontrado.")