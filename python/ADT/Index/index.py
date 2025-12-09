import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from binance.client import Client
import yfinance as yf


import os
import csv
import time
import pandas as pd
import importlib
import threading
import numpy as np
from deep_translator import GoogleTranslator

Verificar_largura = False
largura_2 = 0
verificar_def_estrategia = False
#Lobby_
ISDB_arquivo_dados = r"D:\Progamacao\Python\ADT\CSV\Dados\ADT_ISDB_Dados.csv"
Tickers_arquivo = r"D:\Progamacao\Python\ADT\CSV\Tickers\ADT_Tickers.csv"
Tickers_pack_arquivo =r'D:\Progamacao\Python\ADT\CSV\Tickers\ADT_Pack_TIckers.csv'

BACKT_arquivo_filtro_in = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_filtro_back_test_in.csv"
BACKT_arquivo_filtro_pe = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_filtro_back_test_pe.csv"
Estrategias_pasta = r"D:\Progamacao\Python\ADT\Index\Estrategias"

Estrategias_arquivo_variaveis = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_estrategias_variaveis.csv"
Aplicacoes_andamento = r"D:\Progamacao\Python\ADT\CSV\Dados\ADT_Aplicacoes_andamento.csv"

Arquivo_info_money = r"D:\Progamacao\Python\ADT\CSV\variaveis\ATD_money_info.csv"
capital_set = 60
aplicar_set = 10
aplicar_porc_set = 3
aplicar_01 = False
TPx = 1
SLx = 1


if not os.path.exists(ISDB_arquivo_dados):
    ISDB_df = pd.DataFrame(columns=[
'Ticker', 'Capital', 'Porcentagens', 'Contagem_total',
'Contagem_acerto', 'Contagem_erro', 'Intervalo',
'Tamanho_take', 'Hora'
])
    ISDB_df.to_csv(ISDB_arquivo_dados, index=False)
if not os.path.exists(Tickers_arquivo):
    ISDB_df = pd.DataFrame(columns=['Ticker'])
    ISDB_df.to_csv(Tickers_arquivo, index=False)

opcoes_intervalo = ["5min", "15min", "1hr", "1D", "1sem", "1mes"]
opcoes_periodo = ["1Dia", "1Semana", "1Mes","1y", "2y", "5y"]
if not os.path.exists(BACKT_arquivo_filtro_in):
    with open(BACKT_arquivo_filtro_in, "w", newline="", encoding="utf-8") as f: 
        escritor = csv.writer(f)
        escritor.writerow(["intervalo", "intervalo_01","code"])
        for v,i in zip(opcoes_intervalo,["5m","15m","1h","1d","1wk","1mo"]):
            escritor.writerow([v, 0, i]) # cabeçalho
if not os.path.exists(BACKT_arquivo_filtro_pe):
    with open(BACKT_arquivo_filtro_pe, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["periodo", "periodo_01","code"])  # cabeçalho
        for v,i in zip(opcoes_periodo,["1d","7d","1mo","1y","2y","5y"]):
            escritor.writerow([v, 0, i]) # cabeçalho


 # Lista de estratégias

Estrategia_Price_action = ["Inside Bar"]
Estrategia_Indicadores = ["Rsi + EMA","Rsi"]
Estrategia_Estruturais = ["Pivot Points"]
Estrategias = []

for item in Estrategia_Price_action:
    Estrategias.append([item, "Price_a"])

for item in Estrategia_Indicadores:
    Estrategias.append([item, "Ind"])

for item in Estrategia_Estruturais:
    Estrategias.append([item, "Estr"])


print(Estrategias)
if not os.path.exists(Estrategias_arquivo_variaveis):
    with open(Estrategias_arquivo_variaveis, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["estrategia", "estrategia_01","peso","class"])  # cabeçalho
        for v in Estrategias:
            escritor.writerow([v[0], 0, 1, v[1]]) # cabeçalho

if not os.path.exists(Aplicacoes_andamento):
    with open(Aplicacoes_andamento, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["tempo","close","periodo","intervalo","tp","sl","tp_porc","sl_porc","direcao"])  # cabeçalho
       
if not os.path.exists(Arquivo_info_money):
    with open(Arquivo_info_money, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["capital", "aplicado","aplicado_porc","aplicar_01","TPx","SLx"])  # cabeçalho
        escritor.writerow([capital_set,aplicar_set,aplicar_porc_set,aplicar_01,TPx,SLx])




EDTE_arquivo_config = r"D:\Progamacao\Python\ADT\CSV\variaveis\ATD_config_info.csv"
forca_min = 3
mult_price_a = 1.2
tolerancia = 1

pes_estr = 1.0    
pes_price_a = 1.2
pes_ind = 0.7


if not os.path.exists(EDTE_arquivo_config):
    with open(EDTE_arquivo_config, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["forca_min","mult_price_a","tolerancia","pes_estr","pes_price_a","pes_ind"])  # cabeçalho
        escritor.writerow([forca_min,mult_price_a,tolerancia,pes_estr,pes_price_a,pes_ind])


lista_vela = []
peso_max = 5
list_estrategias_ativas = []
lista_verify_estrategia = []

MDD_list_capital = []
Winrate_positivos = []
Winrate_negativos = []

Winrate_totais = 0

# ======= CLASSE DADO =======
class Dado:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return f"{self.nome}"
# ======= DESCRIÇAO =========
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.label = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.label:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 40
        self.label = ctk.CTkLabel(self.widget.master, text=self.text, fg_color="yellow", text_color="black")
        self.label.place(x=x - self.widget.master.winfo_rootx(), y=y - self.widget.master.winfo_rooty())


    def hide(self, event=None):
        if self.label:
            self.label.destroy()
            self.label = None


# ======= APLICAÇÃO PRINCIPAL =======
class LobbyApp(ctk.CTk):
  
    

    def __init__(self):
        
        super().__init__()
        
        
        # ======= Configurações da janela =======
        self.title("Automatic dry Trading (ADT)")
        self.geometry("420x760") # Tela cheia
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))  # Pressione ESC para sair da tela cheia
        self.resizable(True, True)
        #ctk.set_appearance_mode("dark")
        #ctk.set_default_color_theme("blue")
        ctk.set_default_color_theme(r"D:\Progamacao\Python\ADT\Index\tema.json")
        self.resultados = []

        self.bind("<Configure>", self.acompanhar_largura)

        self.lista_dados = []
        self.criar_lobby()

    def acompanhar_largura(self, event):
        global Verificar_largura, largura_2, verificar_def_estrategia
        largura = self.winfo_width()
        
        largura_max = 1000

        if largura >= largura_max:
            
            Verificar_largura = True
        else:
            Verificar_largura = False
            
        if verificar_def_estrategia == True:
            if (largura_2 >= largura_max and largura < largura_max) or (largura_2 < largura_max and largura >= largura_max):
                self.Editar_estrategias()
    
        largura_2 = largura
    # ======= LIMPAR TELA =======
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ======= LOBBY PRINCIPAL =======
    def criar_lobby(self):
        global verificar_def_estrategia
        verificar_def_estrategia = False
        self.limpar_tela()

        #--- Titulo
        titulo = ctk.CTkLabel(self, text=" 💲 ADT 💲 ", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=60)

        #--- Botao - Começar -
        btn_start = ctk.CTkButton(self, text="Começar", width=220, height=40, command=self.Start_simulation)
        btn_start.pack(pady=(0,60))
        Tooltip(btn_start, " Inicia a simulação do sistema ADT ")
        #--- Botao - Editar -
        btn_edit = ctk.CTkButton(self, text="Editar Estrategias 🖊", width=180, height=40, command=self.Editar_estrategias)
        btn_edit.pack(pady=10)
        Tooltip(btn_edit, " Abre o menu para editar as estrategias ")
        #--- Botao - Tickers -
        btn_edit = ctk.CTkButton(self, text="Tickers 📚", width=180, height=40, command=self.TKRS_Menu)
        btn_edit.pack(pady=10)
        Tooltip(btn_edit, " Add ou excluir os Tickers ")
         #--- Botao - Sair -
        btn_sair = ctk.CTkButton(self, text="❌ Sair", width=220, height=40, fg_color="red", hover_color="#b30000", command=self.destroy)
        btn_sair.pack(side="bottom",pady=30)
        Tooltip(btn_sair, " Encerra o aplicativo ")




    # ======= MENU TESTE DADOS =======
    # -- Verificar_melhores_tickers -- 

    def Retorno_anualizado(self,capital_ini,capital_fim,dias):
        R = (capital_fim - capital_ini) / capital_ini
        RA_ = (1 + R) ** (365/dias) - 1
        RA = round(RA_, 2)
        return RA

    def MDD(self):
        if len(MDD_list_capital) ==0:
            return 0
    
            
        pico = MDD_list_capital[0]
        mdd = 0  # sempre negativo ou zero

        for v in MDD_list_capital:
            pico = max(pico, v)                # maior valor até agora
            dd = (pico - v) / pico             # drawdown atual
            mdd = round (max(mdd, dd),3)             # maior drawdown (positivo)

        
        return mdd

    def DD(self):
        if len(MDD_list_capital) == 0:
            return 0

        pico = MDD_list_capital[0]   # maior valor até agora
        atual = MDD_list_capital[-1] # último valor da lista (capital atual)

        # Atualiza o pico percorrendo a lista
        for v in MDD_list_capital:
            pico = max(pico, v)

        # Drawdown atual (somente do momento)
        dd = (pico - atual) / pico
        dd = round(dd, 3)

        return dd    
    
    def Winrate(self):
        global Winrate_positivos, Winrate_totais
        
    
        Winrate = round(len(Winrate_positivos) / Winrate_totais,2) if Winrate_totais !=0 else 0
       
        return Winrate

    def R_R(self):
        global Winrate_positivos, Winrate_negativos, Winrate_totais
        ganho_total = sum(Winrate_positivos)
        perda_total = abs(sum(Winrate_negativos))
        
        if ganho_total == 0:
        
                return 0
        
        elif perda_total == 0:
            return round(ganho_total,2)
        R_R = round(ganho_total/perda_total,2)
        return R_R
    
    def Expectancy(self,Winrate):
        global Winrate_positivos, Winrate_negativos, Winrate_totais
       
        if Winrate_totais == 0:
            return 0
        Media_ganhos = sum(Winrate_positivos)/Winrate_totais
        
        Media_perdas = abs(sum(Winrate_negativos)/Winrate_totais)
        Excepectancy = round((Winrate * Media_ganhos) - ((1 - Winrate) * Media_perdas), 3)
        
        #print(f"Media_ganhos: {Media_ganhos} | Media_perdas: {Media_perdas} | Total: {Winrate_totais} |Winrate: {Winrate} | Expectancy: {Excepectancy}")
        return Excepectancy

        


    '''def Consistencia(self):
        global Winrate_positivos, Winrate_negativos, Winrate_totais
        ganho_total = sum(Winrate_positivos)
        perda_total = abs(sum(Winrate_negativos))
        if ganho_total > perda_total:
            Constancia = ganho_total'''
    
        
        

    
    # -- Verificar_aplicacoes -- 
    def Verify_estrategias(self,tempo):
    
            # Lê o CSV com as estratégias
            df = pd.read_csv(Estrategias_arquivo_variaveis)

            # Lista para armazenar estratégias ativas
            

            # Identifica as estratégias com valor 1 (ativas)
            for _, linha in df.iterrows():
                nome = linha["estrategia"]
                ativo = linha["estrategia_01"]

                if ativo == 1:
                    # Substitui espaços por underscore (compatível com nomes de arquivo)
                    nome_formatado = nome.replace(" ", "_")
                    list_estrategias_ativas.append(nome_formatado)

            #print("Estratégias ativas:", list_estrategias_ativas)

            # Importa e executa cada uma das estratégias ativas
           
            
            for estrategia in list_estrategias_ativas:
                nome_arquivo = f"ADT_estrategia_{estrategia}"
                if estrategia == "Rsi_+_EMA":
                    nome_arquivo = f"ADT_estrategia_Rsi"

                caminho_completo = os.path.join(Estrategias_pasta, f"{nome_arquivo}.py")
            
                if os.path.exists(caminho_completo):
                    try:
                        # Importa o módulo dinamicamente
                       
                        modulo = importlib.import_module(f"Estrategias.{nome_arquivo}")
                        
                        # Executa a função principal da estratégia (ex: test())
                        if hasattr(modulo, "BCKT_estrategia"):
                           

                            var_estra = modulo.BCKT_estrategia(self.resultados)
                            peso_nome = estrategia.replace("_", " ")
                            peso = int(df.loc[df["estrategia"] == peso_nome, "peso"].iloc[0])
                            classe = str(df.loc[df["estrategia"] == peso_nome, "class"].iloc[0])
                            if classe == "Price_a":      peso *= 1.0
                            elif classe == "Estr":   peso *= 0.7
                            elif classe == "Ind":    peso *= 0.5   # Fibo, Pivot, Gann
                            else:                   peso *= 1.0

                            if var_estra != None:
                                lista_verify_estrategia.append([estrategia,var_estra,peso,classe])
                           

                            #print(f"| {estrategia} --- {var_estra}")
                            

                        else:
                            print(f"⚠ {nome_arquivo} não tem função 'BCKT_estrategia()'")
                    except Exception as e:
                        resultado = GoogleTranslator(source='auto', target='pt').translate(str(e))
                        print(f"❌ Erro ao importar {nome_arquivo}: {resultado}")
               
                else:
                    print(f"⚠ Arquivo não encontrado: {caminho_completo}")
            
         

            #print(f"{tempo} -- {lista_verify_estrategia}")
            #===== Verificar se a Aplicacoes =====      
    def Verify_buy_sell(self,tempo,close,atr,periodo,intervalo,TPx,SLx):
        df_apl = pd.read_csv(Aplicacoes_andamento)
        peso_geral = 0
        Estr_True = False
        Price_a_True = False
        Ind_True = False

        peso_compra = sum(s[2] for s in lista_verify_estrategia if '🟢' in s[1])
        numero_compra = sum(1 for e in lista_verify_estrategia if '🟢' in e[1])
        peso_venda  = sum(s[2] for s in lista_verify_estrategia if '🔴' in s[1]) * -1
        numero_venda = sum(1 for e in lista_verify_estrategia if '🔴' in e[1])
    


        #print(lista_verify_estrategia)
        quantidade_estrategia = len(lista_verify_estrategia)
        if quantidade_estrategia != 0 and atr != 0:
            
            lista_ordem_classe = []

            
            for linha in lista_verify_estrategia:
                estrategia = linha[0]
                direcao = linha[1]

                peso_ = linha[2]
                classe = linha[3]
              
                

                if classe =="Estr":
                    Estr_True = True
                elif classe =="Ind":
                    Ind_True = True
                elif classe =="Price_a":
                    Price_a_True = True
                    

            # Checa se Price Action está ativo
            if not Price_a_True:
                peso_compra *= 1.2
                peso_venda  *= 1.2
                #return None  # sem PA → sem sinal

    
         
            peso_geral = peso_compra + peso_venda
            
            # --- Definir limiar de entrada (escala com número/força de estratégias) ---
            # limiar_base: o mínimo absoluto que você quer (mantive 3 por compatibilidade com seu sistema)
            limiar_base = 3.0
            # limiar proporcional: 40% do peso máximo possível (soma dos pesos absolutos ativos)
            peso_max_possivel = sum(abs(e[2]) for e in lista_verify_estrategia)
            limiar_proporcional = 0.40 * peso_max_possivel

            # escolha final do limiar: o maior entre o base e o proporcional
            limiar = max(limiar_base, limiar_proporcional)

            # --- regra rápida: se não há sinais suficientes (ex: menos de 1 sinal de qualquer lado) → não operar ---
            if numero_compra + numero_venda == 0:
                return None

            # --- SE EXISTIR CONFLITO (ex.: muitas compras e muitas vendas) o peso_geral reflectirá isso ---
            # agora checamos o limiar
            if abs(peso_geral) < limiar:
                return None

            # --- monta TP/SL e registra ---
            tp = sl = tp_porc = sl_porc = None
            direcao = None

            if peso_geral >= limiar:
                # COMPRA
                tp = close + (TPx * atr)
                sl = close - (SLx * atr)

                tp_porc = (tp - close) / tp if tp != 0 else 0
                sl_porc = (close - sl) / close if close != 0 else 0

                direcao = "🟢compra"

            elif peso_geral <= -limiar:
                # VENDA
                tp = close - (TPx * atr)
                sl = close + (SLx * atr)

                tp_porc = (close - tp) / close if close != 0 else 0
                sl_porc = (sl - close) / sl if sl != 0 else 0

                direcao = "🔴venda"

            # Se chegou aqui sem direção válida
            if direcao is None:
                return None

            # --- arredonda e salva a aplicação ---
            tp = round(tp, 2)
            sl = round(sl, 2)
            close_rounded = round(close, 2)

            df_apl.loc[len(df_apl)] = [tempo, close_rounded, periodo, intervalo, tp, sl, tp_porc, sl_porc, direcao]
            df_apl.to_csv(Aplicacoes_andamento, index=False)

            return direcao          
    def Verify_lucro(self,tempo_atual,close,aplicador,capital):
        global Winrate_positivos, Winrate_totais,Winrate_negativos
        df_apl = pd.read_csv(Aplicacoes_andamento)
        linhas_excluir = []
        if not df_apl.empty:
            
            for _, linha in df_apl.iterrows():
                tempo = linha["tempo"]
                close_ex = linha["close"]
                periodo = linha["periodo"]
                intervalo = linha["intervalo"]
                tp = linha["tp"]
                sl = linha["sl"]
                tp_porc = linha["tp_porc"]
                sl_porc = linha["sl_porc"]
                direcao = linha["direcao"]

                lucro_positivo = (tp_porc)*aplicador
                lucro_negativo = ((sl_porc)*aplicador)*-1
                aplicacao_01 = None
                
                if direcao == "🟢compra":

                    if close >= tp:
                        aplicacao_01 = True
                
                    elif close <= sl:
                        aplicacao_01 = False
                    

                if direcao == "🔴venda":
                    if close <= tp:
                        
                        aplicacao_01 = True
                    elif close >= sl:
                        aplicacao_01 = False

                if aplicacao_01 != None:
                    # -- Positivo --
                    if aplicacao_01:
                        capital+=lucro_positivo
                        linhas_excluir.append(_)
                        Winrate_positivos.append(lucro_positivo)

                        
                    # -- Negativo --
                    elif aplicacao_01 == False:
                        capital+=lucro_negativo
                        linhas_excluir.append(_)
                        Winrate_negativos.append(lucro_negativo)
                    Winrate_totais +=1
                    MDD_list_capital.append(float(capital))



           # print(f"--------- CAPITAL FINAL ----> {capital}")
            df_apl.drop(linhas_excluir, inplace=True) 
            df_apl.to_csv(Aplicacoes_andamento, index=False)

        list_estrategias_ativas.clear()
        lista_verify_estrategia.clear()
        return capital



    # ==== COMEÇAR ====
    def Start_simulation(self):
        self.limpar_tela()
        
        titulo = ctk.CTkLabel(self, text="🚀 Painel de Execução", font=ctk.CTkFont(size=24, weight="bold"))
        titulo.pack(pady=(30,10))

        subtitulo = ctk.CTkLabel(self, text="Escolha o modo de operação do ADT",font=ctk.CTkFont(size=14))
        subtitulo.pack(pady=(0,40))

        ctk.CTkButton(self, text="▶ Iniciar Análise ao Vivo", width=220, height=40).pack(pady=10)
        ctk.CTkButton(self, text="🧪 Back-Test Estratégias", width=220, height=40,command=self.Back_test).pack(pady=10)
        ctk.CTkButton(self, text="📊 Resultados Recentes", width=220, height=40).pack(pady=10)
        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby)
        botao_voltar.pack(side="bottom", pady=30)
    
    #=== Back-test ====
    def Back_test(self):

        janela = ctk.CTkToplevel(self)
        janela.title("Fazendo Back-Test 🧪")
        janela.geometry("900x506")
        janela.resizable(True, True)
        janela.grab_set()

        # =====================
        # BOTÃO DE FILTRO
        # =====================
        filtro_img = ctk.CTkImage(
            light_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_filtro.png"),
            dark_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_filtro.png"),
            size=(40, 40)
        )
       
        btn_filtro = ctk.CTkButton(
            janela, text="", image=filtro_img,
            corner_radius=20, width=40, height=40,
            command=self.BACKT_filtro
        )
        btn_filtro.place(x=10, y=10)
        
        money_img = ctk.CTkImage(
            light_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_money.png"),
            dark_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_money.png"),
            size=(30, 30)
        )

        btn_money = ctk.CTkButton(
            janela, text="", image=money_img,
            corner_radius=15, width=30, height=30,
            command=self.BACKT_money
        )
        btn_money.place(x=110, y=13.3)
        # =====================
        # CAIXA DE TEXTO
        # =====================
        caixa = ctk.CTkTextbox(janela, font=ctk.CTkFont(size=14))
        caixa.pack(padx=10, pady=(70, 10), expand=True, fill="both")
        caixa.configure(state="disabled")

        # =====================
        # FLAGS DE CONTROLE
        # =====================
        stop_bckt_flag = False
        start_bckt_flag = False

         


        
           



                
            
        
        # ---- Força velas -----
        def Forca_vela(close, high, low, open_, atr=None, media_range=None):
            """
            Classificação profissional da força da vela:
            Retornos: A+, A, B, C
            """

            tamanho_total = high - low
            if tamanho_total == 0:
                return "C"

            corpo = abs(close - open_)
            corpo_porc = corpo / tamanho_total
            pavio_sup = (high - max(open_, close)) / tamanho_total
            pavio_inf = (min(open_, close) - low) / tamanho_total
            close_pos = (close - low) / tamanho_total

            # --------------------------------------------
            # 1 — VELA INSTITUCIONAL (A+)
            # --------------------------------------------
            cond_corpo_institucional = corpo_porc >= 0.65
            cond_pavio_pequenos = pavio_sup <= 0.10 and pavio_inf <= 0.10
            cond_close_extremo = close_pos >= 0.90 or close_pos <= 0.10

            cond_range_explosivo = False
            if media_range is not None:
                cond_range_explosivo = tamanho_total > media_range * 1.4

            cond_atr_forte = tamanho_total>atr
            if atr is not None:
                cond_atr_forte = tamanho_total > atr

            if cond_corpo_institucional and cond_pavio_pequenos and cond_close_extremo:
                if cond_range_explosivo or cond_atr_forte:
                    return "A+"  # Explosiva (institucional)
                else:
                    return "A"   # Muito forte

            # --------------------------------------------
            # 2 — VELA FORTE (A)
            # --------------------------------------------
            cond_corpo_forte = 0.50 <= corpo_porc < 0.65
            cond_close_bom = (0.80 <= close_pos <= 0.90) or (0.10 <= close_pos <= 0.20)

            if cond_corpo_forte and cond_close_bom:
                return "A"

            # --------------------------------------------
            # 3 — MÉDIA (B)
            # --------------------------------------------
            cond_corpo_medio = 0.30 <= corpo_porc < 0.50
            if cond_corpo_medio:
                return "B"

            # --------------------------------------------
            # 4 — FRACA (C)
            # --------------------------------------------
            return "C"
        
        def calcular_atr(lista_vela, periodo=14):
            """
            ATR profissional usando True Range (TR):
            TR = max(
                high - low,
                abs(high - close anterior),
                abs(low - close anterior)
            )
            ATR = média(TR)
            """

            if len(lista_vela) < periodo + 1:
                return 0

            TR_list = []

            for i in range(-periodo, 0):
                atual = lista_vela[i]
                anterior = lista_vela[i - 1]

                high = atual["high"]
                low = atual["low"]
                close_prev = anterior["close"]

                tr = max(
                    high - low,
                    abs(high - close_prev),
                    abs(low - close_prev)
                )

                TR_list.append(tr)

            return np.mean(TR_list)

        def calcular_media_range(lista_vela):
            if len(lista_vela) < 20:
                return None

            return np.mean([(v["high"] - v["low"]) for v in lista_vela[-20:]])
        # -----------------------

        # =====================
        # FUNÇÃO START
        # =====================
        def Start_BCKT(caixa):
            global lista_vela, Winrate_totais
            
            nonlocal stop_bckt_flag, start_bckt_flag
            start_bckt_flag = True  
            stop_bckt_flag = False  # reseta o flag toda vez que começa
            
            
            janela.after(0, lambda: (
                btn_start.configure(state="disabled", fg_color="gray"),
                btn_stop.configure(state="normal", fg_color="red", command=Stop_BCKT),
                btn_clear.configure(state="disabled", fg_color="gray", command=None)
            ))
            

            df = pd.read_csv(Tickers_arquivo)
            df_in = pd.read_csv(BACKT_arquivo_filtro_in)
            df_pe = pd.read_csv(BACKT_arquivo_filtro_pe)
            df_money = pd.read_csv(Arquivo_info_money)
            capital_ini = df_money.loc[0,"capital"]
            aplicado = df_money.loc[0,"aplicado"]
            aplicado_porc = df_money.loc[0,"aplicado_porc"]
            aplicar_01 = df_money.loc[0,"aplicar_01"]
            TPx = df_money.loc[0,"TPx"]
            SLx = df_money.loc[0,"SLx"]
            #print(f"Capital Inicial: {capital_ini} | Aplicado: {aplicado} | Aplicado %: {aplicado_porc} | Aplicar 01: {aplicar_01}")


            # filtros válidos
            filtr_1d = [df_in.loc[0, "intervalo"], df_in.loc[1, "intervalo"], df_in.loc[2, "intervalo"]]
            filtr_7d = [df_in.loc[i, "intervalo"] for i in range(4)]
            filtr_1mes = [df_in.loc[i, "intervalo"] for i in range(5)]
            filtr_1y_2y = [df_in.loc[i, "intervalo"] for i in range(2, 6)]
            filtr_5y = [df_in.loc[i, "intervalo"] for i in range(3, 6)]

            soma_intevalo = df_in["intervalo_01"].sum()
            soma_periodo = df_pe["periodo_01"].sum()

            caixa.configure(state="normal")
            caixa.delete("1.0", "end")

            if soma_intevalo == 0:
                caixa.insert("end", "⚠️ Ao menos 1 intervalo deve ser selecionado!\n")
            if soma_periodo == 0:
                caixa.insert("end", "⚠️ Ao menos 1 período deve ser selecionado!\n")

            in_filtro = df_in[df_in['intervalo_01'] == 1]
            pe_filtro = df_pe[df_pe['periodo_01'] == 1]

            lista_melhores_tickers = []
            Winrate_positivos.clear()
            Winrate_negativos.clear()
            Winrate_totais = 0
            MDD_list_capital.clear()

            if soma_periodo > 0 and soma_intevalo > 0:
                if "Ticker" in df.columns:
                    lista_tickers = df["Ticker"].tolist()
                    if len(lista_tickers) > 0:
                        for ticker in lista_tickers:
                            
                            if stop_bckt_flag:
                                caixa.insert("end", "\n🟥 Back-test interrompido pelo usuário.\n")
                                caixa.configure(state="disabled")
                                return
                            janela.update()  # permite resposta ao stop

                            for periodo, code_pe in zip(pe_filtro["periodo"], pe_filtro["code"]):
                                dias = 0
                                if periodo == "1Dia": dias = 1
                                elif periodo == "1Semana": dias = 7
                                elif periodo == "1Mes": dias = 30
                                elif periodo == "1y": dias = 365
                                elif periodo == "2y": dias = 365*2
                                elif periodo == "5y": dias = 365*5
                                
                                if stop_bckt_flag:
                                    caixa.insert("end", "\n🟥 Back-test interrompido pelo usuário.\n")
                                    caixa.configure(state="disabled")
                                    break
                               
                                for intervalo, code_in in zip(in_filtro["intervalo"], in_filtro["code"]):
                                    df = pd.DataFrame(columns=["tempo","close","periodo","intervalo","tp","sl","tp_porc","sl_porc","direcao"])
                                    df.to_csv(Aplicacoes_andamento, index=False)
                                    if stop_bckt_flag:
                                        caixa.insert("end", "\n🟥 Back-test interrompido pelo usuário.\n")
                                        caixa.configure(state="disabled")
                                        break
                                    
                                    tempo_ini = 0
                                    
                                    
                            
                                    aplicador = 0
                                    if aplicar_01 == True:
                                        aplicador = aplicado
                                   

                                    
                                    # verifica se a combinação existe
                                    if (
                                        (periodo == "1Dia" and intervalo not in filtr_1d) or
                                        (periodo == "1semana" and intervalo not in filtr_7d) or
                                        (periodo == "1mes" and intervalo not in filtr_1mes) or
                                        (periodo in ["1y", "2y"] and intervalo not in filtr_1y_2y) or
                                        (periodo == "5y" and intervalo not in filtr_5y)
                                    ):
                                        caixa.insert("1.0", f"\n {periodo} --- {intervalo} ---- Não possui dados ❌\n")
                                        continue

                                    # baixa dados
                                    dados = yf.download(ticker, period=code_pe, interval=code_in, progress=False, auto_adjust=True)
                                
                                    if dados.index.tzinfo is None:
                                        dados.index = dados.index.tz_localize('UTC')
                                    dados.index = dados.index.tz_convert('America/Sao_Paulo')
                                    all_dados = dados.iloc[0:1000000000000]
                          
                                    if not dados.empty:
                                        #--- BACK TEST Terminal ---- 
                                        try:
                                            
                                            capital = capital_ini
                                            
                                          
                                            for tempo, linha in all_dados.iterrows():
                                                
                                                if tempo_ini == 0:
                                                    tempo_ini = tempo

                                                if stop_bckt_flag:
                                                    caixa.insert("end", "\n🟥 Back-test interrompido pelo usuário.\n")
                                                    caixa.configure(state="disabled")
                                                    break
                                               
                                                if aplicar_01 == False:
                                                    aplicador = (aplicado_porc/100)*capital
                                               

                                                #print(f"Aplicador: ({aplicado_porc} / 100) x {capital} = {aplicador}  |  Capital: {capital}  |  Lucro {BACKT_lucro}")
                                                close  = pd.Series(linha["Close"]).item()
                                                high   = pd.Series(linha["High"]).item()
                                                low    = pd.Series(linha["Low"]).item()
                                                open_  = pd.Series(linha["Open"]).item()
                                                volume = pd.Series(linha["Volume"]).item()

                                                vela_cor = "green" if close > open_ else "red"
                                        
                                                lista_vela.append({
                                                    "close": close,
                                                    "high": high,
                                                    "low": low,
                                                    "open": open_})
                                                atr = calcular_atr(lista_vela)
                                                media_range = calcular_media_range(lista_vela)


                                                forca_vela = Forca_vela(close,high,low,open_,atr, media_range)
                                              
                                                #print(f"{tempo} --- {forca_vela}  | close : {close:.2f} | open: {open_:.2f} | max: {high:.2f} | min: {low:.2f} | volume: {volume} ")

                                                self.resultados = [] 
                                    
                                                
                                                # ... dentro do loop, quando obtiver os valores de close/open/low/high:
                                                resultado_item = {
                                                    "ticker": ticker,
                                                    "periodo": periodo,
                                                    "intervalo": intervalo,
                                                    "close": close,
                                                    "high": high,
                                                    "low": low,
                                                    "open": open_,
                                                    "vela_cor":vela_cor,
                                                    "hora": tempo,
                                                    "forca_vela":forca_vela,
                                                    "atr":atr
                                                }

                                                # adiciona à lista (não substitui)
                                                self.resultados.append(resultado_item)
                                           
                                         
                                                self.Verify_estrategias(tempo)
                                                self.Verify_buy_sell(tempo,close,atr,periodo,intervalo,TPx,SLx)
                                                capital = self.Verify_lucro(tempo,close,aplicador,capital)
                                                
                                                
                                                #print(f"\n-{tempo} --- Close:{close:.2f}")
                                                



                                                '''caixa.insert(
                                                    "1.0",
                                                    f"\n---== {intervalo}: \n"
                                                    f"Close: {close:.2f}\nHigh: {high:.2f}\nLow: {low:.2f}\nOpen: {open_:.2f}\n\n"
                                                )'''
                                                if capital <= 0:
                                                    caixa.insert("1.0", "\n=== CAPITAL PERDIDO ❌💸====.\n")
                                                    caixa.configure(state="disabled")
                                                    break
                                            
                                            # Calculo Retorno Anualizado (RA)
                                            dias = (tempo - tempo_ini).days
                                            if dias >= 90:
                                                RA = self.Retorno_anualizado(capital_ini,capital,dias)
                                                #Constancia = self.Consistencia()
                                            else:
                                                RA = None
                                                #Constancia = None

                                            # Calculo MDD
                                            MDD = self.MDD()

                                            # Calculo DD
                                            DD = self.DD()
                                            
                                            # Calculo Winrate
                                            Winrate = self.Winrate()

                                            # Calculo R:R
                                            R_R = self.R_R()
                                            
                                            Expectancy = self.Expectancy(Winrate)

                                            Winrate_positivos.clear()
                                            Winrate_negativos.clear()
                                            Winrate_totais = 0
                                            MDD_list_capital.clear()

                                            if (RA is None or RA >= 0.15 ) and  DD <= 0.3 and Winrate >= 0.45 and R_R >= 2 and MDD <= 0.20 and (capital - capital_ini) > 0 and Expectancy > 0.20: 
                                                lista_melhores_tickers.append([ticker, periodo, intervalo, capital - capital_ini , RA, MDD, DD, Winrate, R_R, Expectancy, TPx, SLx])
                                            
                                            
                                            

                                        except Exception as e:
                                            resultado = GoogleTranslator(source='auto', target='pt').translate(str(e))
                                            caixa.insert("1.0", f"\n {tempo} -- {intervalo} !!!Erro ao processar dados ❌\n {resultado}")
                                    if capital > capital_ini:
                                        BACKT_lucro_dire = "✅"

                                    elif capital < capital_ini:
                                        BACKT_lucro_dire = "❌"
                                    else:
                                        BACKT_lucro_dire = "⚪"
                                    caixa.insert("1.0",f"====== -- LUCRO TOTAL: {capital - capital_ini:.3f} R$ -- ====== {BACKT_lucro_dire} -- Capital: {capital:.3f} R$  |  RA: {RA}  |  MDD: {MDD}  |  DD: {DD}  |  Winrate: {Winrate}  |  R_R: {R_R}  |  Expectancy: {Expectancy}  | \n\n\n\n")
                                    caixa.insert("1.0", f"\n{10*"-"} {intervalo} {10*"-"}\n")

                                caixa.insert("1.0", f"{30*"="} {periodo} {30*"="}\n\n")
                            caixa.insert("1.0", f"\n{60*'-'}======= {ticker} ======={60*'-'}\n\n\n")
                            
                    else:
                        caixa.insert("1.0", "❌ Nenhum ticker encontrado.\n")       
                else:
                    caixa.insert("1.0", "❌ Coluna 'Ticker' não encontrada no arquivo.\n")
            else:
                caixa.insert("1.0", "⚠️ Corrija os filtros antes de continuar.\n")

            caixa.insert("1.0", "\n✅ Finalizado!\n")
            for row in lista_melhores_tickers:
                caixa.insert("1.0", f"\n🏆 Ticker: {row[0]} | Período: {row[1]} | Intervalo: {row[2]} -- | -- Lucro: {row[3]:.2f} R$ -- | -- RA: {row[4]} | MDD: {row[5]} | DD: {row[6]} | Winrate: {row[7]} | R:R: {row[8]} | Expectancy: {row[9]} -- | -- TP {int(row[10]*100)}% | TP {int(row[11]*100)}%\n")

           
            start_bckt_flag = False

            janela.after(0, lambda: (
            btn_start.configure(state="normal", fg_color="#4E8F69"),
            btn_stop.configure(state="disabled", fg_color="gray"),
            btn_clear.configure(state="normal", fg_color="purple",command=clear_BKCT)
            ))
        
            
            caixa.configure(state="disabled")

        # =====================
        # FUNÇÃO STOP
        # =====================
        def Stop_BCKT():

            nonlocal stop_bckt_flag
            nonlocal start_bckt_flag
            stop_bckt_flag = True  # muda a flag → loop vai parar
            start_bckt_flag = False
            janela.after(0, lambda: (
                btn_start.configure(state="normal", fg_color="#4E8F69"),
                btn_stop.configure(state="disabled", fg_color="gray"),
                btn_clear.configure(state="normal", fg_color="purple", command=clear_BKCT)
            ))
          

        # =====================
        # FUNÇÃO CLEAR
        # =====================
        def clear_BKCT():

            nonlocal stop_bckt_flag
            nonlocal start_bckt_flag
            if stop_bckt_flag == True or start_bckt_flag == False:
                try:
                    janela.after(0, lambda: (
                        caixa.configure(state="normal"),
                        caixa.delete("1.0", "end"),
                        caixa.configure(state="disabled"),
                        print("🧹 Caixa limpa com sucesso!"),
                        btn_clear.configure(state="disabled", fg_color="gray")
                    ))
                   
                except Exception as e:
                    print(f"Erro ao limpar a caixa: {e}")
                

        # =====================
        # BOTÕES
        # =====================
        frame_botoes = ctk.CTkFrame(janela)
        frame_botoes.pack(pady=(0, 40))

        # Botão START
        btn_start = ctk.CTkButton(
            frame_botoes,
            text="Começar",
            width=220,
            height=40,
            command=lambda: threading.Thread(target=Start_BCKT, args=(caixa,)).start()
        )
        btn_start.pack(side="left", padx=3)

        # Botão STOP
        btn_stop = ctk.CTkButton(
            frame_botoes,
            text="⏹️",
            width=40,
            height=40,
            fg_color="gray",
            command=Stop_BCKT
        )
        btn_stop.pack(side="left", padx=3)

        # Botão CLEAR
        clear_img = ctk.CTkImage(
            light_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_clear.png"),
            dark_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_clear.png"),
            size=(25, 25)
        )
        btn_clear = ctk.CTkButton(
            frame_botoes,
            image=clear_img,
            corner_radius=20,
            text="",
            width=25,
            height=25,
            fg_color="purple",
            command=clear_BKCT
        )
        btn_clear.configure(state="disabled", fg_color="gray", command=None)
        btn_clear.pack(side="left", padx=10)

        janela.mainloop()






    #--- Filtro
    def BACKT_filtro(self):
        filtro_janela = ctk.CTkToplevel(self)
        filtro_janela.title("Filtros")
        filtro_janela.geometry("460x550")
        filtro_janela.resizable(False, False)
        filtro_janela.grab_set()
        
        # Carrega DFs iniciais
        df_in = pd.read_csv(BACKT_arquivo_filtro_in)
        df_pe = pd.read_csv(BACKT_arquivo_filtro_pe)

        # UI
        ctk.CTkLabel(filtro_janela, text="Selecione os filtros desejados",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        frame_principal = ctk.CTkFrame(filtro_janela)
        frame_principal.pack(pady=10, padx=10)

        frame_intervalo = ctk.CTkFrame(frame_principal)
        frame_intervalo.grid(row=0, column=0, padx=25, pady=5, sticky="n")

        frame_periodo = ctk.CTkFrame(frame_principal)
        frame_periodo.grid(row=0, column=1, padx=25, pady=5, sticky="n")

        # estados e botoes
        if not hasattr(self, "estado_estrategias"):
            self.estado_estrategias = {}  # nome -> 0/1
        if not hasattr(self, "botoes_filtros"):
            self.botoes_filtros = {}      # nome -> botão (CTkButton)

        def aplicar_All(pein):
            caminho = f"D:\\Progamacao\\Python\\ADT\\CSV\\variaveis\\ADT_filtro_back_test_{pein}.csv"
            try:
                df = pd.read_csv(caminho)
            except FileNotFoundError:
                print("Arquivo não encontrado:", caminho)
                return

            # força coluna 1 para int (se estiver como "0"/"1")
            try:
                df.iloc[:, 1] = df.iloc[:, 1].astype(int)
            except Exception:
                # se algo não bater, converte item a item
                df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: int(str(x).strip()) if str(x).strip().isdigit() else 0)

            # checa se todos são 1
            if (df.iloc[:, 1] == 1).all():
                novo_valor = 0
                #print("🔴 Todos os valores agora serão 0")
            else:
                novo_valor = 1
                #print("🟢 Todos os valores agora serão 1")

            # aplica no dataframe e salva
            df.iloc[:, 1] = novo_valor
            df.to_csv(caminho, index=False)

            # atualiza estado interno (dicionário) e UI dos botões
            for chave in list(self.estado_estrategias.keys()):
                # se a chave pertence ao pein atual (você pode filtrar por nome se quiser separar periodos/intervalos)
                # aqui assumimos que a lista de keys contém todos os nomes de ambas as colunas
                if "intervalo" in df.columns:
                    if (df["intervalo"] == chave).any():
                        self.estado_estrategias[chave] = novo_valor
                        btn = self.botoes_filtros.get(chave)
                        if btn:
                            if novo_valor == 1:
                                btn.configure(text="✅", fg_color="green")
                            else:
                                btn.configure(text="➕", fg_color="gray")
                if "periodo" in df.columns:
                    if (df["periodo"] == chave).any():
                        self.estado_estrategias[chave] = novo_valor
                        btn = self.botoes_filtros.get(chave)
                        if btn:
                            if novo_valor == 1:
                                btn.configure(text="✅", fg_color="green")
                            else:
                                btn.configure(text="➕", fg_color="gray")
               
                        
           
                        
            #print("✅ Aplicar_All concluído!")

        # botões All
        btn_aplicar_all_pe = ctk.CTkButton(frame_intervalo, text="All", width=20, height=25,
                                        font=ctk.CTkFont(size=7, weight="bold"),
                                        command=lambda pein="in": aplicar_All(pein))
        btn_aplicar_all_pe.pack(pady=(15, 10))

        btn_aplicar_all_in = ctk.CTkButton(frame_periodo, text="All", width=20, height=25,
                                        font=ctk.CTkFont(size=7, weight="bold"),
                                        command=lambda pein="pe": aplicar_All(pein))
        btn_aplicar_all_in.pack(pady=(15, 10))

        # cabeçalhos
        
        ctk.CTkLabel(frame_periodo, text="Período:", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame_intervalo, text="Intervalo:", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        

        def toggle(btn=None, nome=None):
            novo = 1 - self.estado_estrategias.get(nome, 0)
            self.estado_estrategias[nome] = novo
            if novo == 1:
                btn.configure(text="✅", fg_color="green")
            else:
                btn.configure(text="➕", fg_color="gray")

        # criar linha: preenche estado_estrategias e botoes_filtros ao criar
        def criar_linha(frame, nome, pein):
            linha = ctk.CTkFrame(frame)
            linha.pack(anchor="w", pady=3)
            ctk.CTkLabel(linha, text=nome, width=70, anchor="w").pack(side="left", padx=5)

            btn_toggle = ctk.CTkButton(linha, text="➕", width=28, height=25, fg_color="gray")
            btn_toggle.pack(side="left", padx=5)
            btn_toggle.configure(command=lambda b=btn_toggle, n=nome: toggle(b, n))

            # registra botão para controles "All"
            self.botoes_filtros[nome] = btn_toggle

            # lê CSV e configura estado inicial (se existir)
            caminho = f"D:\\Progamacao\\Python\\ADT\\CSV\\variaveis\\ADT_filtro_back_test_{pein}.csv"
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    leitor = csv.reader(f)
                    next(leitor, None)
                    encontrado = False
                    for dados in leitor:
                        if len(dados) >= 2:
                            nome_i, numero = dados[0], dados[1]
                            if nome_i == nome:
                                try:
                                    v = int(str(numero).strip())
                                except:
                                    v = 0
                                self.estado_estrategias[nome] = v
                                if v == 1:
                                    btn_toggle.configure(text="✅", fg_color="green")
                                else:
                                    btn_toggle.configure(text="➕", fg_color="gray")
                                encontrado = True
                                break
                    if not encontrado:
                        # se não encontrou no CSV, inicializa como 0
                        self.estado_estrategias.setdefault(nome, 0)
            except FileNotFoundError:
                # arquivo não existe: inicializa como 0
                self.estado_estrategias.setdefault(nome, 0)

        # cria linhas
        for nome in opcoes_intervalo:
            criar_linha(frame_intervalo, nome, "in")
        for nome in opcoes_periodo:
            criar_linha(frame_periodo, nome, "pe")

        # aplicar final -> grava estado_estrategias nos dois CSVs
        def aplicar():
            #print("Filtros selecionados:")
            # atualiza df_pe e df_in a partir do dicionário de estados
            # pega uma cópia pra garantir leitura atual
            df_in_local = pd.read_csv(BACKT_arquivo_filtro_in)
            df_pe_local = pd.read_csv(BACKT_arquivo_filtro_pe)

            for chave, valor in self.estado_estrategias.items():
                #print(f"{chave}: {'✅' if valor == 1 else '❌'}")
                # tenta atualizar em ambos (um dos dois terá correspondência)
                if "intervalo" in df_in_local.columns:
                    if (df_in_local["intervalo"] == chave).any():
                        df_in_local.loc[df_in_local["intervalo"] == chave, "intervalo_01"] = valor
                if "periodo" in df_pe_local.columns:
                    if (df_pe_local["periodo"] == chave).any():
                        df_pe_local.loc[df_pe_local["periodo"] == chave, "periodo_01"] = valor

            # salva ambos
            df_in_local.to_csv(BACKT_arquivo_filtro_in, index=False)
            df_pe_local.to_csv(BACKT_arquivo_filtro_pe, index=False)

            filtro_janela.destroy()

        btn_aplicar = ctk.CTkButton(filtro_janela, text="Aplicar", width=120, height=55,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                command=aplicar)
        btn_aplicar.pack(pady=(15, 10))

    def BACKT_money(self):
        global capital_set, aplicar_set, aplicar_porc_set
        filtro_janela = ctk.CTkToplevel(self)
        filtro_janela.title("Filtros")
        filtro_janela.geometry("400x450")
        filtro_janela.resizable(False, False)
        filtro_janela.grab_set()

        # UI
        ctk.CTkLabel(filtro_janela, text="Selecione os filtros desejados",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        frame_principal = ctk.CTkFrame(filtro_janela)
        frame_principal.pack(pady=10, padx=10)

        frame_capital = ctk.CTkFrame(frame_principal)
        frame_capital.grid(row=0, column=0, padx=10, pady=(50,0), sticky="n")
        
        frame_Atr = ctk.CTkFrame(frame_principal)
        frame_Atr.grid(row=1, column=0,columnspan=2,  padx=20, pady=(30,5), sticky="n")

        frame_aplicado = ctk.CTkFrame(frame_principal)
        frame_aplicado.grid(row=0, column=1, padx=10, pady=(30,0), sticky="n")

        df = pd.read_csv(Arquivo_info_money)
        capital = df["capital"][0]
        aplicado = df["aplicado"][0]
        aplicado_porc = df["aplicado_porc"][0]
        aplicar_01 = df["aplicar_01"][0]

        TPx = df["TPx"][0]
        SLx = df["SLx"][0]

         # cabeçalhos
        ctk.CTkLabel(frame_capital, text="Capital", font=ctk.CTkFont(weight="bold",size=20)).pack(pady=(0, 5))
        ctk.CTkLabel(frame_aplicado, text="Aplicar", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        

        # ==== Capital ====
        capital_row = ctk.CTkFrame(frame_capital)
        capital_row.pack(pady=5)

        capital_set = ctk.CTkEntry(capital_row, width=100, justify="center")
        capital_set.insert(0, f"{capital}")
        capital_set.pack(side="left")

        ctk.CTkLabel(capital_row, text="R$", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)


        # ==== Aplicar Dinheiro ====
        aplicar_row = ctk.CTkFrame(frame_aplicado)
        aplicar_row.pack(pady=5)

        aplicar_set = ctk.CTkEntry(aplicar_row, width=50, justify="center")
        aplicar_set.insert(0, f"{aplicado}")
        aplicar_set.pack(side="left")

        ctk.CTkLabel(aplicar_row, text="R$", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)


        # ==== Aplicar Porcentagem ====
        aplicar_porc_row = ctk.CTkFrame(frame_aplicado)
        aplicar_porc_row.pack(pady=5)

        aplicar_porc_set = ctk.CTkEntry(aplicar_porc_row, width=50, justify="center")
        aplicar_porc_set.insert(0, f"{aplicado_porc}")
        aplicar_porc_set.pack(side="left")

        ctk.CTkLabel(aplicar_porc_row, text= "%", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)


        #==== Take Proft  ====
        
        ctk.CTkLabel(frame_Atr, text="Projeçao ATR", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        
        ATR_row = ctk.CTkFrame(frame_Atr)
        ATR_row.pack(pady=5)
        
        ctk.CTkLabel(ATR_row, text= "TP: ", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)

        TP_set = ctk.CTkEntry(ATR_row, width=50, justify="center")
        TP_set.insert(0, f"{int(TPx*100)}")
        TP_set.pack(side="left")
        
        ctk.CTkLabel(ATR_row, text= " %", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,20))

        #==== Stop Loss  ====
        
        ctk.CTkLabel(ATR_row, text= "SL:", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)

        SL_set = ctk.CTkEntry(ATR_row, width=50, justify="center")
        SL_set.insert(0, f"{int(SLx*100)}")
        SL_set.pack(side="left")
        
        ctk.CTkLabel(ATR_row, text= " %", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0,5))

    









        if aplicar_01 == True:
            aplicar_porc_set.configure(fg_color = "gray",border_color = "gray")
            aplicar_set.configure(fg_color = "#5E7B6B",border_color = "#465D54")

        elif aplicar_01 == False:
            aplicar_set.configure(fg_color = "gray",border_color = "gray")
            aplicar_porc_set.configure(fg_color = "#5E7B6B",border_color = "#465D54")

        def quando_focar(event):
         
            widget = event.widget
          
            # Se não tiver .nome, tenta pegar do widget pai
            if not hasattr(widget, "nome"):
                widget = widget.master

            if hasattr(widget, "nome"):
                print(widget.nome)
                if widget.nome == "aplicar":
                    df.loc[0,"aplicar_01"] = True
                    aplicar_porc_set.configure(fg_color = "gray",border_color = "gray")
                    aplicar_set.configure(fg_color = "#5E7B6B",border_color = "#465D54")
               
                    df.to_csv(Arquivo_info_money,index=None)
                elif widget.nome == "aplicar_porc":
                    df.loc[0,"aplicar_01"] = False
                    aplicar_set.configure(fg_color = "gray",border_color = "gray")
                    aplicar_porc_set.configure(fg_color = "#5E7B6B",border_color = "#465D54")
                    df.to_csv(Arquivo_info_money,index=None)


        capital_set.nome = "capital"
        aplicar_set.nome = "aplicar"
        aplicar_porc_set.nome = "aplicar_porc"

        capital_set.bind("<FocusIn>", quando_focar)
        aplicar_set.bind("<FocusIn>", quando_focar)
        aplicar_porc_set.bind("<FocusIn>", quando_focar)

        

        def aplicar():
            df = pd.read_csv(Arquivo_info_money)
            capital = df["capital"][0]
            aplicado = df["aplicado"][0]
            aplicado_porc = df["aplicado_porc"][0]
            TPx = df["TPx"][0]
            SLx = df["SLx"][0]
                # pegar valores
            cap_text = capital_set.get()
            aplic_text = aplicar_set.get()
            porc_text = aplicar_porc_set.get()
            TPx_text = TP_set.get()
            SLx_text = SL_set.get()

            if cap_text == "":
                cap_text = capital 
                capital_set.delete(0, "end")
                capital_set.insert(0, f"{capital}")

            if aplic_text == "":
                aplic_text = aplicado

            if porc_text == "":
                porc_text = aplicado_porc
            
            if TPx_text == "":
                TPx_text = TPx
            if SLx_text == "":
                SLx_text = SLx
            
    
            
            #print(cap_text, aplic_text, porc_text, TPx_text, SLx_text)
            
            #Verificar se e float -----------
            try:
                capital_ = float(cap_text)
            except ValueError:
                print("ERRO: valores digitados não são números")
                capital_set.delete(0, "end")
                capital_set.insert(0, f"{capital}")
                return   
            
            try:
                aplicado_ = float(aplic_text)
               
            except ValueError:
                print("ERRO: valores digitados não são números")
                aplicar_set.delete(0, "end")
                aplicar_set.insert(0, f"{aplicado}")
                return    
            try:
                aplicado_porc_ = float(porc_text)
            except ValueError:
                print("ERRO: valores digitados não são números")
                aplicar_porc_set.delete(0, "end")
                aplicar_porc_set.insert(0, f"{aplicado_porc}")
                return  
            
            try:
                TPx_ = float(TPx_text)
            except ValueError:
                print("ERRO: valores digitados não são números")
                TP_set.delete(0, "end")
                TP_set.insert(0, f"{int(TPx*100)}")
                return
            try:
                SLx_ = float(SLx_text)
            except ValueError:
                print("ERRO: valores digitados não são números")
                SL_set.delete(0, "end")
                SL_set.insert(0, f"{int(SLx*100)}")
                return

    
            if capital_ <= 0:
                capital_ = capital
                capital_set.delete(0, "end")
                capital_set.insert(0, f"{capital}")
            else:
                df.loc[0, "capital"] = capital_

            if aplicado_<= 0 or aplicado_ > capital_:
                aplicado_ = aplicado
                aplicar_set.delete(0, "end")
                aplicar_set.insert(0, f"{aplicado}")
            else:
                df.loc[0, "aplicado"] = aplicado_
            
            if aplicado_porc_ <=0 or aplicado_porc_ >100:
                aplicado_porc_ = aplicado_porc
                aplicar_porc_set.delete(0, "end")
                aplicar_porc_set.insert(0, f"{aplicado_porc}")
            else:
                df.loc[0, "aplicado_porc"] = aplicado_porc_

            #print(f"Tpx text = {TPx_text} | Tpx_ = {TPx_} | TPx = {TPx} | SLx text = {SLx_text} | SLx_ = {SLx_} | SLx = {SLx}")
            if TPx_ <= 0:
                TPx_ = TPx
                TP_set.delete(0, "end") 
                TP_set.insert(0, f"{int(TPx_*100)}")
            else:
                df.loc[0, "TPx"] = TPx_/100
            
            if SLx_ <= 0:
                SLx_ = SLx
                SL_set.delete(0, "end")
                SL_set.insert(0, f"{int(SLx_*100)}")
            else:
                df.loc[0, "SLx"] = SLx_/100
            
            df.to_csv(Arquivo_info_money,index=None)
           
            
          

            

        btn_aplicar = ctk.CTkButton(filtro_janela, text="Aplicar", width=120, height=55,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                command=aplicar)
        btn_aplicar.pack(pady=(15, 10))
        filtro_janela.bind('<Return>', lambda event: aplicar())
        
        
        


    # ==== Editar Estrategias ====
    def Editar_estrategias(self):
        if not hasattr(self, "botoes_toggle"):
            self.botoes_toggle = {}
        global Verificar_largura, verificar_def_estrategia
        verificar_def_estrategia = True
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="Editar Estrategias ⚙", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)
    
        # Frame para colocar os botões
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=10)      
        df = pd.read_csv(Estrategias_arquivo_variaveis)

        config_img = ctk.CTkImage(
            light_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Editar-Estrategias\img_config.png"),
            dark_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Editar-Estrategias\img_config.png"),
            size=(30, 30)
        )
       
        btn_config = ctk.CTkButton(
            self, text="", image=config_img,
            corner_radius=20, width=30, height=30,
            command=self.EDTE_config
        )
        btn_config.place(x=10, y=10)


        

       

        # Dicionário para armazenar estado
        
        if not hasattr(self, "estado_estrategias"):
            self.estado_estrategias = {}
        
        
        with open(Estrategias_arquivo_variaveis, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            next(leitor)  # pular cabeçalho

                
            frame_Estrategia = ctk.CTkFrame(frame_botoes)
            
            ctk.CTkLabel(frame_Estrategia, text="Estrategias:", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

            frame_Price_a = ctk.CTkFrame(frame_botoes)
            
            
            ctk.CTkLabel(frame_Price_a, text="Price Action:", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

            frame_Indicadores = ctk.CTkFrame(frame_botoes)
            
            
            ctk.CTkLabel(frame_Indicadores, text="Indicadores:", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
            if Verificar_largura:
                frame_Estrategia.grid(row=0, column=0, padx=25, pady=20, sticky="n")
                frame_Price_a.grid(row=0, column=1, padx=25, pady=20, sticky="n")
                frame_Indicadores.grid(row=0, column=2, padx=25, pady=20, sticky="n")

            else:
                frame_Estrategia.pack(pady=(20, 50))
                frame_Price_a.pack(pady=(15, 50))
                frame_Indicadores.pack(pady=(15, 50))

            for dados in leitor:
                nome, valor, classe = dados[0], int(dados[1]), str(dados[3])
                # Salva o estado inicial no dicionário
               
                self.estado_estrategias[nome] = valor
                frame_btt = frame_botoes
                if classe == "Estr":
                    frame_btt = frame_Estrategia
                elif classe == "Price_a":
                    frame_btt = frame_Price_a
                elif classe == "Ind":
                    frame_btt = frame_Indicadores

                linha_frame = ctk.CTkFrame(frame_btt)
                linha_frame.pack(pady=5)

                btn_principal = ctk.CTkButton(linha_frame, text=nome, width=220, height=40)
                btn_principal.pack(side="left", padx=5)

                if nome == Estrategias[0][0]:
                    btn_principal.configure(command=self.ISNB_Menu)

                if nome == Estrategias[1][0]:
                    btn_principal.configure(command=self.RSI_e_EMA_Menu)

                if nome == Estrategias[2][0]:
                    btn_principal.configure(command=self.RSI_Menu)

                if nome == Estrategias[3][0]:
                    btn_principal.configure(command=self.Pivo_P_Menu)

                # Função toggle corrigida
                def toggle(btn=None, n=nome):
                    # Estado atual
                    v = self.estado_estrategias[n]
                    v = 1 - v  # inverter
                    self.estado_estrategias[n] = v

                    # Ajustar cor do botão
                    if v == 1:
                        btn.configure(text="✅", fg_color="green")
                    else:
                        btn.configure(text="➕", fg_color="gray")

                    # Atualizar CSV
                    df.loc[df["estrategia"] == n, "estrategia_01"] = v

                    # =====================================================
                    # BLOQUEIO: RSI e RSI+EMA NÃO PODEM FICAR ATIVOS JUNTOS
                    # =====================================================
                    if v == 1:  # só se ativou
                        if n == "Rsi":
                            # desativar RSI+EMA
                            self.estado_estrategias["Rsi + EMA"] = 0
                            df.loc[df["estrategia"] == "Rsi + EMA", "estrategia_01"] = 0

                            # atualizar visual ao vivo
                            btn_ema = self.botoes_toggle.get("Rsi + EMA")
                            if btn_ema:
                                btn_ema.configure(text="➕", fg_color="gray")

                        if n == "Rsi + EMA":
                            # desativar RSI
                            self.estado_estrategias["Rsi"] = 0
                            df.loc[df["estrategia"] == "Rsi", "estrategia_01"] = 0

                            # atualizar visual ao vivo
                            btn_rsi = self.botoes_toggle.get("Rsi")
                            if btn_rsi:
                                btn_rsi.configure(text="➕", fg_color="gray")

                    # salvar CSV definitivo
                    df.to_csv(Estrategias_arquivo_variaveis, index=False)
                   

                # Botão lateral
                btn_toggle = ctk.CTkButton(linha_frame, text="➕", width=40, height=40, fg_color="gray")
                btn_toggle.pack(side="left", padx=5)

                # Estado visual inicial
                if valor == 1:
                    btn_toggle.configure(text="✅", fg_color="green")

                self.botoes_toggle[nome] = btn_toggle
                # Vincula comando
                btn_toggle.configure(command=lambda b=btn_toggle, n=nome: toggle(b, n))
               


            # Botão Voltar
            botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby)
            botao_voltar.pack(side="bottom", pady=30)

    def EDTE_config(self):
        filtro_janela = ctk.CTkToplevel(self)
        filtro_janela.title("Filtros")
        filtro_janela.geometry("600x450")
        filtro_janela.resizable(False, False)
        filtro_janela.grab_set()

        # UI
        ctk.CTkLabel(filtro_janela, text="Selecione os filtros desejados",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        frame_principal = ctk.CTkFrame(filtro_janela)
        frame_principal.pack(pady=10, padx=10)




        frame_forca_min = ctk.CTkFrame(frame_principal)
        frame_forca_min.grid(row=0, column=0, padx=10, pady=(30,0), sticky="n")
        
        frame_mult_price = ctk.CTkFrame(frame_principal)
        frame_mult_price.grid(row=0, column=1, padx=20, pady=(30,0), sticky="n")

        frame_tolerancia = ctk.CTkFrame(frame_principal)
        frame_tolerancia.grid(row=0, column=2, padx=10, pady=(30,0), sticky="n")

        frame_classes_pes = ctk.CTkFrame(frame_principal)
        frame_classes_pes.grid(row=1, column=1, columnspan=1,padx=10, pady=(30,30), sticky="n")

        df = pd.read_csv(EDTE_arquivo_config)

        forca_min = df["forca_min"][0]
        mult_price_a = df["mult_price_a"][0]
        tolerancia = df["tolerancia"][0]
        pes_estr = df["pes_estr"][0]
        pes_price_a = df["pes_price_a"][0]
        pes_ind = df["pes_ind"][0]
       
         # cabeçalhos
        ctk.CTkLabel(frame_forca_min, text="Força Minima", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame_mult_price, text="Price Action", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame_tolerancia, text="Toler Conflito", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        ctk.CTkLabel(frame_classes_pes, text="Classes pesos", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))
        

        # ==== Força Minima ====
        forca_min_row = ctk.CTkFrame(frame_forca_min)
        forca_min_row.pack(pady=5)

        forca_min_set = ctk.CTkEntry(forca_min_row, width=50, justify="center")
        forca_min_set.insert(0, f"{forca_min}")
        forca_min_set.pack(side="left")

        #tk.CTkLabel(forca_min_row, text="R$", font=ctk.CTkFont(size=14)).pack(side="left", padx=5)


        # ==== Multiplicador Price Action ====
        mult_price_row = ctk.CTkFrame(frame_mult_price)
        mult_price_row.pack(pady=5)

        mult_price_set = ctk.CTkEntry(mult_price_row, width=50, justify="center")
        mult_price_set.insert(0, f"{mult_price_a}")
        mult_price_set.pack(side="left")

        ctk.CTkLabel(mult_price_row, text="x", font=ctk.CTkFont(size=10)).pack(side="left", padx=5)


        # ==== Tolerancia a conflito ====
        tolerancia_row = ctk.CTkFrame(frame_tolerancia)
        tolerancia_row.pack(pady=5)

        tolerancia_set = ctk.CTkEntry(tolerancia_row, width=50, justify="center")
        tolerancia_set.insert(0, f"{tolerancia}")
        tolerancia_set.pack(side="left")

        #ctk.CTkLabel(tolerancia_row, text="x", font=ctk.CTkFont(size=10)).pack(side="left", padx=5)


         # ==== CLASSES PESO ====
        classes_pes_row = ctk.CTkFrame(frame_classes_pes)
        classes_pes_row.pack(pady=5)
        ctk.CTkLabel(classes_pes_row, text="|", font=ctk.CTkFont(size=20)).pack(side="left", padx=(15,2))

        ctk.CTkLabel(classes_pes_row, text="ESTR:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(5,5))
        class_Estrategia_set = ctk.CTkEntry(classes_pes_row, width=50, justify="center")
        class_Estrategia_set.insert(0, f"{pes_estr}")
        class_Estrategia_set.pack(side="left")

        ctk.CTkLabel(classes_pes_row, text="|", font=ctk.CTkFont(size=20)).pack(side="left", padx=(5,2))
        
        ctk.CTkLabel(classes_pes_row, text="PRIC_A:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(5,5))
        class_Price_a_set = ctk.CTkEntry(classes_pes_row, width=50, justify="center")
        class_Price_a_set.insert(0, f"{pes_price_a}")
        class_Price_a_set.pack(side="left")

        ctk.CTkLabel(classes_pes_row, text="|", font=ctk.CTkFont(size=20)).pack(side="left", padx=(5,2))

        ctk.CTkLabel(classes_pes_row, text="INDI:", font=ctk.CTkFont(size=10)).pack(side="left", padx=(5,5))
        class_Indicador_set = ctk.CTkEntry(classes_pes_row, width=50, justify="center")
        class_Indicador_set.insert(0, f"{pes_ind}")
        class_Indicador_set.pack(side="left")

        ctk.CTkLabel(classes_pes_row, text="|", font=ctk.CTkFont(size=20)).pack(side="left", padx=(5,5))
        #ctk.CTkLabel(tolerancia_row, text="x", font=ctk.CTkFont(size=10)).pack(side="left", padx=5)


        def aplicar():
            df = pd.read_csv(EDTE_arquivo_config)

            # valores atuais no CSV
            forca_min = df["forca_min"][0]
            mult_price_a = df["mult_price_a"][0]
            tolerancia = df["tolerancia"][0]
            pes_estr = df["pes_estr"][0]
            pes_price_a = df["pes_price_a"][0]
            pes_ind = df["pes_ind"][0]

            # pegar valores digitados
            forca_text = forca_min_set.get()
            mult_price_text = mult_price_set.get()
            toler_text = tolerancia_set.get()
            pes_estr_text = class_Estrategia_set.get()
            pes_price_a_text = class_Price_a_set.get()
            pes_ind_text = class_Indicador_set.get()

            # ==============================
            # Se estiver vazio, volta valor original
            # ==============================
            if forca_text == "":
                forca_text = forca_min
                forca_min_set.delete(0, "end")
                forca_min_set.insert(0, f"{forca_min}")

            if mult_price_text == "":
                mult_price_text = mult_price_a
                mult_price_set.delete(0, "end")
                mult_price_set.insert(0, f"{mult_price_a}")

            if toler_text == "":
                toler_text = tolerancia
                tolerancia_set.delete(0, "end")
                tolerancia_set.insert(0, f"{tolerancia}")

            if pes_estr_text == "":
                pes_estr_text = pes_estr
                class_Estrategia_set.delete(0, "end")
                class_Estrategia_set.insert(0, f"{pes_estr}")

            if pes_price_a_text == "":
                pes_price_a_text = pes_price_a
                class_Price_a_set.delete(0, "end")
                class_Price_a_set.insert(0, f"{pes_price_a}")

            if pes_ind_text == "":
                pes_ind_text = pes_ind
                class_Indicador_set.delete(0, "end")
                class_Indicador_set.insert(0, f"{pes_ind}")

            # ==============================
            # VALIDAR NUMÉRICO
            # ==============================
            try:
                forca_min_ = float(forca_text)
            except ValueError:
                forca_min_set.delete(0, "end")
                forca_min_set.insert(0, f"{forca_min}")
                print("ERRO: valor inválido (força mínima)")
                return

            try:
                mult_price_a_ = float(mult_price_text)
            except ValueError:
                mult_price_set.delete(0, "end")
                mult_price_set.insert(0, f"{mult_price_a}")
                print("ERRO: valor inválido (Price Action mult.)")
                return

            try:
                tolerancia_ = float(toler_text)
            except ValueError:
                tolerancia_set.delete(0, "end")
                tolerancia_set.insert(0, f"{tolerancia}")
                print("ERRO: valor inválido (Tolerância)")
                return

            try:
                pes_estr_ = float(pes_estr_text)
                pes_price_a_ = float(pes_price_a_text)
                pes_ind_ = float(pes_ind_text)
            except ValueError:
                print("ERRO: Peso inválido")
                return

            # ==============================
            # VALIDAR NEGATIVO (correção)
            # ==============================
            if forca_min_ < 0:
                forca_min_ = forca_min
                forca_min_set.delete(0, "end")
                forca_min_set.insert(0, f"{forca_min}")

            if mult_price_a_ < 0:
                mult_price_a_ = mult_price_a
                mult_price_set.delete(0, "end")
                mult_price_set.insert(0, f"{mult_price_a}")

            if tolerancia_ < 0:
                tolerancia_ = tolerancia
                tolerancia_set.delete(0, "end")
                tolerancia_set.insert(0, f"{tolerancia}")

            # ==============================
            # SALVAR (correção de nomes de colunas)
            # ==============================
            df.loc[0, "forca_min"] = forca_min_
            df.loc[0, "mult_price_a"] = mult_price_a_        # estava escrito errado antes
            df.loc[0, "tolerancia"] = tolerancia_
            df.loc[0, "pes_estr"] = pes_estr_
            df.loc[0, "pes_price_a"] = pes_price_a_
            df.loc[0, "pes_ind"] = pes_ind_

            df.to_csv(EDTE_arquivo_config, index=False)

            print("\n✔ Filtros atualizados com sucesso!\n")

        btn_aplicar = ctk.CTkButton(filtro_janela, text="Aplicar", width=120, height=55,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                command=aplicar)
        btn_aplicar.pack(pady=(15, 10))
        filtro_janela.bind('<Return>', lambda event: aplicar())
            




 

    # ----- Inside Bar -----
    def ISNB_Menu(self):
        global peso_max
        self.limpar_tela()
        estrategia_nome = "Inside Bar"
        df = pd.read_csv(Estrategias_arquivo_variaveis)

        # número precisa ser variável da classe
        self.num = df.loc[df["estrategia"] == estrategia_nome, "peso"].iloc[0]
        
        def diminuir():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num > 1:
                self.num -= 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)


        def aumentar():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num < peso_max:
                self.num += 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)

        titulo = ctk.CTkLabel(self, text=f"{estrategia_nome} 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        ctk.CTkLabel(self, text="Peso", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

        # -------------------------------
        # FRAME horizontal
        # -------------------------------
        frame_central = ctk.CTkFrame(self)
        frame_central.pack(pady=20)

        # Botão -
        btn_min = ctk.CTkButton(frame_central, text="➖", width=80, command=diminuir)
        btn_min.pack(side="left", padx=5)

        # Número no centro
        peso = ctk.CTkLabel(
            frame_central,
            text=self.num,
            fg_color="#2E2E2E",
            text_color="white",
            corner_radius=10,
            width=200,
            height=40
        )
        peso.pack(side="left", padx=5)

        # Botão +
        btn_max = ctk.CTkButton(frame_central, text="➕", width=80, command=aumentar)
        btn_max.pack(side="left", padx=5)

        # -------------------------------

        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.Editar_estrategias)
        botao_voltar.pack(side="bottom", pady=30)


    def RSI_Menu(self):
        global peso_max
        self.limpar_tela()
        estrategia_nome = "Rsi"
        df = pd.read_csv(Estrategias_arquivo_variaveis)

        # número precisa ser variável da classe
        self.num = df.loc[df["estrategia"] == estrategia_nome, "peso"].iloc[0]
        
        def diminuir():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num > 1:
                self.num -= 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)


        def aumentar():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num < peso_max:
                self.num += 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)

        titulo = ctk.CTkLabel(self, text=f"{estrategia_nome} 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        ctk.CTkLabel(self, text="Peso", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

        # -------------------------------
        # FRAME horizontal
        # -------------------------------
        frame_central = ctk.CTkFrame(self)
        frame_central.pack(pady=20)

        # Botão -
        btn_min = ctk.CTkButton(frame_central, text="➖", width=80, command=diminuir)
        btn_min.pack(side="left", padx=5)

        # Número no centro
        peso = ctk.CTkLabel(
            frame_central,
            text=self.num,
            fg_color="#2E2E2E",
            text_color="white",
            corner_radius=10,
            width=200,
            height=40
        )
        peso.pack(side="left", padx=5)

        # Botão +
        btn_max = ctk.CTkButton(frame_central, text="➕", width=80, command=aumentar)
        btn_max.pack(side="left", padx=5)

        # -------------------------------

        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.Editar_estrategias)
        botao_voltar.pack(side="bottom", pady=30)

    def Pivo_P_Menu(self):
        global peso_max
        self.limpar_tela()
        estrategia_nome = "Pivot Points"
        df = pd.read_csv(Estrategias_arquivo_variaveis)

        # número precisa ser variável da classe
        self.num = df.loc[df["estrategia"] == estrategia_nome, "peso"].iloc[0]
        
        def diminuir():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num > 1:
                self.num -= 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)


        def aumentar():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num < peso_max:
                self.num += 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)

        titulo = ctk.CTkLabel(self, text=f"{estrategia_nome} 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        ctk.CTkLabel(self, text="Peso", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

        # -------------------------------
        # FRAME horizontal
        # -------------------------------
        frame_central = ctk.CTkFrame(self)
        frame_central.pack(pady=20)

        # Botão -
        btn_min = ctk.CTkButton(frame_central, text="➖", width=80, command=diminuir)
        btn_min.pack(side="left", padx=5)

        # Número no centro
        peso = ctk.CTkLabel(
            frame_central,
            text=self.num,
            fg_color="#2E2E2E",
            text_color="white",
            corner_radius=10,
            width=200,
            height=40
        )
        peso.pack(side="left", padx=5)

        # Botão +
        btn_max = ctk.CTkButton(frame_central, text="➕", width=80, command=aumentar)
        btn_max.pack(side="left", padx=5)

        # -------------------------------

        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.Editar_estrategias)
        botao_voltar.pack(side="bottom", pady=30)

    def RSI_e_EMA_Menu (self):
        global peso_max
        self.limpar_tela()
        estrategia_nome = "Rsi + EMA"
        df = pd.read_csv(Estrategias_arquivo_variaveis)

        # número precisa ser variável da classe
        self.num = df.loc[df["estrategia"] == estrategia_nome, "peso"].iloc[0]
        
        def diminuir():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num > 1:
                self.num -= 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)


        def aumentar():
            df = pd.read_csv(Estrategias_arquivo_variaveis)
            if self.num < peso_max:
                self.num += 1
                peso.configure(text=self.num)
                
                df.loc[df["estrategia"] == estrategia_nome, "peso"] = self.num
                df.to_csv(Estrategias_arquivo_variaveis,index=False)

        titulo = ctk.CTkLabel(self, text=f"{estrategia_nome} 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        ctk.CTkLabel(self, text="Peso", font=ctk.CTkFont(weight="bold")).pack(pady=(0, 5))

        # -------------------------------
        # FRAME horizontal
        # -------------------------------
        frame_central = ctk.CTkFrame(self)
        frame_central.pack(pady=20)

        # Botão -
        btn_min = ctk.CTkButton(frame_central, text="➖", width=80, command=diminuir)
        btn_min.pack(side="left", padx=5)

        # Número no centro
        peso = ctk.CTkLabel(
            frame_central,
            text=self.num,
            fg_color="#2E2E2E",
            text_color="white",
            corner_radius=10,
            width=200,
            height=40
        )
        peso.pack(side="left", padx=5)

        # Botão +
        btn_max = ctk.CTkButton(frame_central, text="➕", width=80, command=aumentar)
        btn_max.pack(side="left", padx=5)

        # -------------------------------

        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.Editar_estrategias)
        botao_voltar.pack(side="bottom", pady=30)
        
            
        
    # ==== Tickers ====
    def TKRS_Menu (self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="Tickers 📚", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)
        
        ctk.CTkButton(self, text="➕ Adicionar Tickers", width=220, height=40, command=self.TKRS_Add_tiker).pack(pady=10)
        ctk.CTkButton(self, text="📦 Adicionar Pacote de Tickers", width=220, height=40, command=self.TKRS_Add_pack_ticker).pack(pady=10)
        ctk.CTkButton(self, text="📋 Visualizar Tickers", width=220, height=40, command=self.TKRS_Vizuaizar_tiker).pack(pady=10)
        if len(pd.read_csv(Tickers_arquivo)) > 0:
            ctk.CTkButton(self, text="❌ Excluir Tickers", width=220, height=40, command=self.TKRS_Excluir_tiker).pack(pady=10)
        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby)
        botao_voltar.pack(side="bottom", pady=30)
    # --- Add Ticker


    def TKRS_Add_tiker(self):
        janela = ctk.CTkToplevel(self)
        janela.title("➕ Adicionar Dado")
        janela.geometry("300x250")
        janela.resizable(False, False)
        janela.grab_set()

        ctk.CTkLabel(janela, text="Ticker:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        nome_entry = ctk.CTkEntry(janela, width=200)
        nome_entry.pack(pady=5)
        nome_entry.focus()

        # Label de status
        status_label = ctk.CTkLabel(
            janela,
            text="⚠️ Preencha os campos",
            font=ctk.CTkFont(size=13),
            text_color="yellow"
        )
        status_label.pack(pady=10)

        # Variável para armazenar o after_id (para cancelar o delay anterior)
        delay_id = None

        def verificar_dowload_real():
            ISDB_df = pd.read_csv(Tickers_arquivo)
            nome = nome_entry.get().strip().upper()

            if not nome:
                status_label.configure(text="⚠️ Preencha os campos", text_color="yellow")
                return

            try:
                data = yf.download(nome, period="1d", progress=False, threads=False)
                if data.empty:
                    status_label.configure(text="❌ Ticker inválido", text_color="red")
                    return
            except Exception:
                status_label.configure(text="❌ Erro ao verificar", text_color="red")
                return

            if nome in ISDB_df["Ticker"].values:
                status_label.configure(text="⚠️ Ticker existente", text_color="yellow")
                return

            status_label.configure(text="✅ Ticker válido", text_color="green")

        # Função chamada ao digitar (com atraso)
        def verificar_dowload(event=None):
            nonlocal delay_id
            if delay_id:  # se já houver um timer ativo, cancela
                janela.after_cancel(delay_id)
            # agenda a execução real para daqui 500ms
            delay_id = janela.after(500, verificar_dowload_real)

        def salvar(event=None):
            ISDB_df = pd.read_csv(Tickers_arquivo)
            nome = nome_entry.get().strip().upper()

            if not nome:
                messagebox.showwarning("⚠️ Atenção", "Preencha todos os campos.")
                return

            try:
                data = yf.download(nome, period="1d", progress=False, threads=False)
                if data.empty:
                    messagebox.showerror("❌ Erro", f"O ticker '{nome}' é inválido ou não possui dados.")
                    return
            except Exception:
                messagebox.showerror("❌ Erro", f"Ocorreu um erro ao verificar o ticker '{nome}'.")
                return

            if nome in ISDB_df["Ticker"].values:
                messagebox.showwarning("⚠️ Atenção", "O ticker já existe.")
                return

            nova_linha = pd.DataFrame({'Ticker': [nome]})
            ISDB_df = pd.concat([ISDB_df, nova_linha], ignore_index=True)
            ISDB_df.to_csv(Tickers_arquivo, index=False)
            messagebox.showinfo("✅ Sucesso", "Ticker adicionado com sucesso!")
            janela.destroy()
            self.TKRS_Menu()

        nome_entry.bind("<KeyRelease>", verificar_dowload)
        ctk.CTkButton(janela, text="Salvar", width=120, height=35, command=salvar).pack(pady=20)
        janela.bind('<Return>', salvar)

        
    #--- Add Pack Ticker
    def TKRS_Add_pack_ticker(self):
        ISDB_pack = pd.read_csv(Tickers_pack_arquivo)

        if ISDB_pack.empty:
            messagebox.showinfo("ℹ️ ", "📭 Nenhum Ticker encontrado.")
            return

        ISDB_tickers = pd.read_csv(Tickers_arquivo)
        existentes = set(ISDB_tickers["Ticker"].values)
    
        cont_repetidos = 0

        for dado in ISDB_pack["Ticker"].values:
            if dado in existentes:
                cont_repetidos += 1
            else:
                nova_linha = pd.DataFrame({'Ticker': [dado]})
                ISDB_tickers = pd.concat([ISDB_tickers, nova_linha], ignore_index=True)

        ISDB_tickers.to_csv(Tickers_arquivo, index=False)

        messagebox.showinfo(
            "📦 Pacote de ticker adicionado ✅",
            f"{len(ISDB_pack)} Tickers adicionados\n⚠️ {cont_repetidos} Não adicionados (Repetidos)"
        )

        self.TKRS_Menu()



    # --- Vizualizar Ticker
    def TKRS_Vizuaizar_tiker(self):
        janela = ctk.CTkToplevel(self)
        janela.title("📋 Lista de Tickers")
        janela.geometry("400x300")
        janela.resizable(False, False)
        janela.grab_set()
        ISDB_df = pd.read_csv(Tickers_arquivo)

        if len(pd.read_csv(Tickers_arquivo)) <=0:
            ctk.CTkLabel(janela, text="📭 Nenhum Ticker encontrado.", font=ctk.CTkFont(size=14)).pack(pady=40)
            return

        caixa = ctk.CTkTextbox(janela, width=360, height=230, font=ctk.CTkFont(size=14))
        caixa.pack(pady=15)

        for i, dado in enumerate(ISDB_df["Ticker"].values, 1):

            caixa.insert("end", f"{i} - {dado}\n")

        caixa.configure(state="disabled")

    # --- Excluir Ticker
    def TKRS_Excluir_tiker(self):
            os.remove(Tickers_arquivo)
            ISDB_df = pd.DataFrame(columns=['Ticker'])
            ISDB_df.to_csv(Tickers_arquivo, index=False)
            self.TKRS_Menu()

            
            messagebox.showinfo("ℹ️ ", "EXCLUIR TICKER")

        
    

# ======= EXECUÇÃO =======
if __name__ == "__main__":
    app = LobbyApp()
    app.mainloop()
