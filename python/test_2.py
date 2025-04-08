import pyodbc
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-E5FJI7M;'
    'DATABASE=iq_option_sql;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()


horas_convertidas = []
horas_nm = []
dinheiro_L = []

sql_horas = []
sql_dinheiro = []

per_hora_i = "19.40.0"
# 
# per_hora_f = input("---> ")
per_hora_f = "19.50.0"
Isep = per_hora_i.split(".")
Fsep = per_hora_f.split(".")
Hperiodo = 1
Mperiodo = 1
Speriodo = 1
cont = 0
corda = 0

def sql_para_lista():
    select = 'SELECT * FROM dados_diarios'
    cursor.execute(select)
    for dado in cursor.fetchall():
        horas_convertidas.append([float(dado[0])])
        dinheiro_L.append([float(dado[1])])
    print(horas_convertidas,'\n',dinheiro_L)
 
 
def lista_para_sql ():
    query = """
    INSERT INTO dados_diarios (hora, lucro)
    VALUES (?, ?)
    """
    for horas,dinheiros in zip(sql_horas,sql_dinheiro) :
        din = dinheiros[0]
        hrs = horas.split(':')
        hrs = int(hrs[0]) +(int(hrs[1])/60) + (int(hrs[2])/3600)
        print(hrs , din)
    
    cursor.execute(query, (hrs, din))
    
       
def calcular_hora():
    global Hperiodo
    global Mperiodo
    global Speriodo
    global cont
    #per_hora_i = input("---> ")
    '''perg_periodo = int(input("""
    [1] 1 seg
    [2] 30 seg
    [3] 2 min"""))'''
    perg_periodo = 3
    # 1seg
    if perg_periodo == 1:
        Hperiodo = Mperiodo = Speriodo = 1
    # 30seg
    if perg_periodo == 2:
        Hperiodo = Mperiodo = 1
        Speriodo = 30
    # 2min
    if perg_periodo == 3:
        Hperiodo = 1
        Mperiodo = 2
        Speriodo = 60
     
    
    
    
    min_calc = 60 * (int(Fsep[0])- int(Isep[0])) + int(Fsep[1])
    seg_calc = 60 * (min_calc - int(Isep[1])) + int(Fsep[2])
   
   #Hora --
    for hora in range(int(Isep[0]),24,Hperiodo):
       
       #Minuto --
       for minuto in range(int(Isep[1]),61,Mperiodo):
            
            
            if minuto%60 == 0 and minuto != 0:
                min_calc -=60
                Isep[1] = '0'
                break
           
            #Segundos --
            for segundo in range(int(Isep[2]),61,Speriodo):
                
                if segundo%60 == 0 and segundo != 0:
                    seg_calc -=60
                    Isep[2] = '0'
                    break
                else:
                    soma_hora = hora + (minuto/60)+(segundo/3600)
                    horas_convertidas.append([soma_hora])
                    soma_hora = f"{hora}:{minuto}:{segundo}"
                    horas_nm.append(soma_hora)
                    sql_horas.append(soma_hora)
                    
                    #print(horas_nm)
                    #print(horas_convertidas)
                    #print(f"{hora}:{minuto}:{segundo}")
                    
                    str_seg = str(hora)+"."+str(minuto)+"."+str(segundo)
                    if cont == 1:
                        
                        previsao()    
                    if  str_seg == per_hora_f:
                        t = input(f"{str(hora)}.{str(minuto)}.{str(segundo)} === {per_hora_f}")  
                        add_Dinheiro()
                        cont = 1    
                   
                     
                          
                    
def add_Dinheiro():
    global cont
    if cont == 0:
        for num in horas_nm:
            print("\n",num)
            perg_dinheiro = float(input("Dinheiro -->  "))
            dinheiro_L.append([perg_dinheiro])
            sql_dinheiro.append([perg_dinheiro])
            
    else:
        print("\n",horas_nm[-1])
        perg_dinheiro = float(input("Dinheiro -->  "))
        dinheiro_L.append([perg_dinheiro])
        sql_dinheiro.append([perg_dinheiro])
        
        


def previsao():
    global corda
    
    corda = horas_convertidas[-1]
    
    horas_convertidas.pop()
    print(horas_convertidas)
    print(dinheiro_L)
    #Criando 30 dados com horas quebradas e valores de dinheiro que sobem e descem
    horas = np.array(horas_convertidas)  # Horas
    dinheiro = np.array(dinheiro_L)  # Dinheiro
    
    modelo = LinearRegression()
    modelo.fit(horas, dinheiro)
    horas_grafic = np.array(horas_nm)
    # Fazendo previsões
    previsoes = modelo.predict(horas)
    print(f"\n\nCoeficiente angular (slope): {modelo.coef_[0][0]:.2f}")
    print(f"Intercepto (intercept): {modelo.intercept_[0]:.2f}\n\n")
    


    
    teste2 = modelo.predict([corda])
    print(f"")
    perg_prev = input(f"\n{horas_nm[-1]} Previsao de :  == {teste2[0].item()} == \n  --> ").lower()
    horas_convertidas.append(corda)

    print(type(corda))
    if perg_prev == '':
        dinheiro_L.append([teste2[0].item()])
        sql_dinheiro.append([teste2[0].item()])
    elif perg_prev == '000':
        horas_grafic = horas_convertidas[:-1]
        sql_horas.pop()
        lista_para_sql()
        return grafico(horas_grafic,previsoes,dinheiro)
    else:
        add_Dinheiro()
    

                    
def grafico(horas_grafic,previsoes,dinheiro):
    print(sql_horas,"\n",sql_dinheiro)
    print(len(sql_horas),"\n",len(sql_dinheiro))
    plt.scatter(horas_grafic, dinheiro, color="blue", label="Dados reais")
    plt.plot(horas_grafic, previsoes, color="red", label="Previsões do modelo")
    plt.xlabel("Horas (quebradas)")
    plt.ylabel("Dinheiro (R$)")
    plt.legend()
    plt.show()
    
sql_para_lista()
calcular_hora()

    

     










