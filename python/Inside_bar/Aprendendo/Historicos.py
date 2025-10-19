import os
import pandas as pd

CSV_DIR = "csv"  
os.makedirs(CSV_DIR, exist_ok=True)


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")
# ==========================
# FUNÇÕES DE GESTÃO DE CSV
# ==========================
def listar_csvs():
    arquivos = [f for f in os.listdir(CSV_DIR) if f.endswith(".csv")]

    if not arquivos:
        print("⚠️ Nenhum arquivo CSV encontrado.")
    else:
        print("\n📂 Arquivos CSV disponíveis:")
        for i, arq in enumerate(arquivos, 1):
            print(f"{i}. {arq}")
    return arquivos

def visualizar_csv(nome_arquivo):
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, nome_arquivo))

        print(f"\n📊 Conteúdo do arquivo: {nome_arquivo}")
        print(df.to_string(index=False))
    except Exception as e:
        print(f"⚠️ Erro ao abrir {nome_arquivo}: {e}")

def excluir_csv(nome_arquivo):
    try:
        os.remove(os.path.join(CSV_DIR, nome_arquivo))

        print(f"🗑️ Arquivo {nome_arquivo} excluído com sucesso.")
    except Exception as e:
        print(f"⚠️ Erro ao excluir {nome_arquivo}: {e}")

# ==========================
# LOBBY DE CSV
# ==========================
def lobby():
    while True:
        clear_terminal()
        print("\n==============================")
        print("📌 LOBBY DE GERENCIAMENTO CSV")
        print("==============================")
        print("1 - Listar arquivos CSV")
        print("2 - Visualizar registros")
        print("3 - Excluir arquivo")
        print("4 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            clear_terminal()
            listar_csvs()
            input("")
        elif opcao == "2":
            clear_terminal()
            arquivos = listar_csvs()
            if arquivos:
                escolha = input("Digite o número do arquivo para visualizar: ")
                if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos):
                    visualizar_csv(arquivos[int(escolha)-1])
                    input("")
                else:
                    print("⚠️ Número inválido.")
        elif opcao == "3":
            clear_terminal()
            arquivos = listar_csvs()
            if arquivos:
                escolha = input("Digite o nome do arquivo para excluir: ")
                if escolha in arquivos:
                    confirmar = input(f"Tem certeza que deseja excluir {escolha}? (s/n): ")
                    if confirmar.lower() == "s":
                        excluir_csv(escolha)
                else:
                    print("⚠️ Arquivo não encontrado.")
        elif opcao == "4":
            clear_terminal()
            print("👋 Saindo do lobby...")
            break
        else:
            print("⚠️ Opção inválida, tente novamente.")

if __name__ == "__main__":
    lobby()
