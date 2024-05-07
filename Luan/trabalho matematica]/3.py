print('a)')
print('')
r1=int(input(': '))
r2=int(input(': '))
r3=int(input(': '))
r4=int(input(': '))
r5=int(input(': '))
h=int(input('base: '))
n1=int(input(': '))
n2=int(input(': '))
n3=int(input(': '))
n4=int(input(': '))
n5=int(input(': '))
h1=int(input('base: '))
print('')
j=r4*h
j1=(h*h)*r3
j2=(h*h*h)*r2
j3=(h*h*h*h)*r1
p=r5+j+j1+j2+j3
print(p)
t=n4*h1
t1=(h1*h1)*n3
t2=(h1*h1*h1)*n2
t3=(h1*h1*h1*h1)*n1
p1=n5+t+t1+t2+t3
print(p1)
c=p*p1
print('')
print('resposta: {}'.format(c))
print("")
print('b)')
n1=int(input(':'))
n2=int(input(':'))
n3=int(input(':'))
b1=int(input('Base:'))
m1=int(input(':'))
m2=int(input(':'))
m3=int(input(':'))
b2=int(input('Base:'))
z1=int(input(':'))
z2=int(input(':'))
z3=int(input(':'))
b3=int(input('Base:'))
c=n3
c1=b1*n2
c2=(b1*b1)*n1
cr=c+c1+c2
print(cr)
v=m3
v1=b1*m2
v2=(b1*b1)*m1
vr=v+v1+v2
print(vr,'   +')
x=z3
x1=b1*z2
x2=(b1*b1)*z1
xr=x+x1+x2
print(xr)
r=cr+vr+xr
print('--')
print(r)