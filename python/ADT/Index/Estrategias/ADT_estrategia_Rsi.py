# =====================================
#            VARIÁVEIS GLOBAIS
# =====================================
import pandas as pd

Estrategias_arquivo_variaveis = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_estrategias_variaveis.csv"

# ----- RSI -----
periodo = 14
ultimo_close = None
ganho_medio = None
perda_medio = None
ganhos_iniciais = []
perdas_iniciais = []

# ----- EMA -----
ema_periodo = 20
ema_valor = None

ticker = None
periodo_ = None
intervalo = None


# =====================================
#           PROCESSAR RSI
# =====================================
def processar_rsi(close_atual):
    global ultimo_close, ganho_medio, perda_medio
    global ganhos_iniciais, perdas_iniciais

    if ultimo_close is None:
        ultimo_close = close_atual
        return None

    variacao = close_atual - ultimo_close
    ultimo_close = close_atual

    ganho = max(variacao, 0)
    perda = abs(min(variacao, 0))

    # primeiros 14 períodos
    if ganho_medio is None:
        ganhos_iniciais.append(ganho)
        perdas_iniciais.append(perda)

        if len(ganhos_iniciais) < periodo:
            return None

        ganho_medio = sum(ganhos_iniciais) / periodo
        perda_medio = sum(perdas_iniciais) / periodo

    else:
        ganho_medio = (ganho_medio * (periodo - 1) + ganho) / periodo
        perda_medio = (perda_medio * (periodo - 1) + perda) / periodo

    if perda_medio == 0:
        return 100.0

    rs = ganho_medio / perda_medio
    rsi = 100 - (100 / (1 + rs))
    
    return float(rsi)


# =====================================
#           PROCESSAR EMA
# =====================================
def processar_ema(close_atual):
    global ema_valor, ema_periodo

    # smoothing factor
    k = 2 / (ema_periodo + 1)

    if ema_valor is None:
        ema_valor = close_atual  # primeira EMA = close
    else:
        ema_valor = (close_atual - ema_valor) * k + ema_valor

    return float(ema_valor)


# =====================================
#        LOOP PRINCIPAL BACKTEST
# =====================================
def BCKT_estrategia(resultados):
    global ultimo_close, ganho_medio, perda_medio
    global ganhos_iniciais, perdas_iniciais
    global ticker, periodo_, intervalo
    global ema_valor

    df = pd.read_csv(Estrategias_arquivo_variaveis)

    # Se o usuário ativou RSI+EMA no CSV
    usar_rsi_ema = df.loc[df["estrategia"] == "Rsi + EMA", "estrategia_01"].iloc[0]
    usar_rsi_ema = True if usar_rsi_ema == 1 else False

    for item in resultados:
        ticker_atual = item["ticker"]
        periodo_atual = item["periodo"]
        intervalo_atual = item["intervalo"]
        close_atual = float(item["close"])

        # troca de ativo ou período → reset variáveis
        if ticker_atual != ticker or periodo_atual != periodo_ or intervalo_atual != intervalo:
            ticker = ticker_atual
            periodo_ = periodo_atual
            intervalo = intervalo_atual

            ultimo_close = None
            ganho_medio = None
            perda_medio = None
            ganhos_iniciais = []
            perdas_iniciais = []

            ema_valor = None  # reset EMA

        # ---- PROCESSA RSI ----
        rsi = processar_rsi(close_atual)

        # ---- PROCESSA EMA ----
        ema = processar_ema(close_atual) if usar_rsi_ema else None
      
        # RSI ainda calculando
        if rsi is None:
            continue

        # ==============================
        #     REGRAS DE ENTRADA
        # ==============================

        # --------- SOMENTE RSI ---------
        if not usar_rsi_ema:
            if rsi >= 70:
                return "🔴venda"
            elif rsi <= 30:
                return "🟢compra"

        # --------- RSI + EMA (melhor) ---------
        else:
            # VENDA: RSI sobrecomprado e EMA acima do preço
            if rsi >= 65 and close_atual < ema:
         
                return "🔴venda"

            # COMPRA: RSI sobrevendido e close acima da EMA
            if rsi <= 35 and close_atual > ema:
               
                return "🟢compra"
        
    # sem sinal
    return None
