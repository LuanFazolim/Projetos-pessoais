import os
import time
import pandas as pd

# ==========================
# CONFIGURAÇÕES
# ==========================
PARES = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
RSI_PERIOD = 14
REFRESH = 5
BASE_DIR = os.getcwd()  # garante salvar no mesmo diretório
CSV_DIR = "csv"  
os.makedirs(CSV_DIR, exist_ok=True)

# ==========================
# FUNÇÕES
# ==========================
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def calcular_rsi_wilder(close, period=14):
    delta = close.diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    # Suavização de Wilder (mais comum para RSI)
    avg_ganho = ganho.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    avg_perda = perda.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs = avg_ganho / avg_perda
    rsi = 100 - (100 / (1 + rs))
    return rsi

# ==========================
# LOOP PRINCIPAL
# ==========================
def main():
    try:
        while True:
            clear_terminal()
            print("=" * 60)
            print("📊 MONITOR AO VIVO — RSI (Wilder)")
            print("=" * 60)

            for par in PARES:
                caminho_in = os.path.join(CSV_DIR, f"dados_{par}.csv")
                if not os.path.isfile(caminho_in):
                    print(f"⚠️ {caminho_in} não encontrado ainda...")
                    continue

                # Proteção contra arquivo vazio/corrompido
                try:
                    df = pd.read_csv(caminho_in, index_col=0, parse_dates=True)
                except pd.errors.EmptyDataError:
                    print(f"⚠️ {caminho_in} está vazio/ inválido...")
                    continue

                if df.empty or df["close"].isna().all():
                    print(f"⚠️ {caminho_in} sem dados úteis...")
                    continue

                # Garante quantidade mínima de candles
                if len(df) < RSI_PERIOD + 1:
                    faltam = RSI_PERIOD + 1 - len(df)
                    print(f"{par}: aguardando +{faltam} candles para calcular RSI...")
                    continue

                df["RSI"] = calcular_rsi_wilder(df["close"], RSI_PERIOD)

                caminho_out = os.path.join(CSV_DIR, f"dados_rsi_{par}.csv")

                df[["close", "RSI"]].to_csv(caminho_out)

                ultimo = df.iloc[-1]
                rsi_ult = ultimo["RSI"]
                rsi_txt = f"{rsi_ult:.2f}" if pd.notna(rsi_ult) else "NaN"

                print(f"\n=== {par} ===")
                print(f" Close: {ultimo['close']:.5f}")
                print(f" RSI  : {rsi_txt}")
                print(f" 💾 RSI salvo em: {os.path.abspath(caminho_out)}")

            print(f"\n⌛ Atualizando em {REFRESH}s (CTRL+C para sair)")
            time.sleep(REFRESH)
    except KeyboardInterrupt:
        print("\n🔙 Encerrando cálculos de RSI...")

if __name__ == "__main__":
    main()
