import pandas as pd
import os
import csv
import matplotlib.pyplot as plt

csv_file = 'historico_operacoes.csv'

def limpar_csv():
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['moeda', 'data', 'hora', 'resultado', 'candles', 'dinheiro_entrada', 'lucro', 'total_acumulado', 'dinheiro_total'])
    print("\n[INFO] Todos os dados foram removidos com sucesso.\n")

def ler_e_mostrar_csv():
    try:
        pd.set_option('display.max_rows', None)
        df = pd.read_csv(csv_file)
       

        if df.empty:
            print("[INFO] O arquivo está vazio.\n")
            return

        print("\n=== Histórico de Operações ===\n")
        print(df)

        total = df['lucro'].sum()
        acertos = df[df['resultado'] == 'acerto'].shape[0]
        total_ops = df.shape[0]
        taxa_acerto = (acertos / total_ops) * 100 if total_ops > 0 else 0

        print("\n=== Estatísticas ===")
        print(f"Total de Operações: {total_ops}")
        print(f"Acertos: {acertos}")
        print(f"Taxa de Acerto: {taxa_acerto:.2f}%")
        print(f"Lucro Total: R$ {total:.2f}\n")
    
    except FileNotFoundError:
        print(f"[ERRO] Arquivo '{csv_file}' não encontrado.\n")
    except Exception as e:
        print(f"[ERRO] Erro ao ler o CSV: {e}\n")

def mostrar_grafico_lucro_diario():
    try:
        df = pd.read_csv(csv_file)
        if df.empty:
            print("[INFO] Arquivo vazio, sem dados para o gráfico.\n")
            return

        df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')
        lucro_por_dia = df.groupby(df['data'].dt.date)['lucro'].sum()

        if lucro_por_dia.empty:
            print("[INFO] Nenhuma informação de lucro encontrada.\n")
            return

        print("\n=== Datas Disponíveis ===")
        for i, data in enumerate(lucro_por_dia.index, 1):
            print(f"[{i}] {data.strftime('%d/%m/%y')}")

        print("[0] Voltar")

        escolha = input("\nEscolha a data para exibir o gráfico ou digite 0 para voltar: ").strip()

        if escolha == '0':
            return

        try:
            escolha_int = int(escolha) - 1
            if 0 <= escolha_int < len(lucro_por_dia):
                
                data_selecionada = list(lucro_por_dia.index)[escolha_int]
                print(data_selecionada)

                # Formata todas as horas do DataFrame geral
                df['hora_formatada'] = df['hora'].apply(lambda x: x[:5] if isinstance(x, str) else str(x)[:5])

                # Pega todos os horários únicos existentes
                todos_horarios = sorted(df['hora_formatada'].unique())

                # Filtra apenas os dados do dia selecionado
                df_filtrado = df[df['data'].dt.date == data_selecionada]
                df_filtrado['hora_formatada'] = df_filtrado['hora'].apply(lambda x: x[:5] if isinstance(x, str) else str(x)[:5])

                

                # Agrupa por horário e soma os lucros (caso tenha mais de um no mesmo horário)
                df_grouped = df_filtrado.groupby('hora_formatada')['lucro'].sum()

                # Reindexa para ter todos os horários (preenche ausentes com 0)
                df_reindexado = df_grouped.reindex(todos_horarios, fill_value=0)

                # Calcula lucro acumulado
                lucro_acumulado = df_reindexado.cumsum()

                # === Gráfico ===
                plt.figure(figsize=(12, 5))

                # Plota a linha geral (sem bolinhas em tudo)
                plt.plot(df_reindexado.index, lucro_acumulado, linestyle='-', color='blue', label='Lucro Acumulado')
                

                # Marca apenas os pontos com alteração de lucro (ou seja, lucro ≠ 0 no horário original)
                pontos_com_operacao = df_grouped.index  
                lucro_com_operacao = lucro_acumulado[pontos_com_operacao]
                plt.scatter(pontos_com_operacao, lucro_com_operacao, color='red', zorder=5)

                # Estética
                plt.title(f"Lucro Acumulado - {data_selecionada.strftime('%d/%m/%y')}")
                plt.xlabel("Hora")
                plt.ylabel("Lucro Acumulado (R$)")
                # Mostrar menos horários para espaçar os ticks
                espacamento = max(1, len(df_reindexado.index) // 15)  # Mostra cerca de 15 horários no eixo
                xticks_indices = list(range(0, len(df_reindexado.index), espacamento))
                xticks_labels = [df_reindexado.index[i] for i in xticks_indices]

                plt.xticks(xticks_labels, rotation=45)

                plt.grid(True)
                plt.tight_layout()
                plt.legend()
                plt.savefig('D:\programacao\Python\IA\Bot_iq_option\Graficos\semana 1 (01.07.25 -- 04.07.25)\save.png')
                print("salvo nos arquivos..")
                plt.show()


            else:
                print("[ERRO] Número inválido.\n")
        except ValueError:
            print("[ERRO] Entrada inválida.\n")
        
    except Exception as e:
        print(f"[ERRO] Erro ao gerar gráfico: {e}\n")

def menu():
    while True:
        print("=== MENU PRINCIPAL ===")
        print("1. Ver Histórico de Operações")
        print("2. Limpar CSV")
        print("3. Ver Gráfico de Lucro Diário")
        print("4 Sair")
        
        escolha = input("Escolha uma opção (1/2/3/4): ").strip()

        if escolha == '1':
            ler_e_mostrar_csv()
        elif escolha == '2':
            limpar_csv()
        elif escolha == '3':
            mostrar_grafico_lucro_diario()
        elif escolha == '4':
            print("Encerrando programa.")
            break
        else:
            print("[ERRO] Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    if not os.path.exists(csv_file):
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['moeda', 'data', 'hora', 'resultado', 'candles', 'dinheiro_entrada', 'lucro', 'total_acumulado', 'dinheiro_total'])

    menu()
