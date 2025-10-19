import os
import time
import pandas as pd
from datetime import datetime,timedelta
import pytz

# ==========================
# CONFIGURAÇÕES
# ==========================
CSV_DIR = "csv"
os.makedirs(CSV_DIR, exist_ok=True)
PARES = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
REFRESH = 5  # Atualização a cada 5 segundos
tz_sp = pytz.timezone("America/Sao_Paulo")


# ==========================
# FUNÇÕES
# ==========================
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def ler_csv(caminho):
    """
    Lê o CSV atualizado constantemente.
    Retorna None se arquivo não existir ou estiver vazio.
    """
    if not os.path.isfile(caminho):
        return None
    try:
        df = pd.read_csv(caminho, index_col=0, parse_dates=True)
        if df.empty:
            return None
        return df
    except pd.errors.EmptyDataError:
        return None


def verificar_hammer(verify_hammer,poss_tend_compra, poss_tend_venda):
    if verify_hammer == True:
        if poss_tend_compra:
            print("Compra")
            return "Comprar"
        elif poss_tend_venda:
            print("Venda")
            return "Vender"
    else:
        return "None hammer"
    
        
            



# ==========================
# LOOP PRINCIPAL
# ==========================
def main():
    try:
        while True:
            
            clear_terminal()
            print("=" * 60)
            print("📊 MONITOR AO VIVO — HAMMER")
            print("=" * 60)
            
            for par in PARES:
                    
                    hora_agora = datetime.now(tz_sp) - timedelta(minutes=1)
                    min_agora = hora_agora.minute

                    caminho = os.path.join(CSV_DIR, f"dados_{par}.csv")
                    caminho_bb = os.path.join(CSV_DIR, f"dados_bb_{par}.csv")
                    df = ler_csv(caminho)
                    df_bb = ler_csv(caminho_bb)
                    if df is None:
                        return None
                    if df_bb is None:
                        return None
                    
                 
                    #==== Variavel hammer ====

                    #-- Vela ao vivo
                    ultimo = df.iloc[-1]

                    vela_atual_close = ultimo["close"]

                    #-- confirmaçaodo hamer
                    ultimo_2 = df.iloc[-2]
                    
                    vela_close_cheak = ultimo_2["close"]
                    vela_open_cheak = ultimo_2["open"]

                    verify_cor_vela = vela_open_cheak < vela_close_cheak # se for True = vela verde ----- False = vela vermelha

                    #-- hammer
                    ultimo_3 = df.iloc[-3]

                    vela_close = ultimo_3["close"]
                    vela_open = ultimo_3["open"]
                    vela_max = ultimo_3["high"]
                    vela_min = ultimo_3["low"]
                    
                    hora_vela = ultimo_3.name.strftime('%H:%M')
                    tamanho_vela = abs(vela_close - vela_open)

                    shadow_top = 0.125 * tamanho_vela  
                    
                    verify_top_shadow = (vela_max - vela_open) <= shadow_top or vela_max - vela_close <= shadow_top
                    if vela_close > vela_open:
                        verify_lower_shadow_size = vela_open - vela_min > (1.8 * tamanho_vela)
                    else:
                        verify_lower_shadow_size = vela_close - vela_min > (1.8 * tamanho_vela)

                    verify_hammer = verify_top_shadow and verify_lower_shadow_size



                    # ==== RSI e EMA ====
                    ultimo_bb = df_bb.iloc[-1]

                    rsi = ultimo_bb["RSI"]
                    ema = ultimo_bb["EMA"]

                    tend_alta = rsi < 30 and ema > vela_atual_close
                    tend_baixa = rsi > 80 and ema < vela_atual_close
                    # ==== Possibilidades ====

                    poss_tend_compra = ( tend_alta == True and verify_cor_vela == False ) or ( verify_cor_vela == True and tend_baixa==True )
                    
                    poss_tend_venda = ( tend_alta == True and verify_cor_vela == True ) or ( verify_cor_vela == False and tend_baixa == True )
                    


                    valor_hammer = verificar_hammer(verify_hammer, poss_tend_compra, poss_tend_venda)
                    if "Hammer" not in df_bb.columns:
                        df_bb["Hammer"] = "None hammer"
                        
                    df_bb.loc[df_bb.index[-1], "Hammer"] = valor_hammer
                    df_bb.to_csv(caminho_bb)


                    if ultimo is None:
                        print(f"⚠️ {par} ainda não possui dados.")
                        continue
                    
               



                

                    print(f"\n=== {par} ===")
                    print(f"{tamanho_vela:.5f} -- Hora {hora_vela} --- shadow top?: {verify_top_shadow}")
                    print(f"\nClose: {vela_close:.5f}\n")
                    print(f"Hammer : {valor_hammer}")
       
                    
            print(f"\n⌛ Atualizando em {REFRESH}s (CTRL+C para sair)")
            time.sleep(REFRESH)

    except KeyboardInterrupt:
        print("\n🔙 Encerrando Hammer...")

if __name__ == "__main__":
    main()
