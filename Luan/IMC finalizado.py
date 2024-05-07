print('\033[34mIMC\033[m')

print('')

p = float(input('\033[7mPeso\033[m: '))

a = float(input('\033[7;36mAltura \033[m(*\033[35m.\033[m**): '))

e = a * a

f = p / e

print()

print('seu \033[34mIMC\033[m é de:{:.2f}'.format(f))

print()

if f <= 18.5:
    print('\033[33mAbaixo do peso')

if f >= 18.5:
    if f <= 24.9: print('\033[32mPeso normal')

if f >= 25:
    if f <= 29.9: print('\033[33mAcima do peso(sobrepeso)')

if f >= 30:
    if f <= 34.9: print('\033[31mObesidade 1')

if f >= 35:
    if f <= 39.9: print('\033[31mObesidade 2')

if f >= 40:
    print('\033[31;40mObesidade 3!!\033[m')



# Menor do que 18,5 = abaixo do peso



# entre 18,5 e 24,9 = peso normal



# entre 25 e 29,9 = acima do peso (sobrepeso)



# entre 30 e 34,9 = obesidade 1



# entre 35 e 39,9 = obesidade 2



# maior do que 40 = obesidade 3