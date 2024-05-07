print('transferrncia mm,cm,M')
n=float(input('n: '))
print('      M    cm     mm')
mmpcm=n/10
mmpM=n/1000
cmpM=n/100
cmpmm=n*10
Mpcm=n*100
Mpmm=n*1000


print(' mm {}   {}    {}'.format(mmpM,mmpcm,n))
print(' cm {}   {}    {}'.format(cmpM,n,cmpmm))
print(' mm {}   {}    {}'.format(n,Mpcm,Mpmm))