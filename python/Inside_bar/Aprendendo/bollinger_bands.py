import os
import time
import pandas as pd
from datetime import datetime,timedelta
import pytz
import csv
CSV_DIR = "csv"  
os.makedirs(CSV_DIR, exist_ok=True)
tz_sp = pytz.timezone("America/Sao_Paulo")

# ==========================
# CONFIGURAÇÕES
# ==========================
PARES = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
PERIODO = 20

DESV = 2
REFRESH = 5

K_PERIOD = 14  # Período %K do Estocástico
D_PERIOD = 3

PERIODO_EMA = 20  # período da EMA (pode mudar depois)



# ==========================
# FUNÇÕES
# ==========================
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

# === Calculos ===
def calcular_bollinger(df):
    mid = df["close"].rolling(PERIODO).mean()
    std = df["close"].rolling(PERIODO).std(ddof=0)
    df["BB_MID"] = mid
    df["BB_UPPER"] = mid + DESV * std
    df["BB_LOWER"] = mid - DESV * std
    return df
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

def calcular_estocastico(df, k_period=K_PERIOD, d_period=D_PERIOD):
    df['Lowest_Low'] = df['low'].rolling(k_period).min()
    df['Highest_High'] = df['high'].rolling(k_period).max()
    df['%K'] = 100 * ((df['close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low']))
    df['%D'] = df['%K'].rolling(d_period).mean()
    return df

def registrar_hammer(caminho,par, verify_hammer,shadow_top,verify_top_shadow,media_hammer,tamanho_martelo,verify_lower_shadow,vela_close,vela_open,vela_min,vela_max):
    

    caminho_csv = os.path.join(CSV_DIR, caminho)                    
    arquivo_existe = os.path.isfile(caminho_csv)                    

    if arquivo_existe:
        df_exist = pd.read_csv(caminho_csv)
        duplicado = ((df_exist["Par"] == par) &
                    (df_exist["Data"] == candle_time.strftime("%Y-%m-%d")) &
                    (df_exist['Hora'] == candle_time.strftime("%H:%M")))
        if duplicado.any():
            return
    
    with open(caminho_csv, mode='a', newline='', encoding='utf-8') as f:
        print("passo 2")
        writer = csv.writer(f)
        
        # se nao existir
        if not arquivo_existe:
            writer.writerow(["Data",
                             "Hora", 
                             "Par",
                             "Verify_Hammer",
                             "shadow_top",
                             "verify_top_shadow",
                             "media_hammer",
                             "tamanho_martelo",
                             "verify_lower_shadow",
                             "close",
                             "open",
                             "min",
                             "max"])

        writer.writerow([candle_time.strftime("%Y-%m-%d"),
                         candle_time.strftime("%H:%M"), 
                         par,
                         verify_hammer,
                         shadow_top,
                         verify_top_shadow,
                         media_hammer,
                         tamanho_martelo,
                         verify_lower_shadow,
                         vela_close,
                         vela_open,
                         vela_min,
                         vela_max])

    print(f"[{par}] Registro adicionado: {candle_time.strftime('%H:%M')} -> AVALIAR HAMMER")
    return
    
def verificar_hammer(ultimo_2,ultimo_3,rsi,ema, vela_atual_close,df,par):

    vela_close_cheak = ultimo_2["close"]
    vela_open_cheak = ultimo_2["open"]

    verify_cor_vela = vela_open_cheak < vela_close_cheak # se for True = vela verde ----- False = vela vermelha

    #-- hammer

    vela_close = ultimo_3["close"]
    vela_open = ultimo_3["open"]
    vela_max = ultimo_3["high"]
    vela_min = ultimo_3["low"]
    
    hora_vela = ultimo_3.name.strftime('%H:%M')
    tamanho_vela = abs(vela_close - vela_open)
    tamanho_martelo = vela_max - vela_min

    media_tamanho_total = (df["high"].iloc[-20:] - df["low"].iloc[-20:]).mean() # media ultimas 20 velas
    
            
    shadow_top = 0.1 * tamanho_vela  
    
    verify_top_shadow = (vela_max - vela_open) <= shadow_top or (vela_max - vela_close) <= shadow_top
    if vela_close > vela_open:
        verify_lower_shadow_size = vela_open - vela_min > (1.8 * tamanho_vela)
    else:
        verify_lower_shadow_size = vela_close - vela_min > (1.8 * tamanho_vela)

    verify_hammer = verify_top_shadow and verify_lower_shadow_size



    tend_alta = rsi < 50 and ema > vela_atual_close
    tend_baixa = rsi > 50 and ema < vela_atual_close
    # ==== Possibilidades ====

                                    #            VEMELHA                                           VERDE
                                    # Rsi < 50  --- E --- EMA (ALTO ↑)             Rsi > 50  --- E --- EMA (BAiXO ↓)     
    poss_tend_compra = ( tend_alta == True and verify_cor_vela == False ) or ( verify_cor_vela == True and tend_baixa==True )

                                    #           VERDE                                           VERMELHA
                                    # Rsi < 50  --- E --- EMA (ALTO ↑)             Rsi > 50  --- E --- EMA (BAiXO ↓)
    poss_tend_venda = ( tend_alta == True and verify_cor_vela == True ) or ( verify_cor_vela == False and tend_baixa == True )

   
    
    if verify_hammer == True:
        if poss_tend_compra:
            print("Compra")
            return "Comprar ↑"
        elif poss_tend_venda:
            print("Venda")
            return "Vender ↓"
        else:
            return "Indefinido x"
    else:
        caminho = "Nada.csv"
        media_hammer = tamanho_martelo < 1.2 * media_tamanho_total

        if verify_top_shadow and verify_lower_shadow_size == False:
                caminho = "hammer_debug_lower_False.csv"
        elif verify_top_shadow == False and verify_lower_shadow_size:
                caminho = "hammer_debug_top_False.csv"
        elif verify_top_shadow == False and verify_lower_shadow_size == False:
                caminho = "hammer_debug_AMBOS_False.csv"
        elif media_hammer == False:
                caminho = "Media_hammer.csv"
       
        
        registrar_hammer(
            caminho,
            par,
            verify_hammer,
            shadow_top,    
            verify_top_shadow,
            media_hammer,
            tamanho_martelo,
            verify_lower_shadow_size,
            vela_close,
            vela_open,
            vela_min,
            vela_max
            )
        return "None hammer"
    




def ler_csv(caminho):
    if not os.path.isfile(caminho):
        print(f"⚠️ {caminho} não encontrado ainda...")
        return None
    try:
        df = pd.read_csv(caminho, index_col=0, parse_dates=True)
        if df.empty:
            print(f"⚠️ {caminho} está vazio...")
            return None
        return df
    except pd.errors.EmptyDataError:
        print(f"⚠️ {caminho} está vazio ou inválido...")
        return None

# ==========================
# LOOP PRINCIPAL
# ==========================
def main():
    try:
        while True:
            largura_terminal = os.get_terminal_size().columns
            hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
            seg_agora = hora_agora.second
            min_agora = hora_agora.minute
            while hora_agora.hour >= 1 and hora_agora.hour < 2:
                clear_terminal()
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
                hora_iq = hora_agora.strftime("%H:%M:%S")
                print("\n", hora_iq.center(largura_terminal))
                print("HORARIO INAPROPRIADO....\n (horas inapropiadas: 1am a 2am)")
            
                time.sleep(60)
            
            while 22 < seg_agora <=28: 
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
                seg_agora = hora_agora.second
                print("Realinhando Programas..")
                if seg_agora > 28:
                    continue

            clear_terminal()
            print("=" * 60)
            print("📊 MONITOR AO VIVO — BOLLINGER BANDS")
            print("=" * 60)

            for par in PARES:
                global candle_time
                script_dir = os.path.dirname(os.path.abspath(__file__))
                caminho = os.path.join(CSV_DIR, f"dados_{par}.csv")

                
                df = ler_csv(caminho)
                if df is None:
                    continue  # pula para o próximo par
                
                df = calcular_bollinger(df)
                df["RSI"] = calcular_rsi_wilder(df['close'])
                df = calcular_estocastico(df)
                df["EMA"]= df["close"].ewm(span=PERIODO_EMA, adjust=False).mean()
                
                candle_time = df.index[-1]
                try:
                    
                    hammer_result = verificar_hammer(
                                                df.iloc[-2], 
                                                df.iloc[-3],
                                                df["RSI"].iloc[-2], 
                                                df["EMA"].iloc[-2], 
                                                df["close"].iloc[-2],
                                                df,
                                                par
                    )
                except Exception as e:
                    # Em caso de erro inesperado, evita quebrar o loop e registra None
                    print(f"Erro ao verificar hammer para {par}: {e}")
                    hammer_result = "None hammer"   
                df.loc[df.index[-1], "Hammer"] = hammer_result

                
                
                df.to_csv(os.path.join(CSV_DIR, f"dados_bb_{par}.csv"))
                
               
                ultimo = df.iloc[-1]
                print(f"\n=== {par} ===")
                print(f" Close : {ultimo['close']:.5f}")
                print(f" BB_UP : {ultimo['BB_UPPER']:.5f}")
                print(f" BB_MID: {ultimo['BB_MID']:.5f}")
                print(f" BB_LOW: {ultimo['BB_LOWER']:.5f}")
                print(f"\n RSI {ultimo['RSI']:.0f}")
                print(f"\n %K : {ultimo['%K']:.2f}")
                print(f" %D : {ultimo['%D']:.2f}")
                print(f" EMA: {ultimo['EMA']:.5f}")
                print(f" Hammer: {ultimo['Hammer']}")

            print(f"\n⌛ Atualizando em {REFRESH}s (CTRL+C para sair)")
            time.sleep(REFRESH)

    except KeyboardInterrupt:
        print("\n🔙 Encerrando cálculos de Bollinger...")

if __name__ == "__main__":
    main()
