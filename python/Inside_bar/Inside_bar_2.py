import pandas as pd
import yfinance as yf

naotem = []
tem = []
# Lê o CSV
df = pd.read_csv(
    r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\todas_acoes.csv",
    sep=';',
    encoding='latin1',
    low_memory=False,
    skiprows=1
)
df.columns = df.columns.str.strip()

coluna = "Asst"

i = 0
while i < len(df):
    i += 1 # só avança se a linha não foi removida
    print(len(df))
    print(tem)
    valor = df.iloc[i][coluna]
    ticker = valor if valor.endswith('.SA') else f"{valor}.SA"

    try:
        # Pula tickers que já deram erro
        if ticker in naotem or ticker in tem:
            print(f"⚠️ Nenhum dado encontrado para: {ticker}. Linha será removida.")
            df = df.drop(df.index[i])
            df = df.reset_index(drop=True)
            continue  # não incrementa i, próxima linha assume o índice
      
        # Baixa dados do Yahoo Finance
        dados = yf.download(tickers=ticker, period='1y', interval='1h')

        if dados.empty:
            print(f"⚠️ Nenhum dado encontrado para: {ticker}. Linha será removida.")
            df = df.drop(df.index[i])
            df = df.reset_index(drop=True)
            naotem.append(ticker)
            # não incrementa i
        else:
            print(dados.iloc[0:3])
            
            tem.append(ticker)
    except Exception as e:
        print(f"❌ Erro ao baixar {valor}: {e}")
        df = df.drop(df.index[i])
        df = df.reset_index(drop=True)
        naotem.append(ticker)
        # não incrementa i

# Salva no final
dff = pd.DataFrame(tem,columns=["Tikers"])
dff.to_csv(r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\todas_acoes_filtradas.csv", index=False)
print("✅ Arquivo salvo como 'todas_acoes_filtradas.csv'")



''' if isinstance(valor, str) and "brasil" in valor.lower():
        print(f"Linha {i} contém 'brasil': {valor}")
        # Aqui você pode fazer o que quiser, por exemplo:
        # df.loc[i, 'ContemBrasil'] = True
        # OU pular, modificar, etc.
    else:
        # Linha normal
        pass
# (Opcional) Se quiser criar uma nova coluna marcando as linhas
df["ContemBrasil"] = df[coluna].astype(str).str.contains("brasil", case=False, na=False)

# Salvar o resultado
df.to_csv("CadastroInstrumentosListados_marcado.csv", index=False, sep=';', encoding='latin1')

print("Arquivo salvo com a nova coluna 'ContemBrasil'.")
'''

'''
url = "https://arquivos.b3.com.br/api/download/requestname?fileName=InstrumentsConsolidatedFile&lang=pt"
print("📡 Baixando lista de ações da B3...")

resp = requests.get("https://arquivos.b3.com.br/api/download/requestname?fileName=InstrumentsConsolidatedFile&lang=pt")

if resp.status_code != 200:
    print(f"❌ Erro ao baixar lista da B3 (status {resp.status_code}).")
    acoes_b3 = []
else:
    # A B3 retorna um link para download, então fazemos outro request
    link_download = resp.json().get("redirectUri")

    if not link_download:
        print("❌ Não foi possível obter o link de download da B3.")
        acoes_b3 = []
    else:
        conteudo = requests.get(link_download).content.decode("latin1")
        df = pd.read_csv(StringIO(conteudo), sep=";", on_bad_lines="skip")
        
        # Coluna de símbolos
        if "TckrSymb" in df.columns:
            acoes_b3 = df["TckrSymb"].dropna().unique()
            acoes_b3 = [f"{a}.SA" for a in acoes_b3]
            print(f"✅ Total de ações encontradas: {len(acoes_b3)}")
            print(acoes_b3[:20])
        else:
            print("❌ Coluna 'TckrSymb' não encontrada no arquivo da B3.")
            acoes_b3 = []

# ==========================
# LISTAS DO YFINANCE
# ==========================
periodos = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
intervalos = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]

print("\nPeríodos válidos:")
print(", ".join(periodos))

print("\nIntervalos válidos:")
print(", ".join(intervalos))

# ==========================
# SALVAR EM CSV
# ==========================
if acoes_b3:
    pd.DataFrame({"Ticker": acoes_b3}).to_csv("acoes_b3.csv", index=False, encoding="utf-8-sig")
    print("\n💾 Arquivo 'acoes_b3.csv' salvo com sucesso!")
else:
    print("\n⚠️ Nenhuma ação foi salva porque não foi possível obter a lista.")
'''