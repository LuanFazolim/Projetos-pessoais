print('\033[1;33mCRIAÇAO\033[m')
#TOPICO -------------------------------------------------------------------------------------------------------
lista=[]
correto=[]
certa=[]


pergun=0
cont=0

tema=input(str('\033[33mTema\033[m: '))
print(20*'',f'      \033[33m{tema:}\033[37m',end='    ')
print('| \033[35m...\033[37m | \033[35m... \033[37m| \033[35m... \033[m')
print()
while pergun != 'PRONTO' and pergun!= '00':

    pergun= input('\033[35mTopico \033[37m(escrava "PRONTO" para acabar)\033[m: ')
    if pergun != 'PRONTO' and pergun!='00':
        lista.append(pergun)
        cont+=1

#------------------------------------------------------------------------------------------------------------
#Linha-------------------------------------------------------------------------------------------------------
print()
l=0
print()
print(7*' ',end='')
print(f'\033[1;33m{tema.upper():<13}\033[m',end='')

for fon in range(0,cont):
    leno=len(lista[fon])
    l+=leno
    print(f'|   \033[35m{lista[fon].upper()}\033[m   ',end='')
print()
lilista=[]
lipergun=0
licont=0

while lipergun != 'PRONTO' and lipergun!= '00':

    lipergun= input('\033[32mLinha \033[37m(escrava "PRONTO" para acabar)\033[m: ')
    if lipergun != 'PRONTO' and lipergun!='00':
        lilista.append(lipergun)
        licont+=1

#--------------------------------------------------------------------------------------------------------------




l=0
print()
print(7*' ',end='')
print(f'\033[1;33m{tema.upper():<13}\033[m',end='')


#print Topico---------------------------------------------------------------------------------------------------

for fon in range(0,cont):
    leno=len(lista[fon])
    l+=leno
    print(f'|   \033[35m{lista[fon].upper()}\033[m   ',end='')
#---------------------------------------------------------------------------------------------------------------------


print()
m='-'
n=len(lista)*8
ln=l+n
print(f'{m:-<20}'+'|'+ln*'-')

#print Linha-----------------------------------------------------------------------------------------------------------
for fon in range(0,licont):
    print(7*' '+f'\033[32m{lilista[fon].capitalize():<13}\033[m|',end='')
    for num in range(0,cont):
        lem=len(lista[num])
        l8=lem+8
        lenlista=int(l8/2)-2
        lm1=lenlista+1
        if lem%2==0:
            print(lenlista*' '+f'\033[34m({num+1})\033[m',end=lenlista*' ')

        else:
            print(lenlista*' '+f'\033[34m({num+1})\033[m',end=lm1*' ')
    print()
    correto.append(input('Qual esta \033[34mcerto?\033[m: '))
    print()
    print(f'{m:-<20}' + '|' + ln * '-')

#------------------------------------------------------------------------------------------------------------------










for espa in range(0,100):
    print()
print(20*'='+'\033[1;36mQUAL E A CORRETA\033[m'+20*'=')




l=0
print()
print(7*' ',end='')
print(f'\033[1;33m{tema.upper():<13}\033[m',end='')


#print Topico---------------------------------------------------------------------------------------------------

for fon in range(0,cont):
    leno=len(lista[fon])
    l+=leno
    print(f'|   \033[35m{lista[fon].upper()}\033[m   ',end='')
print()

#---------------------------------------------------------------------------------------------------------------------


m='-'
n=len(lista)*8
ln=l+n
print(f'{m:-<20}'+'|'+ln*'-')


#print Linha-----------------------------------------------------------------------------------------------------------
for fon in range(0,licont):
    print(7*' '+f'\033[32m{lilista[fon].capitalize():<13}\033[m|',end='')
    for num in range(0,cont):
        lem=len(lista[num])
        l8=lem+8
        lenlista=int(l8/2)-2
        lm1=lenlista+1
        if lem%2==0:
            print(lenlista*' '+f'\033[34m({num+1})\033[m',end=lenlista*' ')

        else:
            print(lenlista*' '+f'\033[34m({num+1})\033[m',end=lm1*' ')
    print()
#-----------------------------------------------------------------------------------------------------------------------
conta=0
for coin in range(0,licont):
    couin=input(f'\033[34m{lilista[coin]}\033[m?: ')

    if couin in correto[coin]:
        certa.append(conta)
    conta += 1
print(certa)




#Resultado----------------------------------------------------------------------------------
for espa in range (0,50):
    print()

print(20*'='+'\033[1;35mRESULTADO\033[m'+20*'=')
print()








l=0
print()
print(7*' ',end='')
print(f'\033[1;33m{tema.upper():<13}\033[m',end='')


#print Topico---------------------------------------------------------------------------------------------------

for fon in range(0,cont):
    leno=len(lista[fon])
    l+=leno
    print(f'|   \033[35m{lista[fon].upper()}\033[m   ',end='')
print()

for ww in range (0,licont):
    for cor in certa:
        if lilista[ww] in certa[ww]:
            print(f'\033[32m{lilista[cor]}\033[m')
        else:
            print(f'\033[31m{lilista[ww]}\033[m')
