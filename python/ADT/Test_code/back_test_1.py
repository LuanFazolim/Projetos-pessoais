import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
import csv
import os

lobby = """
===== BACK TEST ====

[1] Add todos da lista
[2] Remover todos da lista
[3] Refazer todos da lista
[4] Add um item a lista e fazer o back test
[0] Sair"""

# =========================
# CONFIGURAÇÕES
# =========================
ticker = ['BTC-USD','A1MD34.SA', 'AAPL34.SA', 'ABCB4.SA', 'ABEV3.SA', 'AERI3.SA', 'AGFS.SA', 'AGRI.SA', 'AGRO3.SA', 'ALOS3.SA', 'ALPA4.SA', 'ALUP11.SA', 'AMAR3.SA', 'AMBP3.SA'
,'AMER3.SA', 'AMZO34.SA', 'ANIM3.SA', 'ARML3.SA', 'ASAI3.SA', 'AURA33.SA', 'AURE.SA', 'AURE3.SA', 'AZUL4.SA', 'AZZA3.SA', 'B3SA3.SA', 'BABA34.SA', 'BBAS3.SA', 'BBDC3.SA', 'BBDC4.SA', 
'BBOV.SA', 'BBSD.SA', 'BBSE3.SA', 'BDEF.SA', 'BDRX.SA', 'BEEF3.SA', 'BERK34.SA', 'BEST.SA', 'BHIA3.SA', 'BLAU3.SA', 'BMGB4.SA', 'BMMT.SA', 'BMOB3.SA', 'BOVA11.SA', 'BOVB11.SA', 'BOVV.SA', 
'BOVV11.SA', 'BPAC11.SA', 'BPAN4.SA', 'BRAP4.SA', 'BRAV3.SA', 'BRAX11.SA', 'BREW.SA', 'BRFS3.SA', 'BRKM5.SA', 'BRSR6.SA', 'BRXC.SA', 'BXPO.SA', 'CAML3.SA', 'CASH3.SA', 'CBAV3.SA', 'CEAB3.SA', 
'CHVX34.SA', 'CMDB.SA', 'CMIG4.SA', 'CMIG3.SA', 'CMIN3.SA', 'COCA34.SA', 'COGN3.SA', 'CPFE3.SA', 'CPLE6.SA', 'CPLE3.SA', 'CSAN3.SA', 'CSMG3.SA', 'CSNA3.SA', 'CURY3.SA', 'CVCB3.SA', 'CXSE3.SA', 
'CYRE3.SA', 'DASA3.SA', 'DIRR3.SA', 'DIVO.SA', 'DVER.SA', 'DXCO3.SA', 'E1MR34.SA', 'ECOO.SA', 'ECOR3.SA', 'EGIE3.SA', 'ELET6.SA', 'ELET3.SA', 'EMBR3.SA', 'ENEV3.SA', 'ENGI11.SA', 'ENJU3.SA', 
'EQTL3.SA', 'ESGB.SA', 'ESPA3.SA', 'EVEN3.SA', 'EWBZ.SA', 'EXXO34.SA', 'EZTC3.SA', 'FESA4.SA', 'FLRY3.SA', 'GENB.SA', 'GFSA3.SA', 'GGBR4.SA', 'GGPS3.SA', 'GMAT3.SA', 'GMCO34.SA', 'GOAU4.SA', 
'GOGL34.SA', 'GOLD11.SA', 'GOLL54.SA', 'GRND3.SA', 'GSGI34.SA', 'GUAR3.SA', 'HAPV3.SA', 'HBOR3.SA', 'HBSA3.SA', 'HERT.SA', 'HIGH.SA', 'HYPE3.SA', 'IBBE.SA', 'IBEE.SA', 'IBEP.SA', 'IBEW.SA', 
'IBHB.SA', 'IBLV.SA', 'IBOB.SA', 'IBSD.SA', 'ICON.SA', 'IFCM3.SA', 'IGCT.SA', 'IGTI11.SA', 'IMAT.SA', 'IMOB.SA', 'INBR32.SA', 'INTB3.SA', 'IRBR3.SA', 'ISAE4.SA', 'ISEE.SA', 'ITAG.SA', 
'ITLC34.SA', 'ITSA4.SA', 'ITUB4.SA', 'ITUB3.SA', 'IVVB11.SA', 'JALL3.SA', 'JBSS32.SA', 'JHSF3.SA', 'JNJB34.SA', 'JPMC34.SA', 'KEPL3.SA', 'KLBN11.SA', 'LAVV3.SA', 'LEVE3.SA', 'LILY34.SA', 
'LJQQ3.SA', 'LOGG3.SA', 'LOGN3.SA', 'LREN3.SA', 'LVOL.SA', 'LWSA3.SA', 'M1TA34.SA', 'MATD3.SA', 'MBRF3.SA', 'MCDC34.SA', 'MDIA3.SA', 'MDNE3.SA', 'MEAL3.SA', 'MELI34.SA', 'MGLU3.SA', 
'MILS3.SA', 'MLAS3.SA', 'MLCX.SA', 'MOTV3.SA', 'MOVI3.SA', 'MRVE3.SA', 'MSFT34.SA', 'MTRE3.SA', 'MULT3.SA', 'MYPK3.SA', 'N1VO34.SA', 'NASD11.SA', 'NATU3.SA', 'NDIV.SA', 'NEOE3.SA', 
'NFLX34.SA', 'NSDV.SA', 'NVDC34.SA', 'ODPV3.SA', 'ONCO3.SA', 'ORVR3.SA', 'OXYP34.SA', 'P1GR34.SA', 'PAGS34.SA', 'PCAR3.SA', 'PETR4.SA', 'PETR3.SA', 'PETZ3.SA', 'PIBB.SA', 'PIBB11.SA',
 'PLPL3.SA', 'PNVL3.SA', 'POMO4.SA', 'POSI3.SA', 'PRIO3.SA', 'PSSA3.SA', 'PTBL3.SA', 'PYPL34.SA', 'QUAL3.SA', 'RADL3.SA', 'RAIL3.SA', 'RAIZ4.SA', 'RANI3.SA', 'RAPT4.SA', 'RDOR3.SA', 
 'RECV3.SA', 'RENT3.SA', 'RIOT34.SA', 'ROMI3.SA', 'ROXO34.SA', 'SANB11.SA', 'SAPR11.SA', 'SBFG3.SA', 'SBSP3.SA', 'SEER3.SA', 'SEQL3.SA', 'SIMH3.SA', 'SIMN34.SA', 'SLCE3.SA', 'SMAB.SA', 
 'SMAC.SA', 'SMAL.SA', 'SMAL11.SA', 'SMFT3.SA', 'SMTO3.SA', 'SOJA3.SA', 'SPUB.SA', 'SPXI11.SA', 'SRNA3.SA', 'STBP3.SA', 'SUZB3.SA', 'TAEE11.SA', 'TASA4.SA', 'TCSA3.SA', 'TEND3.SA', 'TIMS3.SA', 
 'TMOS34.SA', 'TOKY3.SA', 'TOTS3.SA', 'TRAD3.SA', 'TRIS3.SA', 'TSLA34.SA', 'TSMC34.SA', 'TTEN3.SA', 'TUPY3.SA', 'UGPA3.SA', 'UNIP6.SA', 'USIM5.SA', 'UTIL.SA', 'UTLL.SA', 'VALE3.SA', 'VAMO.SA', 
 'VAMO3.SA', 'VBBR3.SA', 'VERZ34.SA', 'VISA34.SA', 'VIVA3.SA', 'VIVT3.SA', 'VLID3.SA', 'VULC3.SA', 'VVEO3.SA', 'WALM34.SA', 'WEGE3.SA', 'WIZC3.SA', 'XBOV.SA', 'XBOV11.SA', 'XFIX.SA', 
 'XPBR31.SA', 'YDUQ3.SA', 'ZAMP3.SA']
#ticker = ["BTC-USD"]

intervalo = ['15m','1h','1d']
inicio = 0
fim =100000000000   
tempo = "1y"
tamanho_take = [2,2.5,3,4]
capital = 1000
capital_inicial = capital
capital_list = []
verify_melhor = []
total_verify = 0

arquivo = r"D:\Progamacao\Python\ADT\CSV\Dados\ADT_ISDB_Dados.csv"
cabecalhos = ['Ticker', 'Capital','Porcentagens', 'Contagem_total','Contagem_acerto','Contagem_erro', 'Intervalo', 'Tamanho_take','Hora']

with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(cabecalhos)  # Escreve o cabeçalho
        writer.writerows(capital_list)      # Escreve todas as linhas da lista
ultimo_tempo = None
media_tempo = 0
segundo_totais = 0

total = 0
simulando = False  # indica se estamos em uma simulação de trade
trade_info = {}    # armazena info da operação atual
contagem_acerto = 0
contagem_erro = 0
contagem_total = 0
terceira_candle = 0

# =========================
# PEGAR DADOS
# =========================

# =========================
# FUNÇÕES
# =========================
def simular_trade(open_, high_, low_, close_):

    global contagem_erro, contagem_acerto, contagem_total,terceira_candle, capital
    """
    Simula uma operação de trade (compra ou venda) baseada no rompimento do inside bar
    """
    global total, simulando, trade_info
    valor = abs(capital*0.03)
    #print(f"Valor aplicado: {valor:.2f} R$")
    stop_loss = trade_info['stop']
    take_profit = trade_info['take']
    direction = trade_info['direction']  # 'compra' ou 'venda'
    
    if direction == 'compra':
        if high_ >= take_profit or close_ >= take_profit :
            total += ((take_profit - trade_info['entry'])/trade_info["entry"]) * valor
            capital += ((take_profit - trade_info['entry'])/trade_info["entry"]) * valor
            
            #print(f"✅ Compra concluída | Lucro: {(take_profit - trade_info['entry'])*valor:.2f} R$")
            contagem_acerto+=1
            contagem_total+=1

            simulando = False
            terceira_candle = 0
        elif low_ <= stop_loss or close_ <= stop_loss:
            total += ((stop_loss - trade_info['entry']) /trade_info["entry"])* valor
            capital += ((stop_loss - trade_info['entry'])/trade_info["entry"]) * valor

            #print(f"❌ Stop hit (Compra) | Prejuízo: {(stop_loss - trade_info['entry'])*valor:.2f} R$")
            contagem_erro+=1
            contagem_total+=1

            simulando = False
            terceira_candle = 0

    elif direction == 'venda':
        if low_ <= take_profit or close_ <= take_profit:
            total += ((trade_info['entry'] - take_profit)/trade_info["entry"]) * valor
            capital += ((trade_info['entry'] - take_profit)/trade_info["entry"]) * valor

            #print(f"✅ Venda concluída | Lucro: {(trade_info['entry'] - take_profit)*valor:.2f} R$")
            contagem_acerto+=1
            contagem_total+=1

            simulando = False
            terceira_candle = 0
        elif high_ >= stop_loss or close_ >= stop_loss:
            total += ((trade_info['entry'] - stop_loss)/trade_info["entry"]) * valor
            capital += ((trade_info['entry'] - stop_loss)/trade_info["entry"]) * valor

            #print(f"❌ Stop hit (Venda) | Prejuízo: {(trade_info['entry'] - stop_loss)*valor:.2f} R$")
            contagem_erro+=1
            contagem_total+=1

            simulando = False
            terceira_candle = 0

def avaliar_ISB(tamanho_take):
    global total, simulando, trade_info, terceira_candle, capital
    
    corda_mae = [0, 0, 0]  # high e low da vela mãe

    selecionados = dados.iloc[inicio:fim+1]

    for tempo, linha in selecionados.iterrows():
        if capital <= 0:
            print(f"Banca quebrou com {capital} R$")
            break
        hora = tempo.hour
        #if 13<=hora > 9:
           # continue
        open_  = float(linha["Open"].iloc[0])
        high   = float(linha["High"].iloc[0])
        low    = float(linha["Low"].iloc[0])
        close  = float(linha["Close"].iloc[0])
        volume = int(linha["Volume"].iloc[0])

        vela_verde = close > open_

        #print(f"{tempo} | O:{open_:.2f} H:{high:.2f} L:{low:.2f} C:{close:.2f} V:{volume} TOTAL: {total:.2f} R$")

        tamanho_vela = (corda_mae[0] - corda_mae[1])*2.5

        # Se estiver simulando, executa trade
        if simulando:
            simular_trade(open_, high, low, close)
            continue

          
        # Detectar Inside Bar
        if corda_mae[0] != 0 and corda_mae[1] != 0 and close != open_:
            if high < corda_mae[0] and low > corda_mae[1] and terceira_candle == 0:
                #print(f"📌 INSIDE BAR detectada em {tempo}")
                # Define linha para compra/venda
                linha_superior = close if vela_verde else open_
                linha_inferior = open_ if vela_verde else close

                # Configura a trade_info para simulação
                # Compra
                trade_info_compra = {
                    'direction': 'compra',
                    'entry': linha_superior,
                    'stop': high - low,
                    'take': tamanho_take*abs(high - low)
                }
                
                # Venda
                trade_info_venda = {
                    'direction': 'venda',
                    'entry': linha_inferior,
                    'stop': high - low,
                    'take': tamanho_take*abs(high - low)
                }
                terceira_candle = 1
            
            elif terceira_candle == 1:
                    # Decisão inicial baseada no rompimento do próximo candle
                    # Aqui só armazenamos e aguardamos o próximo candle
                if close > linha_superior:
                    trade_info = trade_info_compra
                    trade_info['stop'] = close - trade_info["stop"]
                    trade_info['take'] = close + trade_info["take"]
                    trade_info['entry'] = close
                   
                    #print(f"Take proft: {trade_info['take']}\n Stop Loss: {trade_info['stop']}")
                    simulando = True

                elif close < linha_inferior:
                    trade_info = trade_info_venda
                    trade_info['stop'] = close + trade_info["stop"]
                    trade_info['take'] = close - trade_info["take"]
                    trade_info['entry'] = close

                    #print(f"Take proft: {trade_info['take']}\n Stop Loss: {trade_info['stop']}")
                    simulando = True
               
                
                
                
                
                


        
        # Atualiza vela mãe
        corda_mae[0] = high
        corda_mae[1] = low
        corda_mae[2] = abs(close - open_)

def porcentagem_hud(total_verify):
    global ultimo_tempo, media_tempo, segundo_totais
    
    total_acoes_verify = len(ticker) * len(intervalo) * len(tamanho_take)
    porcentagem = total_verify / total_acoes_verify * 100
    agora = time.time()
    
    if ultimo_tempo is not None:
        difer = agora - ultimo_tempo
        segundo_totais += difer
        media_tempo += difer
        tempo_medio = media_tempo / total_verify
        tempo_restante = tempo_medio * (total_acoes_verify - total_verify)
        tempo_falta = timedelta(seconds=int(tempo_restante))
        print(f"\nDifer {difer:.2f}: \nSegundos_totais {segundo_totais:.2f}: \ntempo_medio {tempo_medio:.2f}: \ntempo_restante {tempo_restante:.2f}: \n")
    else:
        tempo_falta = "--"
    
    ultimo_tempo = agora
    
    print(f"--- {total_verify}/{total_acoes_verify} --- Progresso geral: {porcentagem:.1f}% --- Tempo estimado --> {tempo_falta}\n", end="")



with open(arquivo, "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=';')
    for linha in leitor:
        print(linha["Ticker"], linha["hora"])

# =========================
# EXECUTAR
# =========================

capital_list = []
verify_melhor = []

print("\033[2J")
print("\033[H")
print("--- 0/0 --- Progresso geral: 0.0% ---\n")
for ticker_ in ticker:
    

    for intervalo_ in intervalo:
        

        tempo = '1mo' if intervalo_ == '15m' else '1y'
        
        dados = yf.download(ticker_, period=tempo, interval=intervalo_, progress=False,auto_adjust=True)
        if dados.index.tzinfo is None:
            dados.index = dados.index.tz_localize('UTC')

        dados.index = dados.index.tz_convert('America/Sao_Paulo')
        for tamanho_take_ in tamanho_take:
            if not dados.empty:
                
                print(f"==== {ticker_} ==== {intervalo_}  {tamanho_take_}x\n\n")
        
                avaliar_ISB(tamanho_take_)

                print(f"\nEm {tempo}, com um intervalo de {intervalo_} tivemos:")
                porcentagem = (contagem_acerto/contagem_total) *100 if contagem_acerto != 0 and contagem_total !=0 else 0
                print(f"\n\nAplicaçoes Totais: {contagem_total}\nAcertos: {contagem_acerto}\nErros: {contagem_erro}\n\nCerca de {porcentagem:.1f}% de acertos")
                print(f"\nLucro total: {total:.2f} R$\nCapital final: {capital:.2f} R$")
                capital_list.append([ticker_,round(capital,2),round(porcentagem,2),contagem_total,contagem_acerto,contagem_erro, intervalo_, tamanho_take_, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            
                terceira_candle = 0
                total = 0
                contagem_erro = 0
                contagem_acerto = 0
                contagem_total = 0
                capital = 1000
                print('\n',50*"-=",'\n')
                total_verify +=1
                
                print("\033[2J\033[H", end="")
                porcentagem_hud(total_verify)
                
                
            
            else:
                print("❌ Nenhum dado retornado. Verifique o ticker ou o intervalo.")
                total_verify +=1

# Criação do arquivo CSV
if not os.path.exists(arquivo):
    with open(arquivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(cabecalhos)  # Escreve o cabeçalho
        writer.writerows(capital_list)      # Escreve todas as linhas da lista

print(f"Arquivo '{arquivo}' criado com sucesso!")

for num in capital_list:    
    
    if verify_melhor:
       
        if verify_melhor[0][1] > num[1] :
            continue
        else:
            if num[2] == 0:
                continue
            verify_melhor.clear()
            verify_melhor.append([num[0],num[1],num[2],num[3],num[4],num[5],num[6],num[7]])
    else:
        verify_melhor.append([num[0],num[1],num[2],num[3],num[4],num[5],num[6],num[7]])

print(f"\nMelhor para usar Inside Bar == {verify_melhor[0][0]} {verify_melhor[0][6]} == {verify_melhor[0][7]}x \n\nCom {verify_melhor[0][1]} R$ do capital ({verify_melhor[0][1] - capital_inicial:.2f} R$ de Lucro) \n\n{verify_melhor[0][2]} % de acerto \n{verify_melhor[0][3]} Aplicaçoes totais \n\n{verify_melhor[0][4]} Acertos\n{verify_melhor[0][5]} Erros")