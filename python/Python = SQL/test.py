import mysql.connector

conex = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0419",

    database="primeirobd",
)

cursor = conex.cursor()
c = 0



while c<= 4:

    nome_produto = "todynho"
    valor = c
    comando = f'INSERT INTO vendas (nome_produto, valor) VALUE ("{nome_produto}","{valor}")'
    comando2 = f'DELETE FROM vendas WHERE nome_produto = ("{nome_produto}")'
    c +=1
    cursor.execute(comando2)

    conex.commit() #editar o Banco de dados
    resultado = cursor.fetchall() #ler o Banco de dados

    print(resultado)

cursor.close()
conex.close()
