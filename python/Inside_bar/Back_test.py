import os
import time
import pandas as pd
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
# === Funçoes ===
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

#--- Inside Bar
def ISDB_add_valor (ISDB_arquivo_tickers):
    global ISDB_mensagem 

    ISDB_df = pd.read_csv(ISDB_arquivo_tickers)
    ISDB_valor_add = str(input("Adicione um Ticker ---> "))
    if ISDB_valor_add not in ISDB_df['Ticker'].values:
        nova_linha = pd.DataFrame({'Ticker': [ISDB_valor_add]})
        ISDB_df = pd.concat([ISDB_df, nova_linha], ignore_index=True)
        ISDB_df.to_csv(ISDB_arquivo_tickers, index=False)
        ISDB_mensagem =f"✅ Nome '{ISDB_valor_add}' adicionado ao arquivo {ISDB_arquivo_tickers}."
        return ISDB_mensagem
    else:
        ISDB_mensagem = f"⚠️ Ticker '{ISDB_valor_add}' já existe, não foi adicionado."
        return ISDB_mensagem

   


while True: 
    clear_terminal()
    lobby ='''
===== BACK TEST ====
[1] Inside-Bar
[0] Sair

--> '''
    perg_lobby = int(input(lobby))

    # 1 === Inside Bar ===
    if perg_lobby == 1:
        ISDB_mensagem = ''
        clear_terminal()
        while True:
            
            #--- Variaveis
            lobby = '''
    ===== Inside Bar ====

    [1] Fazer o Back Test do ISDB
    [2] Remover dados do Back Test
    [3] Add um item a lista e fazer o back test ( so do item adicionado )
    [4] Remover Tickers
    [0] Sair

    --> '''
            ISDB_arquivo_dados = r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\Inside_bar_dados.csv"
            ISDB_arquivo_tickers = r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\Inside_bar_tikers.csv"


            #--- Criar arquivo caso não exista
            if not os.path.exists(ISDB_arquivo_dados):
                ISDB_df = pd.DataFrame(columns=[
            'Ticker', 'Capital', 'Porcentagens', 'Contagem_total',
            'Contagem_acerto', 'Contagem_erro', 'Intervalo',
            'Tamanho_take', 'Hora'
        ])
                ISDB_df.to_csv(ISDB_arquivo_dados, index=False)
            if not os.path.exists(ISDB_arquivo_tickers):
                ISDB_df = pd.DataFrame(columns=['Ticker'])
                ISDB_df.to_csv(ISDB_arquivo_tickers, index=False)

         
            print(len(pd.read_csv(ISDB_arquivo_tickers)))
            #--- Adicionar o primeiro Tiker
            if len(pd.read_csv(ISDB_arquivo_tickers)) <= 0:
                print("--- Você esta sem Ticker, adiocione ao menos 1 para começar... ---")
                ISDB_add_valor(ISDB_arquivo_tickers)

            clear_terminal()
            print(ISDB_mensagem)
            perg_lobby = int(input(lobby))

            #1-1 --- Fazer o Back Test do ISDB ---
            if perg_lobby == 1:
                
                print()

            #1-2 --- Remover dados do Back Test ---
            elif perg_lobby == 2:
                
                print()
                
            #1-3 --- Add um item a lista e fazer o back test ( so do item adicionado ) ---
            elif perg_lobby == 3:
                ISDB_add_valor(ISDB_arquivo_tickers)
            
             #1-4 --- Add um item a lista e fazer o back test ( so do item adicionado ) ---
            elif perg_lobby == 4:
                ISDB_add_valor(ISDB_arquivo_tickers)
            
            #1-0 --- ADD Todos a lista ---
            elif perg_lobby == 0:
                break
            

    # 0 === Sair ===
    elif perg_lobby == 0:
        clear_terminal()
        print("Encerrando Programa...")
        time.sleep(1)
        break
