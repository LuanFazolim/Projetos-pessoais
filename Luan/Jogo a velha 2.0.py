jogo_l = []

caixa_l = []
time1_l = []
time2_l = []



ganhador_lista = ["123","456","789","147","258","369","159","357"]

nm_xo = ["[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]", "[9]"]
nomeO = ""
nomeX = ""
while not nomeX or not nomeO:
    if not nomeO or not nomeX:
        if not nomeO:
            nomeO = input("Digite o nome do usuario O: ")
        elif not nomeX:
            nomeX = input("Digite o nome do usuario X: ")


rodada = 0
xo = "o"

def Dganhador(time):
    cont = 0
    i = 0



    while cont != len(time):

        if rodada != 5 and rodada != 6:
            caixa_l.append(time.pop(0))
        juntar = "".join(time)

        for _ in range(9):
            if juntar in ganhador_lista:
                return Dsele(time1_l,nomeO,1)

            else:
                if i == 2:
                    i = 0
                    caixa = time.pop(0)
                    time.append(caixa)
                    juntar = "".join(time)
                else:
                    caixa = time.pop(1)
                    time.append(caixa)
                    juntar = "".join(time)
                    i += 1
        if rodada != 5 and rodada != 6:
            time.insert(0, caixa_l[0])
            caixa_l.clear()

        cont += 1

def Dsele(nome,time, fim):
        selecionar = f'''  

          {nm_xo[0]} | {nm_xo[1]} | {nm_xo[2]}
         -----|-----|-----
          {nm_xo[3]} | {nm_xo[4]} | {nm_xo[5]}
         -----|-----|-----
          {nm_xo[6]} | {nm_xo[7]} | {nm_xo[8]}

             Escolha um: '''

        if fim ==0:
            print(f"Vez de {nome}")
            pergunta = input(f"""{selecionar}""")


            if pergunta in ("1,2,3,4,5,6,7,8,9") and pergunta:
                if jogo_l:
                    if pergunta in jogo_l:
                            print("Escolha um valor que nao foi selecionado!!")
                            Dsele(nome,time,0)
                    else:
                        jogo_l.append(pergunta)
                        nm_xo[int(pergunta)-1] = f' {xo} '
                        time.append(pergunta)

                else:
                    jogo_l.append(pergunta)
                    nm_xo[int(pergunta)-1] = f' {xo} '
                    time.append(pergunta)
            else:
                print("Escolha um valor valido")
                Dsele(nome,time,0)
        else:
            print(100 * "\n")
            print(selecionar)
            if xo == "o":
                print(f"{nomeO} e o vencedor!!!")
                exit()
            elif xo == "x":
                print(f"{nomeX} e o vencedor!!!")
                exit()


while True:



  if xo == "o":
      print(100 * "\n")
      Dsele(nomeO,time1_l,0)
      rodada+=1
      if rodada >= 5:
         Dganhador(time1_l)

      xo = "x"


  else:
      print(100 * "\n")
      Dsele(nomeX, time2_l,0)

      rodada += 1
      if rodada >= 5:
          Dganhador(time2_l)
      xo = "o"
