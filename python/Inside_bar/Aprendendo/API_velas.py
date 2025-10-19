

import os
import time
import pandas as pd
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime,timedelta
import pytz

# ==========================
# CONFIGURAÇÕES
# ==========================
EMAIL = "Luanfazolim@gmail.com"
SENHA = "Luna@0419"
PARES = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
TIMEFRAME = 60 * 5       # 5 minutos
N_FETCH = 50             # Quantidade de candles
REFRESH = 5              # Atualização em segundos
CSV_DIR = "csv"  
os.makedirs(CSV_DIR, exist_ok=True)
tz_sp = pytz.timezone("America/Sao_Paulo")

# ==========================
# FUNÇÕES
# ==========================
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def conectar_api():
    print("🔌 Conectando à IQ Option...")
    api = IQ_Option(EMAIL, SENHA)
    api.connect()
    if not api.check_connect():
        raise RuntimeError("❌ Falha na conexão com a IQ Option.")
    print("✅ Conectado com sucesso!\n")
    return api

def obter_candles(api, par, n):
    agora = time.time()
    candles = api.get_candles(par, TIMEFRAME, n, agora)
    df = pd.DataFrame(candles)[["from", "open", "max", "min", "close"]]
    df.rename(columns={"from": "time", "max": "high", "min": "low"}, inplace=True)

    df["time"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert("America/Sao_Paulo") 
    print(df.set_index("time").sort_index())
    return df.set_index("time").sort_index()

# ==========================
# LOOP PRINCIPAL
# ==========================
api = conectar_api()
def main():
    
    try:
        while True:
            largura_terminal = os.get_terminal_size().columns
            hora_agora = datetime.now(tz_sp) - timedelta(minutes=1)
            seg_agora = hora_agora.second
            min_agora = hora_agora.minute
            
            while hora_agora.hour >= 1 and hora_agora.hour < 2:
                clear_terminal()
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
                hora_iq = hora_agora.strftime("%H:%M:%S")
                print("\n", hora_iq.center(largura_terminal))
                print("HORARIO INAPROPRIADO....\n (horas inapropiadas: 1am a 2am)")
            
                time.sleep(60)

            while 20 < seg_agora <= 26 : 
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1)
                seg_agora = hora_agora.second
                print("Realinhando Programas..")
                if seg_agora > 26:
                    continue
                
            clear_terminal()
            print("=" * 60)
            print("📊 MONITOR AO VIVO — DADOS DAS MOEDAS")
            print("=" * 60)

            for par in PARES:
                try:
                    df = obter_candles(api, par, N_FETCH)
                    df.to_csv(os.path.join(CSV_DIR, f"dados_{par}.csv"))


                    ultimo = df.iloc[-1]
                    print(f"\n=== {par} ===")
                    print(f" Close: {ultimo['close']:.5f}\n")
                    print(f" Open : {ultimo['open']:.5f}")
                    print(f" High : {ultimo['high']:.5f}")
                    print(f" Low  : {ultimo['low']:.5f}")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao coletar {par}: {e}")

            print(f"\n⌛ Atualizando em {REFRESH}s (CTRL+C para sair)")
            time.sleep(REFRESH)
    except KeyboardInterrupt:
        print("\n🔙 Encerrando coleta...")


if __name__ == "__main__":
    main()
