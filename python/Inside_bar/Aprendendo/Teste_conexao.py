import os
import time
import csv
import pandas as pd
import pytz
from datetime import datetime, timedelta
import pyautogui as pyg

# ==========================
# CONFIGURAÇÕES
# ==========================
PARES = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
cont_apll = 0
REFRESH = 5
CSV_DIR = "csv"  
os.makedirs(CSV_DIR, exist_ok=True)
tz_sp = pytz.timezone("America/Sao_Paulo")

# ==========================
# FUNÇÕES AUXILIARES
# ==========================
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def registrar_horario_debug(par, Posicao, BGB, RSI, STOCH, STOCH_cruzado, EMA,candle_time,Hammer):
    
  
    caminho_csv = os.path.join(CSV_DIR, "horarios_calculos.csv")

    arquivo_existe = os.path.isfile(caminho_csv)

    if arquivo_existe:
        df_exist = pd.read_csv(caminho_csv)
        duplicado = ((df_exist["Par"] == par) &
                    (df_exist["Data"] == candle_time.strftime("%Y-%m-%d")) &
                    (df_exist['Hora'] == candle_time.strftime("%H:%M")))
        if duplicado.any():
            return

    with open(caminho_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # se nao existir
        if not arquivo_existe:
            writer.writerow(["Data","Hora", "Par","Posicao","BGB", "RSI", 'STOCH', "STOCH_cruzado","EMA","Hammer"])

        writer.writerow([candle_time.strftime("%Y-%m-%d"),candle_time.strftime("%H:%M"), par,Posicao, BGB, RSI, STOCH, STOCH_cruzado, EMA,Hammer])

    print(f"[{par}] Registro adicionado: {candle_time.strftime('%H:%M')} -> AVALIAR CALCULOS")

    

def registrar_horario(par, result, candle_time, Hammer):
    global cont_apll

    caminho_csv = os.path.join(CSV_DIR, "horarios.csv")
    arquivo_existe = os.path.isfile(caminho_csv)


    if arquivo_existe:
        df_exist = pd.read_csv(caminho_csv)
        duplicado = ((df_exist["Par"] == par) &
                        (df_exist["Data"] == candle_time.strftime("%Y-%m-%d")) &
                        (df_exist["Hora"] == candle_time.strftime("%H:%M")))
        if duplicado.any():
            return
    with open(caminho_csv, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not arquivo_existe:
            writer.writerow(["Data", "Hora", "Par", "Resultado", "Hammer"])
        writer.writerow([candle_time.strftime("%Y-%m-%d"),
                     candle_time.strftime("%H:%M"), par, result, Hammer])
    print(f"[{par}] Registro adicionado: {candle_time.strftime('%Y-%m-%d %H:%M')} -> {result}")
    cont_apll += 1
    if Hammer != "None hammer":
    
        pyg.write(f'=== {par} {result} Hammer: {Hammer}===')
    else:
        pyg.write(f'=== {par} {result} ===')
    time.sleep(2)
    pyg.press('enter')




def avaliar_csv_exis(caminho):
    if not os.path.isfile(caminho):
        print(f"⚠️ Arquivo {caminho} não encontrado ainda...")     
        return avaliar_csv_exis(caminho)

    try:
        df = pd.read_csv(caminho, index_col=0, parse_dates=True)
    except pd.errors.EmptyDataError:
        print(f"⚠️ Arquivo {caminho} está vazio ou inválido...")
        return avaliar_csv_exis(caminho)

    if df.empty:
        print(f"⚠️ Arquivo {caminho} está vazio...")
        return avaliar_csv_exis(caminho)

    return df

    # ==========================
# LOOP PRINCIPAL
# ==========================

def main():
    global cont_apll
    try:
        
        while True:
            # Hora atual ajustada para IQ Option
            largura_terminal = os.get_terminal_size().columns
            hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
            seg_agora = hora_agora.second
            min_agora = hora_agora.minute
            
            hora_iq = hora_agora.strftime("%H:%M:%S")
                
            while hora_agora.hour >= 1 and hora_agora.hour < 2:
                clear_terminal()
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
                hora_iq = hora_agora.strftime("%H:%M:%S")
                print("\n", hora_iq.center(largura_terminal))
                print("HORARIO INAPROPRIADO....\n (horas inapropiadas: 1am a 2am)")
            
                time.sleep(60)

            while 24 < seg_agora <= 30 : 
                hora_agora = datetime.now(tz_sp) - timedelta(minutes=1,seconds=20)
                seg_agora = hora_agora.second
                print("Realinhando Programas..")
                if seg_agora > 30:
                    continue
            
            
            clear_terminal()

            print("=" * (int(largura_terminal)))
            print("📊 MONITOR AO VIVO — LOBBY (SINAIS)".center(largura_terminal))
            print("=" * (int(largura_terminal)))
            print(hora_agora)

            for par in PARES:
                
                
                if par == "EURUSD-OTC":
                    print("\n", hora_iq.center(largura_terminal))
                    # 🔹 Proteção contra arquivo vazio ou inválido

                #====---API Avaliar---====
                caminho_dados = os.path.join(CSV_DIR, f"dados_{par}.csv")
                df_dados = avaliar_csv_exis(caminho_dados)
                if df_dados is None:
                    continue 
             

                #====---BB Avaliar---====
                caminho_bb = os.path.join(CSV_DIR, f"dados_bb_{par}.csv")
                df_bb = avaliar_csv_exis(caminho_bb)
                if df_bb is None:
                    continue 

                if "Hammer" not in df_bb.columns:
                    df_bb["Hammer"] = "None hammer"
                    df_bb.to_csv(caminho_bb)
                

                ultimo_bb = df_bb.iloc[-1]
                ultimo_dados = df_dados.iloc[-1]
                candle_time = df_bb.index[-1]
                print(candle_time)
                

                # Pega também o penúltimo candle para detectar cruzamento K/D
                penultimo = df_bb.iloc[-2]  # assumindo que %K e %D estão salvos no df_bb


                # === variaveis para o IF ===
                difer_lower = ultimo_bb["BB_LOWER"] - ultimo_dados["close"]
                difer_upper = ultimo_dados["close"] - ultimo_bb["BB_UPPER"]

                dentro_verify = ultimo_bb["BB_LOWER"] < ultimo_dados["close"] < ultimo_bb["BB_UPPER"]
                lower_verify = ultimo_dados["close"] < ultimo_bb["BB_LOWER"]
                upper_verify = ultimo_dados["close"] > ultimo_bb["BB_UPPER"]

                num_difer = 0.015 if par == "USDJPY-OTC" else 0.0015



                K_atual = ultimo_bb["%K"]
                D_atual = ultimo_bb["%D"]
                K_anterior = penultimo["%K"]
                D_anterior = penultimo["%D"]

                global difer_LU
            
                # Cruzamento K/D para compra/venda
                cruzou_para_cima = K_anterior < D_anterior and K_atual > D_atual
                cruzou_para_baixo = K_anterior > D_anterior and K_atual < D_atual
                global cruzou_low_upp
                cruzou_low_upp = f'Baixo ↓ {cruzou_para_baixo}'

                if cruzou_para_baixo == True:
                    cruzou_low_upp = f'Baixo ↓ {cruzou_para_baixo}'
                elif cruzou_para_cima == True:
                    cruzou_low_upp = f'Cima ↑ {cruzou_para_cima}'
                else:
                    cruzou_low_upp = "False"


                #================ PRINTS ================
                print((6*"=-=").center(largura_terminal))
                print(f"|   {par}   |".center(largura_terminal))
                print((6*"=-=").center(largura_terminal))

                #-- Vela
                print("Último Close: %.5f".center(largura_terminal) % ultimo_dados["close"])

                #-- diferencia
                if difer_lower < 0 and difer_upper < 0:
                    print("- Difer < 0".center(largura_terminal))
                    difer_LU = f'Difer < 0'
                
                else:
                   

                    if difer_lower > difer_upper: 
                        if num_difer > difer_lower > 0:
                            print(f"- Difer_Lower: {difer_lower:.3f}".center(largura_terminal) )
                            difer_LU = f'Lower: {difer_lower:.5f}'

                    elif difer_lower < difer_upper:
                        if num_difer > difer_lower > 0:
                            print(f"- Difer_Upper: {difer_upper:.3f}".center(largura_terminal) )
                            difer_LU = f'Upper: {difer_upper:.5f}'
                
                #-- RSi
                print(f"- RSI: {ultimo_bb['RSI']:.0f}".center(largura_terminal))

                #-- Estocastico
                if cruzou_para_cima:
                    print(f"- Cruzou: Cima ↑".center(largura_terminal))
                elif cruzou_para_baixo:
                    print(f"- Cruzou: baixo ↓".center(largura_terminal))
                else:
                    print("- Cruzou: False".center(largura_terminal))

                print(f"- K%: {K_atual:.1f}".center(largura_terminal))

                #-- EMA
                EMA = 'Center ---'
                if ultimo_bb['EMA'] > ultimo_dados["close"]:
                    print(f"- EMA: {ultimo_bb['EMA']:.5f} ↑".center(largura_terminal)) 
                    EMA = "Cima ↑"
                elif ultimo_bb['EMA'] < ultimo_dados["close"]:
                    print(f"- EMA: {ultimo_bb['EMA']:.5f} ↓".center(largura_terminal)) 
                    EMA = "Baixo ↓"
                
                print("\n")

                #-- Posição
                Posicao = '--- (Dentro)'
                if dentro_verify:
                    print("Posição: --- (Dentro)".center(largura_terminal))
                    Posicao = '--- (Dentro)'

                elif lower_verify:
                    print("Posição: ↓ (Baixo)".center(largura_terminal))
                    Posicao = '↓ (Baixo)'
                
                elif upper_verify:
                    print("Posição: ↑ (Cima)".center(largura_terminal))
                    Posicao = '↑ (Cima)'
                #-- Hammer    
                print(f"- Hammer: {ultimo_bb['Hammer']}".center(largura_terminal))

                #=============================================

                

                #================ Verificar Aplicaçao ================
                #                                   4:55                               ------                       5:05
                if (min_agora == 0 or min_agora%5 == 0) and seg_agora <= 10 :

                    # ↓ (Baixo)
                    if ultimo_dados["close"] < ultimo_bb["BB_LOWER"]:
                        # Condição RSI + Bollinger
                        registrar_horario_debug(
                                                par,
                                                Posicao,
                                                difer_LU,
                                                f"{ultimo_bb['RSI']:.1f}",
                                                f"{ultimo_bb['%K']:.1f}",
                                                cruzou_low_upp,
                                                EMA,
                                                candle_time,
                                                ultimo_bb["Hammer"])   #par, Posicao, BGB, RSI, STOCH, STOCH_cruzado, EMA,candle_time)
                        if difer_lower >= num_difer and ultimo_bb["RSI"] < 45:
                           
                            # Sinal de compra se K < 20 ou cruzamento confirmado
                            if (K_atual < 20 or cruzou_para_cima) and ultimo_bb["EMA"] > ultimo_dados["close"]:
                                registrar_horario(par, "Compra ↑", candle_time, ultimo_bb["Hammer"])
                                print(f"Sinal de COMPRA confirmado com Estocástico: %K={K_atual:.2f}, %D={D_atual:.2f}")

                
                
                    # ↑ (Cima)
                    elif ultimo_dados["close"] > ultimo_bb["BB_UPPER"]:
                        registrar_horario_debug(
                                                par,
                                                Posicao,
                                                difer_LU,
                                                f"{ultimo_bb['RSI']:.1f}",
                                                f"{ultimo_bb['%K']:.1f}",
                                                cruzou_low_upp,
                                                EMA,
                                                candle_time,
                                                 ultimo_bb["Hammer"] )   #par, Posicao, BGB, RSI, STOCH, STOCH_cruzado, EMA,candle_time)
                        if difer_upper >= num_difer and ultimo_bb["RSI"] > 55:
                            
                            # Sinal de venda se K > 80 ou cruzamento confirmado
                            if (K_atual > 80 or cruzou_para_baixo) and ultimo_bb["EMA"] < ultimo_dados["close"]:
                                registrar_horario(par, "Venda ↓", candle_time,ultimo_bb["Hammer"])
                                print(f"Sinal de VENDA confirmado com Estocástico: %K={K_atual:.2f}, %D={D_atual:.2f}")

                    #verificar hammer
                    if ultimo_bb["Hammer"] != "None hammer":
                        registrar_horario_debug(
                                                par,
                                                Posicao,
                                                   difer_LU,
                                                f"{ultimo_bb['RSI']:.1f}",
                                                f"{ultimo_bb['%K']:.1f}",
                                                cruzou_low_upp,
                                                EMA,
                                                candle_time ,
                                                ultimo_bb["Hammer"])
                        registrar_horario(par, "---", candle_time,ultimo_bb["Hammer"])         
                #=====================================================

                    print("Fazendo a avaliação...")
                print("\n",largura_terminal*"-","\n")
            print(f"{cont_apll} Aplicações totais".center(largura_terminal))
            print(f"\n⌛ Atualizando em {REFRESH}s (CTRL+C para sair)")
            
            time.sleep(REFRESH)
    except KeyboardInterrupt:
        print("\n🔙 Encerrando lobby...")

if __name__ == "__main__":
    main()
