import pyodbc
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-E5FJI7M;'
    'DATABASE=iq_option_sql;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

horas_convertidas = []
dinheiro_L = []
sql_horas = []
sql_dinheiro = []

per_hora_i = "19.40.0"
per_hora_f = "19.50.0"
Isep = per_hora_i.split(".")
Fsep = per_hora_f.split(".")
cont = 0

# Carregar dados do banco

def sql_para_lista():
    select = 'SELECT * FROM dados_diarios'
    cursor.execute(select)
    for dado in cursor.fetchall():
        horas_convertidas.append([float(dado[0])])
        dinheiro_L.append([float(dado[1])])

def lista_para_sql():
    query = """
    INSERT INTO dados_diarios (hora, lucro)
    VALUES (?, ?)
    """
    for horas, dinheiros in zip(sql_horas, sql_dinheiro):
        din = dinheiros[0]
        hrs = sum(int(x) / (60**i) for i, x in enumerate(horas.split(':')))
        cursor.execute(query, (hrs, din))
    conn.commit()

def calcular_hora():
    global cont
    for hora in range(int(Isep[0]), int(Fsep[0]) + 1):
        for minuto in range(int(Isep[1]), 60, 2):
            for segundo in range(int(Isep[2]), 60, 60):
                soma_hora = hora + (minuto/60) + (segundo/3600)
                horas_convertidas.append([soma_hora])
                sql_horas.append(f"{hora}:{minuto}:{segundo}")
                if cont == 1 and len(horas_convertidas) == len(dinheiro_L):
                    previsao()
                if f"{hora}.{minuto}.{segundo}" == per_hora_f:
                    input(f"{hora}.{minuto}.{segundo} === {per_hora_f}")
                    add_Dinheiro()
                    cont = 1

def add_Dinheiro():
    global cont
    if cont == 0:
        for num in sql_horas:
            perg_dinheiro = float(input(f"Dinheiro para {num} -->  "))
            dinheiro_L.append([perg_dinheiro])
            sql_dinheiro.append([perg_dinheiro])
    else:
        perg_dinheiro = float(input(f"Dinheiro para {sql_horas[-1]} -->  "))
        dinheiro_L.append([perg_dinheiro])
        sql_dinheiro.append([perg_dinheiro])

def previsao():
    if len(horas_convertidas) != len(dinheiro_L):
        return  # Evita erro se os tamanhos forem diferentes
    
    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(horas_convertidas, np.ravel(dinheiro_L))
    nova_previsao = modelo.predict([horas_convertidas[-1]])[0]
    perg_prev = input(f"\n{sql_horas[-1]} Previsão: {nova_previsao:.5f}  --> ").strip()
    if perg_prev == '':
        dinheiro_L.append([nova_previsao])
        sql_dinheiro.append([nova_previsao])
    elif perg_prev == '000':
        lista_para_sql()
        return grafico()
    else:
        add_Dinheiro()

def grafico():
    plt.scatter(horas_convertidas, dinheiro_L, color="blue", label="Dados reais")
    plt.plot(horas_convertidas, RandomForestRegressor(n_estimators=100).fit(horas_convertidas, np.ravel(dinheiro_L)).predict(horas_convertidas), color="red", label="Previsão")
    plt.xlabel("Horas")
    plt.ylabel("Lucro")
    plt.legend()
    plt.show()

sql_para_lista()
calcular_hora()
