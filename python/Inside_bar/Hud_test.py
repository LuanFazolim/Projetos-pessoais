import customtkinter as ctk
from tkinter import messagebox

from binance.client import Client
import yfinance as yf


import os
import time
import pandas as pd

#Lobby_
ISDB_arquivo_dados = r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\Inside_bar_dados.csv"
ISDB_arquivo_tickers = r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\Inside_bar_tikers.csv"
ISDB_arquivo_pack_tickers =r'D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\Inside_bar_pack_tikers.csv'
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
        color_tema = "#360fe2"
        # ======= Configurações da janela =======
        self.title("Automatic dry Trading (ADT)")
        self.geometry("420x760") # Tela cheia
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))  # Pressione ESC para sair da tela cheia
        self.resizable(True, True)
        #ctk.set_appearance_mode("dark")
        #ctk.set_default_color_theme("blue")
        ctk.set_default_color_theme(r"D:\programacao\Python\Bot_iq_option\Manual\Inside_bar\tema.json")



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
        btn_start = ctk.CTkButton(self, text="Começar", width=220, height=40, command=self.start_simulation)
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
    def start_simulation(self):
        #self.limpar_tela()
        messagebox.showinfo("ℹ️ Sobre", "Aplicativo de Lobby feito em Python 🐍\nPor: Luan Fazolim")

    # ==== Editar Estrategias ====
    def Editar_estrategias(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="⚙ Editar Estrategias ⚙", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        # Frame para colocar os botões
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=10)

        # Lista de estratégias
        estrategias = ["Inside Bar", "Martelo", "Outro"]

        # Dicionário para armazenar estado
        self.estado_estrategias = {nome: 0 for nome in estrategias}

        for nome in estrategias:
            # Frame individual para cada linha
            linha_frame = ctk.CTkFrame(frame_botoes)
            linha_frame.pack(pady=5)

            # Botão principal (não precisa alternar)
            btn_principal = ctk.CTkButton(linha_frame, text=nome, width=220, height=40)
            btn_principal.pack(side="left", padx=5)
            if nome == estrategias[0]:
                btn_principal.configure(command = self.ISNB_Menu )

            # Botão lateral que vai alternar 0/1
            def toggle(btn= None, n=nome):
                self.estado_estrategias[n] = 1 - self.estado_estrategias[n]
                if self.estado_estrategias[n] == 1:
                    btn.configure(text="✅", fg_color="green")
                else:
                    btn.configure(text="➕", fg_color="gray")
                print(f"{n} = {self.estado_estrategias[n]}")

            btn_toggle = ctk.CTkButton(linha_frame, text="➕", width=40, height=40, fg_color="gray")
            btn_toggle.pack(side="left", padx=5)
            btn_toggle.configure(command=lambda b=btn_toggle, n=nome: toggle(b, n))

        # Botão Voltar
        ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby).pack(pady=(50,0))


    # ----- Inside Bar -----
    def ISNB_Menu(self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="INSIDE BAR 🖊", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)

        
        
        
            
        ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.Editar_estrategias).pack(pady=(50,0))
       
        
            
        
    # ==== Tickers ====
    def TKRS_Menu (self):
        self.limpar_tela()

        titulo = ctk.CTkLabel(self, text="Tickers 📚", font=ctk.CTkFont(size=22, weight="bold"))
        titulo.pack(pady=20)
        
        ctk.CTkButton(self, text="➕ Adicionar Tickers", width=220, height=40, command=self.TKRS_Add_tiker).pack(pady=10)
        ctk.CTkButton(self, text="📦 Adicionar Pacote de Tickers", width=220, height=40, command=self.TKRS_Add_pack_ticker).pack(pady=10)
        ctk.CTkButton(self, text="📋 Visualizar Tickers", width=220, height=40, command=self.TKRS_Vizuaizar_tiker).pack(pady=10)
        if len(pd.read_csv(ISDB_arquivo_tickers)) > 0:
            ctk.CTkButton(self, text="❌ Excluir Tickers", width=220, height=40, command=self.TKRS_Excluir_tiker).pack(pady=10)
        ctk.CTkButton(self, text="⬅️ Voltar", width=220, height=40, command=self.criar_lobby).pack(pady=(50,0))
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
            ISDB_df = pd.read_csv(ISDB_arquivo_tickers)
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
            ISDB_df = pd.read_csv(ISDB_arquivo_tickers)
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
            ISDB_df.to_csv(ISDB_arquivo_tickers, index=False)
            messagebox.showinfo("✅ Sucesso", "Ticker adicionado com sucesso!")
            janela.destroy()
            self.TKRS_Menu()

        nome_entry.bind("<KeyRelease>", verificar_dowload)
        ctk.CTkButton(janela, text="Salvar", width=120, height=35, command=salvar).pack(pady=20)
        janela.bind('<Return>', salvar)

          



    #--- Add Pack Ticker
    def TKRS_Add_pack_ticker(self):
        ISDB_pack = pd.read_csv(ISDB_arquivo_pack_tickers)

        if ISDB_pack.empty:
            messagebox.showinfo("ℹ️ ", "📭 Nenhum Ticker encontrado.")
            return

        ISDB_tickers = pd.read_csv(ISDB_arquivo_tickers)
        existentes = set(ISDB_tickers["Ticker"].values)
    
        cont_repetidos = 0

        for dado in ISDB_pack["Ticker"].values:
            if dado in existentes:
                cont_repetidos += 1
            else:
                nova_linha = pd.DataFrame({'Ticker': [dado]})
                ISDB_tickers = pd.concat([ISDB_tickers, nova_linha], ignore_index=True)

        ISDB_tickers.to_csv(ISDB_arquivo_tickers, index=False)

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
        ISDB_df = pd.read_csv(ISDB_arquivo_tickers)

        if len(pd.read_csv(ISDB_arquivo_tickers)) <=0:
            ctk.CTkLabel(janela, text="📭 Nenhum Ticker encontrado.", font=ctk.CTkFont(size=14)).pack(pady=40)
            return

        caixa = ctk.CTkTextbox(janela, width=360, height=230, font=ctk.CTkFont(size=14))
        caixa.pack(pady=15)

        for i, dado in enumerate(ISDB_df["Ticker"].values, 1):

            caixa.insert("end", f"{i} - {dado}\n")

        caixa.configure(state="disabled")

    # --- Excluir Ticker
    def TKRS_Excluir_tiker(self):
            os.remove(ISDB_arquivo_tickers)
            ISDB_df = pd.DataFrame(columns=['Ticker'])
            ISDB_df.to_csv(ISDB_arquivo_tickers, index=False)
            self.TKRS_Menu()

            
            messagebox.showinfo("ℹ️ ", "EXCLUIR TICKER")

    
    

# ======= EXECUÇÃO =======
if __name__ == "__main__":
    app = LobbyApp()
    app.mainloop()
