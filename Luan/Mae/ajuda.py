#numero 1
r=input('posiçao: ')
a=input('cidade: ')
e=input('estado: ')
p1=input('preço 0 a 10: ')
p2=input('preço 10 a 20: ')
p3=input('preço 20 a 30: ')
p4=input('preço 30 a 50: ')
p5=input('preço 50 a 70: ')
p7=input('preço 70 a 100: ')
p6=input('preço Kgs: ')

print(40*'\033[35m=\033[m')
print('#{}'.format(r))
print()

print('{}10=float(d/100*{})\nr{}10=float({}-{}10)\n\n'.format(a,p1,a,p1,a))

print('{}20=float(d/100*{})\nr{}20=float({}-{}20)\n\n'.format(a,p2,a,p2,a))

print('{}30=float(d/100*{})\nr{}30=float({}-{}40)\n\n'.format(a,p3,a,p3,a))

print('{}50=float(d/100*{})\nr{}50=float({}-{}60)\n\n'.format(a,p4,a,p4,a))

print('{}70=float(d/100*{})\nr{}70=float({}-{}100)\n\n'.format(a,p5,a,p5,a))

print('{}100=float(d/100*{})\nr{}100=float({}-{}100)\n\n'.format(a,p7,a,p7,a))


print('{}Kgs=float(d/100*{})\nr{}Kgs=float({}-{}Kgs)\n\n'.format(a,p6,a,p6,a))

t=('\ 0 ')
f=t[::2]
verde=('{}33[32m'.format(f))
azul = ('{}33[34m'.format(f))
fim=('{}33[m'.format(f))


print(130*'\033[35m=\033[m')
print()

print("print('",verde+a,"         ",fim,"         (",e,")|  ",azul,"  R${:.4}           R${:.4}             R${:.4}            R${:.4}            R${:.4}             R${:.4}               R${:.4}  ",fim,"    '.format(r"+a+"10,r"+a+"20,r"+a+"30,r"+a+"50,r"+a+"70,r"+a+"100,r"+a+"Kgs))")
