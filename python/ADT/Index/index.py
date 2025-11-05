import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from binance.client import Client
import yfinance as yf


import os
import csv
import time
import pandas as pd

#Lobby_
ISDB_arquivo_dados = r"D:\Progamacao\Python\ADT\CSV\Dados\ADT_ISDB_Dados.csv"
Tickers_arquivo = r"D:\Progamacao\Python\ADT\CSV\Tickers\ADT_Tickers.csv"
Tickers_pack_arquivo =r'D:\Progamacao\Python\ADT\CSV\Tickers\ADT_Pack_TIckers.csv'

BACKT_arquivo_filtro_pe = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_filtro_back_test_pe.csv"
BACKT_arquivo_filtro_in = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_filtro_back_test_in.csv"

Estrategias_arquivo_vaiaveis = r"D:\Progamacao\Python\ADT\CSV\variaveis\ADT_estrategias_variaveis.csv"
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

opcoes_periodo = ["5min", "15min", "1hr", "1D", "1sem", "1m"]
opcoes_intervalo = ["1Dia", "1semana", "1mes","1y", "2y", "5y"]
if not os.path.exists(BACKT_arquivo_filtro_pe):
    with open(BACKT_arquivo_filtro_pe, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["periodo", "periodo_01","code"])
        for v,i in zip(opcoes_periodo,["5m","15m","1h","1d","1wk","1mo"]):
            escritor.writerow([v, 0, i]) # cabeçalho
if not os.path.exists(BACKT_arquivo_filtro_in):
    with open(BACKT_arquivo_filtro_in, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["intervalo", "intervalo_01","code"])  # cabeçalho
        for v,i in zip(opcoes_intervalo,["1d","7d","1mo","1y","2y","5y"]):
            escritor.writerow([v, 0, i]) # cabeçalho


 # Lista de estratégias
estrategias = ["Inside Bar", "Martelo"]
if not os.path.exists(Estrategias_arquivo_vaiaveis):
    with open(Estrategias_arquivo_vaiaveis, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["estrategia", "estrategia_01"])  # cabeçalho
        for v in estrategias:
            escritor.writerow([v, 0]) # cabeçalho
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



        self.lista_dados = []
        self.criar_lobby()

    # ======= LIMPAR TELA =======
    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ======= LOBBY PRINCIPAL =======
    def criar_lobby(self):
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
    
    #--- Back-test ---
    def Back_test(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Fazendo Back-Test 🧪")
        janela.geometry("900x506")
        janela.resizable(True, True)
        janela.grab_set()
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        filtro_img = ctk.CTkImage(
            light_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_filtro.png"),  # imagem modo claro
            dark_image=Image.open(r"D:\Progamacao\Python\ADT\Imagens\Back-Test\img_filtro.png"),   # imagem modo escuro
            size=(40, 40)  # tamanho da imagem no botão
        )

        btn_filtro = ctk.CTkButton(janela, text="",image=filtro_img ,corner_radius=20,width=40, height=40, command=self.BACKT_filtro)
        btn_filtro.pack(pady=(0,40))
        btn_filtro.place(x=10, y=10)


        
        caixa = ctk.CTkTextbox(janela, font=ctk.CTkFont(size=14))
        caixa.pack(padx=10, pady=(70,10), expand=True, fill="both")
        caixa.configure(state="disabled")

        def Start_BCKT(caixa):  
            #janela.after(1, lambda: Start_BCKT(caixa, i + 1, max_i))   
            df = pd.read_csv(Tickers_arquivo)
            df_pe = pd.read_csv(BACKT_arquivo_filtro_pe)
            df_in = pd.read_csv(BACKT_arquivo_filtro_in)

            min_5_15_h_1 = ['']

            soma_periodo = df_pe["periodo_01"].sum()
            soma_intevalo = df_in["intervalo_01"].sum()

            caixa.configure(state="normal")
            caixa.delete("1.0", "end")
            caixa.insert("end", "Período:\n")

            if soma_periodo == 0:
                caixa.insert("end", "⚠️ Ao menos 1 período deve ser selecionado!\n")

            if soma_intevalo == 0:
                caixa.insert("end", "⚠️ Ao menos 1 intervalo deve ser selecionado!\n")

            caixa.see("end")

            # Se ambos forem > 0
            if soma_periodo > 0 and soma_intevalo > 0:
                if "Ticker" in df.columns:
                    lista_tickers = df["Ticker"].tolist()
                    if len(lista_tickers) > 0:
                        for ticker in lista_tickers:
                            print(ticker)
                            caixa.insert("end", f"{ticker}\n")
                    else:
                        caixa.insert("end", "❌ Nenhum ticker encontrado.\n")
                else:
                    caixa.insert("end", "❌ Coluna 'Ticker' não encontrada no arquivo.\n")
            else:
                caixa.insert("end", "⚠️ Corrija os filtros antes de continuar.\n")

            caixa.insert("end", "✅ Finalizado!\n")
            caixa.configure(state="disabled")



        btn_start = ctk.CTkButton(janela, text="Começar", width=220, height=40, command=lambda:Start_BCKT(caixa))
        btn_start.pack(pady=(0,60))


        #caixa.configure(state="disabled")
        janela.mainloop()






    #--- Filtro
    def BACKT_filtro(self):
        filtro_janela = ctk.CTkToplevel(self)
        filtro_janela.title("Filtros")
        filtro_janela.geometry("460x550")
        filtro_janela.resizable(False, False)
        filtro_janela.grab_set()
        
        # Carrega DFs iniciais
        df_pe = pd.read_csv(BACKT_arquivo_filtro_pe)
        df_in = pd.read_csv(BACKT_arquivo_filtro_in)

        # UI
        ctk.CTkLabel(filtro_janela, text="Selecione os filtros desejados",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        frame_principal = ctk.CTkFrame(filtro_janela)
        frame_principal.pack(pady=10, padx=10)

        frame_periodo = ctk.CTkFrame(frame_principal)
        frame_periodo.grid(row=0, column=0, padx=25, pady=5, sticky="n")

        frame_intervalo = ctk.CTkFrame(frame_principal)
        frame_intervalo.grid(row=0, column=1, padx=25, pady=5, sticky="n")

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
                if "periodo" in df.columns:
                    if (df["periodo"] == chave).any():
                        self.estado_estrategias[chave] = novo_valor
                        btn = self.botoes_filtros.get(chave)
                        if btn:
                            if novo_valor == 1:
                                btn.configure(text="✅", fg_color="green")
                            else:
                                btn.configure(text="➕", fg_color="gray")
                if "intervalo" in df.columns:
                    if (df["intervalo"] == chave).any():
                        self.estado_estrategias[chave] = novo_valor
                        btn = self.botoes_filtros.get(chave)
                        if btn:
                            if novo_valor == 1:
                                btn.configure(text="✅", fg_color="green")
                            else:
                                btn.configure(text="➕", fg_color="gray")
                        
           
                        
            #print("✅ Aplicar_All concluído!")

        # botões All
        btn_aplicar_all_pe = ctk.CTkButton(frame_periodo, text="All", width=20, height=25,
                                        font=ctk.CTkFont(size=7, weight="bold"),
                                        command=lambda pein="pe": aplicar_All(pein))
        btn_aplicar_all_pe.pack(pady=(15, 10))

        btn_aplicar_all_in = ctk.CTkButton(frame_intervalo, text="All", width=20, height=25,
                                        font=ctk.CTkFont(size=7, weight="bold"),
                                        command=lambda pein="in": aplicar_All(pein))
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
        for nome in opcoes_periodo:
            criar_linha(frame_periodo, nome, "pe")
        for nome in opcoes_intervalo:
            criar_linha(frame_intervalo, nome, "in")

        # aplicar final -> grava estado_estrategias nos dois CSVs
        def aplicar():
            #print("Filtros selecionados:")
            # atualiza df_pe e df_in a partir do dicionário de estados
            # pega uma cópia pra garantir leitura atual
            df_pe_local = pd.read_csv(BACKT_arquivo_filtro_pe)
            df_in_local = pd.read_csv(BACKT_arquivo_filtro_in)

            for chave, valor in self.estado_estrategias.items():
                #print(f"{chave}: {'✅' if valor == 1 else '❌'}")
                # tenta atualizar em ambos (um dos dois terá correspondência)
                if "periodo" in df_pe_local.columns:
                    if (df_pe_local["periodo"] == chave).any():
                        df_pe_local.loc[df_pe_local["periodo"] == chave, "periodo_01"] = valor
                if "intervalo" in df_in_local.columns:
                    if (df_in_local["intervalo"] == chave).any():
                        df_in_local.loc[df_in_local["intervalo"] == chave, "intervalo_01"] = valor

            # salva ambos
            df_pe_local.to_csv(BACKT_arquivo_filtro_pe, index=False)
            df_in_local.to_csv(BACKT_arquivo_filtro_in, index=False)

            filtro_janela.destroy()

        btn_aplicar = ctk.CTkButton(filtro_janela, text="Aplicar", width=120, height=55,
                                font=ctk.CTkFont(size=14, weight="bold"),
                                command=aplicar)
        btn_aplicar.pack(pady=(15, 10))


        
        





    # ==== Editar Estrategias ====
    def Editar_estrategias(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="⚙ Editar Estrategias ⚙", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        # Frame para colocar os botões
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=10)
        df = pd.read_csv(Estrategias_arquivo_vaiaveis)

       

        # Dicionário para armazenar estado
        
        if not hasattr(self, "estado_estrategias"):
            self.estado_estrategias = {}
        
        print(self.estado_estrategias)
        with open(Estrategias_arquivo_vaiaveis, "r", encoding="utf-8") as f:
            leitor = csv.reader(f)
            next(leitor)  # pular cabeçalho
            for dados in leitor:
                nome, valor = dados[0], int(dados[1])
                # Salva o estado inicial no dicionário
                self.estado_estrategias[nome] = valor

                linha_frame = ctk.CTkFrame(frame_botoes)
                linha_frame.pack(pady=5)

                btn_principal = ctk.CTkButton(linha_frame, text=nome, width=220, height=40)
                btn_principal.pack(side="left", padx=5)

                if nome == estrategias[0]:
                    btn_principal.configure(command=self.ISNB_Menu)

                # Função toggle corrigida
                def toggle(btn=None, n=nome):
                    # pega o estado atual do dicionário
                    v = self.estado_estrategias[n]
                    v = 1 - v  # inverte
                    self.estado_estrategias[n] = v  # atualiza o estado

                    # muda a cor do botão
                    if v == 1:
                        btn.configure(text="✅", fg_color="green")
                    else:
                        btn.configure(text="➕", fg_color="gray")

                    # atualiza no DataFrame
                    df.loc[df["estrategia"] == n, "estrategia_01"] = v
                    df.to_csv(Estrategias_arquivo_vaiaveis, index=False)
                    print(f"{n} = {v}")

                # Botão lateral
                btn_toggle = ctk.CTkButton(linha_frame, text="➕", width=40, height=40, fg_color="gray")
                btn_toggle.pack(side="left", padx=5)

                # Estado visual inicial
                if valor == 1:
                    btn_toggle.configure(text="✅", fg_color="green")

                # Vincula comando
                btn_toggle.configure(command=lambda b=btn_toggle, n=nome: toggle(b, n))


            # Botão Voltar
            botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby)
            botao_voltar.pack(side="bottom", pady=30)




    # ----- Inside Bar -----
    def ISNB_Menu(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="INSIDE BAR 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        
        
        
            
        botao_voltar = ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby)
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
