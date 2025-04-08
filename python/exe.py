import pyodbc
import os


conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-E5FJI7M;'
    'DATABASE=iq_option_sql;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
cont = 0
select = "SELECT * FROM dados_diarios"
while True:
    cont = 0
    T = input("")
    os.system('cls' if os.name == 'nt' else 'clear')
    #print("\033[H\033[J", end="")
    print(T)
    if T == '0':
        break
    cursor.execute(select)
    for row in cursor.fetchall():
        cont +=1
        print(f"  {cont}   |   {row[0]:.5f} ---- {row[1]:.0f}  ")  
conn.commit()
cursor.close()
conn.close()

#cd C:\programacao\python\Machine_Lerang