print('==-'*13)
print('           J0GO DA VELHA')
print('==-'*13)
print("O '\033[34mo\033[m' começa")
print(30*'-')
nomeO=str(input('\033[34mo\033[m = Nome: '))
nomeX=str(input('\033[35mx\033[m = Nome: '))
print(40*'-==')
n='''  [1] | [2] | [3]
 -----|-----|-----
  [4] | [5] | [6]
 -----|-----|-----
  [7] | [8] | [9]
  
     Escolha um: '''
ox='o'
num=[1,2,3,4,5,6,7,8,9]
n1=0
n2=0
n3=0
n4=0
n5=0
n6=0
n7=0
n8=0
n9=0
con=0







#==============================================================================================

while True:
    print(f'\033[1;34m{nomeO}:\033[m')
    jdv=int(input(f'''{n}'''))
#=================================================================================
    print()
    while jdv == n1 or jdv == n2 or jdv == n3 or jdv == n4 or jdv == n5 or jdv == n6 or jdv == n7 or jdv == n8 or jdv == n9:

            print('\033[31mEsse local ja foi selecionado!!\033[m')
            print(f'\033[1;34m{nomeO}:\033[m')
            jdv = int(input(f'''Tente denovo!!\n{n}'''))


    if jdv == 1 and ox=='o':
        n=n.replace('[1]',' \033[34mO\033[m ')
        n1=1

    elif jdv == 2 and ox=='o':

        n=n.replace('[2]',' \033[34mO\033[m ')
        n2=2

    elif jdv == 3 and ox=='o':

        n = n.replace('[3]', ' \033[34mO\033[m ')
        n3=3

    elif jdv == 4 and ox=='o':

        n = n.replace('[4]', ' \033[34mO\033[m ')
        n4=4

    elif jdv == 5 and ox=='o':

        n = n.replace('[5]', ' \033[34mO\033[m ')
        n5=5

    elif jdv == 6 and ox=='o':

        n = n.replace('[6]', ' \033[34mO\033[m ')
        n6=6

    elif jdv == 7 and ox=='o':

        n = n.replace('[7]', ' \033[34mO\033[m ')
        n7=7

    elif jdv == 8 and ox=='o':

        n = n.replace('[8]', ' \033[34mO\033[m ')
        n8=8

    elif jdv == 9 and ox=='o':

        n = n.replace('[9]', ' \033[34mO\033[m ')
        n9=9
    print(30 * '-')
    ox='x'
    con+=1



    #============================================================================================================
    if con >= 3 :

        f1 = n.replace(' ','').replace('[34m','').replace('|','').replace('[35m','')[0:15:]

        q1 = f1.count('O')
        if q1 == 3:
            n = n.replace('Escolha um:', ' ').replace('   \033[34mO\033[m  |  \033[34mO\033[m  |  \033[34mO\033[m ','   \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m ')
            print()
            print(n)
            print(f'{nomeO} ganhou!!')
            con+=1
            break


        f2 = n.replace(' ', '').replace('[34m', '').replace('|', '').replace('[35m','')[25:45:]

        q2 = f2.count('O')
        if q2 == 3:

            n = n.replace('Escolha um:', ' ').replace('   \033[34mO\033[m  |  \033[34mO\033[m  |  \033[34mO\033[m ','   \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m ')
            print()
            print(n)
            print(f'{nomeO} ganhou!!')
            con+=1
            break

        f3 = n.replace(' ', '').replace('[34m', '').replace('|', '').replace('[35m','')[48:67:]

        q3 = f3.count('O')
        if q3 == 3:
            n = n.replace('Escolha um:', ' ').replace('   \033[34mO\033[m  |  \033[34mO\033[m  |  \033[34mO\033[m ','   \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m  |  \033[1;4;32mO\033[m ')
            print()

            print(n)

            print(f'{nomeO} ganhou!!')
            con+=1
            break
        print(f1,'\n',f2,'\n',f3)

        f1v = ''.join(n)
        for d1a9 in range(0,10):
            f1v=f1v.replace(' ','').replace('-','').replace('|','').replace(f'[{d1a9}]',f'{d1a9}').replace('Escolha um: ','')

        print(f1v)
        cf1v=f1v.replace('\033[34mO\033[m','O').replace('\033[35mX\033[m','X')
        cf1v1 = cf1v[0:1:].count('O')
        cf1v2 = cf1v[5:6:].count('O')
        cf1v3 = cf1v[8:11:].count('O')


        scf1v= cf1v1+cf1v2+cf1v3

        if scf1v ==3 :

            n1v= n.replace('[34m', '').replace('[35m','').replace('O','\033[1;4;32mO\033[m')[0:7:]
            n2v=n.replace ('\033[34mO\033[m','\033[1;4;32mO\033[m').replace('[34m', '').replace('[35m','')[25:40:]
            n3v= n.replace('\033[34mO\033[m', '\033[1;4;32mO\033[m').replace('[34m', '').replace('[35m','')[48:60:]
            print(n1v,' ',n2v,' ',n3v)



            print(n)
            break










#=======================================================================================================



    if con == 9:
        n=n.replace('Escolha um:',' DEU VELHA!!')
        print(n)

        break
#====================================================================================
    print()
    print(f'\033[1;35m{nomeX}:\033[m')
    jdv = int(input(f'''{n}'''))

    while jdv == n1 or jdv == n2 or jdv == n3 or jdv == n4 or jdv == n5 or jdv == n6 or jdv == n7 or jdv == n8 or jdv == n9:
        print('\033[31mEsse local ja foi selecionado!!\033[m')
        print(f'\033[1;35m{nomeX}:\033[m')
        jdv = int(input(f'''Tente denovo!!\n{n}'''))




    if jdv == 1 and ox == 'x':
        n = n.replace('[1]', ' \033[35mX\033[m ')
        n1=1

    elif jdv == 2 and ox == 'x':
        n = n.replace('[2]', ' \033[35mX\033[m ')
        n2=2

    elif jdv == 3 and ox == 'x':
        n = n.replace('[3]', ' \033[35mX\033[m ')
        n3 = 3

    elif jdv == 4 and ox == 'x':
        n = n.replace('[4]', ' \033[35mX\033[m ')
        n4 = 4
    elif jdv == 5 and ox == 'x':
        n = n.replace('[5]', ' \033[35mX\033[m ')
        n5 = 5
    elif jdv == 6 and ox == 'x':
        n = n.replace('[6]', ' \033[35mX\033[m ')
        n6 = 6
    elif jdv == 7 and ox == 'x':
        n = n.replace('[7]', ' \033[35mX\033[m ')
        n7 = 7
    elif jdv == 8 and ox == 'x':
        n = n.replace('[8]', ' \033[35mX\033[m ')
        n8 = 8
    elif jdv == 9 and ox == 'x':
        n = n.replace('[9]', ' \033[35mX\033[m ')
        n9 = 9



    print(30*'-')

    ox='o'
    con+=1








