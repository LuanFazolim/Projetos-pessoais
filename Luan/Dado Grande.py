from random import choice
ligacao=[]
pulando=[]
numesc=[0]
numesc2=[]
criacao=[]
conta=0
per=[]
aju=0
buc=0
dados=('''             -----------
             |         |
             |    ?    |
             |         |
             -----------
''','''              _________
             /         \ 
            /           \ 
           /             \ 
          |       ?       |
           \             /
            \           / 
             \_________/ 
''','''              _________
         ----/         \---- 
         |  /           \  | 
          \/             \/
          |       ?       |
          /\             /\ 
         |  \           /  |
         ----\_________/----
''','''             -----------
            / _________ \ 
         ----/         \---- 
        /|  /           \  |\ 
       /  \/             \/  \ 
      |   |       ?       |   |
       \  /\             /\  /
        \|  \           /  |/
         ----\_________/----
            \           / 
             -----------
''','''                  /\ 
                 /  \ 
                /    \ 
               /      \ 
              /        \  
             /    ?     \ 
            /            \ 
           /              \ 
          /________________\ ''')
cont=0




while True:
    print(50*'-')
    print('''  [\033[1;34m1\033[m]   \033[33mDado normal \033[37m(6 lados)\033[m
  [\033[1;34m2\033[m]   \033[32mDado 0 ao 9\033[m
  [\033[1;34m3\033[m]   \033[36mDado 0 ao 20\033[m
  [\033[1;34m4\033[m]   \033[31mDado 0 ao 90\033[37m (pulando de 10 em 10)\033[m
  [\033[1;34m5\033[m]   \033[35mPersonalizado..\033[m
  [\033[1;34m6\033[m]   \033[1;37mSair\033[m''')
    esc=int(input('Escolha um: '))
    print(50*'-')

    #Dado normal======================================================================================================================================
    if esc == 1:
        print(50*'\n')
        print(70*'\033[33m=','\033[1;33m6 LADOS\033[33m',70*'=')
        print(2*'\n')
        while True:

        #6 LADOS
            x = 1,2,3,4,5,6
            c = choice(x)

            # 1

            t=input("\033[37mClique enter para \033[34mcontinuar\033[37m e 'v' para \033[31mvoltar\033[37m...\033[m")
            if t == 'v':
                print(50 * '\n')
                break
            print(110 * '\n')
            if c >= 0.9:
                if c <= 1.1:
                    print('             ', end='')
                    print(41 * '-')
                    print(8 * "             |                                       |\n", end='')
                    print("             |                   O                   |\n", end='')
                    print(8 * "             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')

            # 2
            if c >= 1.9:
                if c <= 2.1:
                    print('             ', end='')
                    print(41 * '-')
                    print(8 * "             |                                       |\n", end='')
                    print("             |       O                        O      |\n", end='')
                    print(8 * "             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')

            # 3
            if c >= 2.9:
                if c <= 3.1:
                    print('             ', end='')
                    print(41 * '-')
                    print("             |                                       |\n", end='')
                    print("             |   O                                   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |                   O                   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |                                   O   |\n", end='')
                    print("             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')

            # 4
            if c >= 3.9:
                if c <= 4.1:
                    print('             ', end='')
                    print(41 * '-')
                    print("             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |                                       |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print("             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')

            # 5
            if c >= 4.9:
                if c <= 5.1:

                    print('             ', end='')
                    print(41 * '-')
                    print("             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |                   O                   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print("             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')

            # 6
            if c >= 5.9:
                if c <= 6.1:
                    print('             ', end='')
                    print(41 * '-')
                    print("             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print(6 * "             |                                       |\n", end='')
                    print("             |   O                               O   |\n", end='')
                    print("             |                                       |\n", end='')
                    print('             ', end='')
                    print(41 * '-')
            print(10 * '\n')
    #0 ao 9===========================================================================================================================================
    elif esc == 2:
        a09=0,1,2,3,4,5,6,7,8,9
        print(50 * '\n')
        print(70 * '\033[32m=', '\033[1;32m0 ao 9\033[32m', 70 * '=')
        print(2 * '\n')


        while True:

            al09=choice(a09)
            t = input("\033[37mClique enter para \033[34mcontinuar\033[37m e 'v' para \033[31mvoltar\033[37m...\033[m")
            if t == 'v':
                print(50 * '\n')
                break
            else:
                print(20*'\n')
                print('              _________')
                print('             /         \ ')
                print('            /           \ ')
                print('           /             \ ')
                print(f'          |       \033[32m{al09}\033[m       |')
                print('           \             /')
                print('            \           / ')
                print('             \_________/ ')
                print(20 * '\n')
    # 0 ao 20=========================================================================================================================================
    elif esc == 3:
        a20 = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
        print(50 * '\n')
        print(70 * '\033[36m=', '\033[1;36m0 ao 20\033[36m', 70 * '=')
        print(2 * '\n')

        while True:

            al20 = choice(a20)
            t = input("\033[37mClique enter para \033[34mcontinuar\033[37m e 'v' para \033[31mvoltar\033[37m...\033[m")
            if t == 'v':
                print(50 * '\n')
                break
            if al20 < 10 :
                print(20 * '\n')
                print('               _________')
                print('          ----/         \---- ')
                print('          |  /           \  | ')
                print('           \/             \/')
                print(f'           |       \033[1;36m{al20}\033[m       |')
                print('           /\             /\ ')
                print('          |  \           /  |')
                print('          ----\_________/----')
                print(20 * '\n')
            else:
                print(20 * '\n')
                print('               _________')
                print('          ----/         \---- ')
                print('          |  /           \  | ')
                print('           \/             \/')
                print(f'           |      \033[1;36m{al20}\033[m       |')
                print('           /\             /\ ')
                print('          |  \           /  |')
                print('          ----\_________/----')
                print(20 * '\n')
    # 0 ao 90=========================================================================================================================================
    elif esc == 4:
        a90 = 0,10,20,30,40,50,60,70,80,90
        print(50 * '\n')
        print(70 * '\033[31m=', '\033[1;31m0 ao 90\033[31m', 70 * '=')
        print(2 * '\n')

        while True:

            al90 = choice(a90)
            t = input("\033[37mClique enter para \033[34mcontinuar\033[37m e 'v' para \033[31mvoltar\033[37m...\033[m")
            if t == 'v':
                print(50 * '\n')
                break
            if al90 == 0:
                print(20 * '\n')
                print('         -----------')
                print('        / _________ \ ')
                print('     ----/         \---- ')
                print('    /|  /           \  |\ ')
                print('   /  \/             \/  \ ')
                print('  |   |       \033[31m0\033[m       |   |')
                print('   \  /\             /\  /')
                print('    \|  \           /  |/')
                print('     ----\_________/----')
                print('        \           / ')
                print('         -----------')
                print(20 * '\n')
            else:
                print(20 * '\n')
                print('         -----------')
                print('        / _________ \ ')
                print('     ----/         \---- ')
                print('    /|  /           \  |\ ')
                print('   /  \/             \/  \ ')
                print(f'  |   |      \033[31m{al90}\033[m       |   |')
                print('   \  /\             /\  /')
                print('    \|  \           /  |/')
                print('     ----\_________/----')
                print('        \           / ')
                print('         -----------')
                print(20 * '\n')
    #criar============================================================================================================================================
    elif esc == 5:
        print(50 * '\n')
        print(70*'\033[35m=\033[m','\033[1;35mPERSONALIZADO\033[m',70*'\033[35m=\033[m')
        if cont == 0:
            print('\033[1mDigite o nome para o seu dado:\033[m')
            print(10*'\n')
            ligacao.append(input(': '))




        elif cont > 0 :
            lec=len(criacao)
            print('(\033[1;35m0\033[m)  Criar..')
            print()
            for www in range(0,cont):

                print(f'(\033[1;34m{www+1}\033[m)   {criacao[www][0]}')
            print(40*'-')
            print()
            per=int(input('Escolha um: '))
            if per == 0:
                print('\033[1mDigite o nome para o seu dado:\033[m')
                print(10 * '\n')
                ligacao.append(input(': '))


            else:

                while True:


                    cc = choice(criacao[per-1][2])



                    t = input("\033[37mClique enter para \033[34mcontinuar\033[37m e 'v' para \033[31mvoltar\033[37m...\033[m")
                    if t == 'v':
                        print(50 * '\n')
                        break
                    elif cc > 9 and aju == 1:
                        print(20 * '\n')
                        s = criacao[per - 1][1].replace('? ', f'{cc}')

                        print(s)
                        print(20 * '\n')

                    elif cc > 9 and aju == 0:
                        print(20 * '\n')
                        s = criacao[per - 1][1].replace(' ?', f'{cc}')

                        print(s)
                        print(20 * '\n')


                    else:
                        print(20 * '\n')
                        s = criacao[per - 1][1].replace('?', f'{cc}')
                        print(s)
                        print(20 * '\n')


            print()
            print(50*'-')



#perso------------------------------------------------------------------------------------------------------------------



        if cont == 0 or per == 0:
            print(10*'\n')
            print('''(\033[34m1\033[m) \033[1;33mNumeros Selecionados\033[m 
\033[37m...numeros que vc seleciona...\033[m 

(\033[34m2\033[m) \033[1;32mNumeros Personalizados\033[m    
\033[37m...numeros que vc pode personalizar de onde começa, acaba, pulando tantos em tantos numeros...\033[m''')

            print(30*'\n')
            nume=int(input('Escolha um: '))
            print(50*'\n')
            if nume == 1:
                print('\033[1mEscolha os numeros\033[37m(escreva "s" para parar)\033[m:')
                print(5*'\n')

                while numesc[0] != 's' and numesc[0] != 'S':
                    conta+=1
                    tnu=str(input(f'numero {conta}: ')).lower()
                    numesc.insert(0,tnu)
                numesc.remove(0)
                numesc.remove('s')
                conta-=conta
                numesc = list(map(int, numesc))




            elif nume == 2:
                comec=int(input('Começa: '))
                print()
                pula=int(input('Pulando de: '))
                print()
                fim=int(input('Termina: '))
                for aa in range(comec,fim+1):
                    pulando.append(aa)



                numesc2.append(pulando[::pula])
                print(numesc2)








                print()



    #Dados--------------------------------------------------------------------------------------------------------------------
            for eee in range(0,5):
                print(40*'-')
                print()
                print(f'(\033[1;34m{eee+1}\033[m)\n'+dados[eee])
                print()
            print(40*'-')
            print()

            cri=int(input('Escolha um: '))
            if cri == 5:
                aju+=1
            else:
                aju=0
            ligacao.append(dados[cri-1])





            if buc == 1:
                ligacao.append(1)
            else:
                ligacao.append(0)
            print(numesc)
            ligacao.append(numesc[:])
            criacao.append(ligacao[:])

            ligacao.clear()
            numesc.clear()
            numesc.append(0)
            cont+=1


            print()
            print(criacao)




    #print(30 * '=', 'Criar', 30 * '=')
    #print('[\033[1;34m0\033[m] \033[1;37m+\033[m')
    #print(30 * '-')








    #SAIR=========================================================================================================================================
    elif esc == 6:
        print('\033[1;31;47mVOCE ESCOLHEU SAIR!!\033[m')
        break

    #else=============================================================================================================================================
    else:
        print('\033[1;31mtente novamente!!\033[m')