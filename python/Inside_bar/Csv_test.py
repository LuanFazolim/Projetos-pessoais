import csv

# Lista de dados
lista = [['ola', 2, 4], ['thau', 1, 3]]

# Nome do arquivo CSV
arquivo = "D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\dados.csv"

# Cabeçalhos das colunas
cabecalhos = ['thauorola', 'quantidade', 'pessoa']

# Criação do arquivo CSV
with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(cabecalhos)  # Escreve o cabeçalho
    writer.writerows(lista)      # Escreve todas as linhas da lista

print(f"Arquivo '{arquivo}' criado com sucesso!")
