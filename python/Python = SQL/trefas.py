import mysql.connector

# Conexão com o banco de dados
conex = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0419",
    database="bd_lista_tarefas"
)
cursor = conex.cursor()

total = []
lista_tarefa = []
lista_marcado = []

#comando = "DELETE FROM usuarios"
#cursor.execute(comando)

escolha = 0


def dv_f(v_f):
    if marc_ou_exc == 1:
        total[escolha - 1][1] = v_f
        # lista_tarefa[escolha-1] = f"{escolha-1} ✔"
    elif marc_ou_exc == 2:
        total.pop(escolha-1)

def dBd_lis(exe,lista_):
    for lista in exe:
        list = lista[0]

        lista_.append(list)


def dPy_lis(tarefa, marcado):
    total.append([tarefa, marcado])






while escolha != 999:

    #ler coluna Tarefa
    cursor.execute("SELECT Tarefa FROM usuarios")
    tarefa_exe = cursor.fetchall()

    # ler coluna marcado
    cursor.execute("SELECT marcado FROM usuarios")
    marcado_exe = cursor.fetchall()

    #VERIFICAR SE POSSUI UM ITEM
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE Tarefa IS NOT NULL")
    possuir_item = cursor.fetchone()




    #possui um item
    if possuir_item[0] > 0:
        total.clear()
        lista_marcado.clear()
        lista_tarefa.clear()


        dBd_lis(tarefa_exe,lista_tarefa)
        dBd_lis(marcado_exe,lista_marcado)
        for num,tt in enumerate(tarefa_exe):

            dPy_lis(lista_tarefa[num],lista_marcado[num])

        print(100 * '\n')
        print("[0] Criar uma nova tarefa\n")


        for num,item in enumerate(lista_tarefa):

            if total[num][1] == "f":
                print(f"[{num+1}] {item}")
            elif total[num][1] == "v":
                print(f"[{num + 1}] {item} ✔")
        print(2*"\n")
        escolha = int(input("Escolha uma opçao --> "))

        if escolha > 0:
            print(100 * '\n')
            print(f"========-- {total[escolha - 1][0]} --========")

            if total[escolha-1][1] == "f":
                print("""
Oque voce deseja fazer cm essa tarefa:

[1] Marcar como concluida
[2] Excluir    
        
""")
            elif total[escolha - 1][1] == "v":
                print("""
Oque voce deseja fazer cm essa tarefa:

[1] Desmarcar como concluido
[2] Excluir    

                """)
            marc_ou_exc = int(input("---> "))

            if total[escolha - 1][1] == "f":
               dv_f("v")


            elif total[escolha - 1][1] == "v":
                dv_f("f")

        elif escolha == 0:
            print(100 * '\n')
            print("Crie uma nova tarefa:\n\n")
            tarefa = str(input("Tarefa: "))
            dPy_lis(tarefa,"f")

    else:
        print("Crie a sua primeira tarefa:\n")
        tarefa = str(input("Tarefa: "))
        dPy_lis(tarefa, "f")

    comando = "DELETE FROM usuarios"
    cursor.execute(comando)
    for  lista in total:

        comand = f'INSERT INTO usuarios (Tarefa, marcado) VALUE ("{lista[0]}","{lista[1]}")'
        cursor.execute(comand)

    conex.commit()  # editar o Banco de dados






