import csv
import os

arquivo = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_filtro_back_test.csv"

# Criar o arquivo se não existir
if not os.path.exists(arquivo):
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["periodo", "periodo_01","intervalo", "intervalo_01"])  # cabeçalho

print("=== Sistema de Cadastro em CSV ===")
print("Digite 'excluir' para remover alguém ou 'sair' para encerrar.\n")

while True:
    periodo = input("Periodo: ").strip()

    if periodo.lower() == "sair":
        print("Encerrando programa...")
        break

    elif periodo.lower() == "excluir":
        alvo = input("Digite o nome que deseja excluir: ").strip()

        linhas = []
        removido = False

        with open(arquivo, "r", newline="", encoding="utf-8") as f:
            leitor = csv.reader(f)
            for linha in leitor:
                if linha and linha[0] != alvo:
                    linhas.append(linha)
                elif linha and linha[0] == alvo:
                    removido = True

        with open(arquivo, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerows(linhas)

        if removido:
            print(f"✅ '{alvo}' foi removido.")
        else:
            print(f"❌ '{alvo}' não encontrado.")

    else:
        idade = input("Idade: ").strip()

        if idade.lower() == "excluir":
            alvo = input("Digite a idade que deseja excluir: ").strip()

            linhas = []
            removido = False

            with open(arquivo, "r", newline="", encoding="utf-8") as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    if linha and linha[1] != alvo:
                        linhas.append(linha)
                    elif linha and linha[1] == alvo:
                        removido = True

            with open(arquivo, "w", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerows(linhas)

            if removido:
                print(f"✅ Registros com idade '{alvo}' foram removidos.")
            else:
                print(f"❌ Nenhuma pessoa com idade '{alvo}' encontrada.")
        else:
            # Adicionar novo registro
            with open(arquivo, "a", newline="", encoding="utf-8") as f:
                escritor = csv.writer(f)
                escritor.writerow([nome, idade])
            print(f"Adicionado: {nome} - {idade} anos")
