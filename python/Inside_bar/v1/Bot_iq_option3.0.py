# Iniciando a modificação do código conforme solicitado
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import pandas as pd
import os
import threading
from sklearn.ensemble import RandomForestClassifier
import joblib
from colorama import init, Fore
import csv
from datetime import datetime
import pyautogui
import pyperclip


init(autoreset=True)

# === CONFIGURAÇÕES ===
email = "Luanfazolim@gmail.com"
senha = "Luna@0419"
ml_pronto = False  # ou True, se quiser que comece como carregado


cont_acertos = 0
cont_trades = 0
paridades = ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC"]
timeframe = 5
periodo = 14
valor_base = 5.0
valor_min = 1.0
valor_max = 5.0
csv_file = 'historico_dados.csv'
modelo_file = 'modelo_ml.pkl'
min_amostras_treino = 30
csv_operacoes_file = 'historico_operacoes.csv'
FEATURE_COLS = ['rsi', 'k', 'd', 'ema', 'macd', 'signal','boll_upper', 'boll_lower']
horarios_bons = list(range(24))

def horario_valido():
    return datetime.now().hour in horarios_bons

def inicializar_csv_operacoes(filename=csv_operacoes_file):
    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['moeda', 'data', 'hora', 'resultado', 'candles', 'dinheiro_entrada', 'lucro', 'total_acumulado', 'dinheiro_total'])
lock = threading.Lock()

def registrar_operacao(moeda, resultado, candles, dinheiro_entrada, lucro, filename=csv_operacoes_file):
    now = datetime.now()
    data = now.strftime('%Y-%m-%d')
    hora = now.strftime('%H:%M:%S')
    total_acumulado = 0.0
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            linhas = list(csv.DictReader(f))
            if linhas:
                try:
                    total_acumulado = float(linhas[-1]['total_acumulado'])
                except:
                    total_acumulado = 0.0
    total_acumulado += lucro
    dinheiro_total = API.get_balance()

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([moeda, data, hora, resultado, candles, dinheiro_entrada, lucro, total_acumulado, dinheiro_total])

API = IQ_Option(email, senha)
API.connect()
API.change_balance("PRACTICE")

if not API.check_connect():
    print(Fore.RED + "Erro ao conectar à IQ Option.")
    exit()
print(Fore.GREEN + "Conectado com sucesso!")

inicializar_csv_operacoes()

# Cálculos matemáticos
def calcular_rsi(fechamentos, periodo=14):
    delta = np.diff(fechamentos)
    ganhos = np.where(delta > 0, delta, 0)
    perdas = np.where(delta < 0, -delta, 0)
    media_ganho = np.mean(ganhos[:periodo])
    media_perda = np.mean(perdas[:periodo])
    rsi_lista = []
    for i in range(periodo, len(fechamentos)-1):
        ganho = ganhos[i]
        perda = perdas[i]
        media_ganho = (media_ganho * (periodo - 1) + ganho) / periodo
        media_perda = (media_perda * (periodo - 1) + perda) / periodo
        rsi_lista.append(100 if media_perda == 0 else 100 - (100 / (1 + media_ganho / media_perda)))
    return rsi_lista[-1] if rsi_lista else 50

def calcular_ema(fechamentos, periodo=14):
    return np.mean(fechamentos[-periodo:])

def calcular_macd(fechamentos):
    ema12 = np.mean(fechamentos[-12:])
    ema26 = np.mean(fechamentos[-26:])
    macd = ema12 - ema26
    signal = np.mean(fechamentos[-9:])
    return macd, signal

def calcular_bollinger_bands(fechamentos, periodo=20, desvio=2):
    if len(fechamentos) < periodo:
        return None, None, None
    media = np.mean(fechamentos[-periodo:])
    std = np.std(fechamentos[-periodo:])
    upper = media + desvio * std
    lower = media - desvio * std
    return upper, media, lower

def obter_candles(par, timeframe, quantidade):
    for _ in range(5):
        if not API.check_connect():
            API.connect()
            API.change_balance("PRACTICE")
        try:
            candles = API.get_candles(par, timeframe * 60, quantidade, time.time())
            if candles and len(candles) == quantidade:
                return candles
        except:
            time.sleep(2)
    return None

def extrair_features(candles):
    closes = np.array([x['close'] for x in candles])
    highs = np.array([x['max'] for x in candles])
    lows = np.array([x['min'] for x in candles])

    rsi = calcular_rsi(closes, periodo)
    k = calcular_rsi(highs, periodo)
    d = calcular_rsi(lows, periodo)
    ema = calcular_ema(closes)
    macd, signal = calcular_macd(closes)
    upper, middle, lower = calcular_bollinger_bands(closes)

    return [rsi, k, d, ema, macd, signal, upper, lower], closes[-1], candles[-1]['from']

def obter_rotulos_para_ml():
    if not os.path.exists(csv_operacoes_file):
        return pd.DataFrame()
    df_op = pd.read_csv(csv_operacoes_file)
    df_op = df_op[['moeda', 'data', 'hora', 'resultado']]
    df_op['timestamp'] = pd.to_datetime(df_op['data'] + ' ' + df_op['hora'])
    return df_op

# Implementando o Machine Learning
def treinar_modelo():
    global ml_modelo, ml_pronto
    while True:
        time.sleep(10)
        with lock:
            try:
                df = pd.read_csv(csv_file)
                df_train = df[df['sinal'].isin(['call', 'put'])]
                if len(df_train) < min_amostras_treino:
                    ml_pronto = False
                    continue
                X = df_train[FEATURE_COLS]
                y = df_train['sinal'].map({'call': 1, 'put': 0})
                modelo = RandomForestClassifier(n_estimators=100, random_state=42)
                modelo.fit(X, y)
                joblib.dump(modelo, modelo_file)
                ml_modelo = modelo
                ml_pronto = True
                print(Fore.GREEN + f"Modelo IA treinado com {len(df_train)} amostras.")
            except Exception as e:
                print(Fore.RED + f"[ERRO ML] {e}")

# Funções financeiras
def calcular_valor_operacao(precisao):
    valor = (precisao * valor_base) / 80
    return round(min(max(valor, valor_min), valor_max), 2)

def calcular_precisao():
    return (cont_acertos / cont_trades) * 100 if cont_trades > 0 else 0

def entrar_operacao(par, direcao, valor):
    try:
        status, id_op = API.buy(valor, par, direcao, timeframe)
        return status, id_op if status else (False, None)
    except:
        return False, None

# Estratégia de Stop Loss e DQL
def stop_loss():
    saldo = API.get_balance()
    if saldo < valor_base * 0.1:  # Exemplo de stop loss com 10% de saldo
        print(Fore.RED + "Stop Loss atingido. Pausando operações.")
        return True
    return False

def aplicar_dql(precisao):
    valor = (precisao * valor_base) / 80
    return round(min(max(valor, valor_min), valor_max), 2)

# Thread de treinamento do modelo
threading.Thread(target=treinar_modelo, daemon=True).start()

print("Inicializando base com candles...")
# Ajuste inicial de dados
dados = []
for par in paridades:
    candles = obter_candles(par, timeframe, 100)
    if candles:
        for i in range(periodo, len(candles)):
            feat, _, ts = extrair_features(candles[:i+1])
            dados.append({
                'par': par, 'timestamp': datetime.fromtimestamp(ts),
                'rsi': feat[0], 'k': feat[1], 'd': feat[2],
                'ema': feat[3], 'macd': feat[4], 'signal': feat[5], 
                'boll_upper': feat[6], 'boll_lower': feat[7], 'sinal': 'none'
            })

df = pd.DataFrame(dados)
df.to_csv(csv_file, index=False)

# Parte de Monitoramento e Envio via WhatsApp
sinais_enviados = {}
contador_ciclo = 0
valor_total = 0.0

def escrever(texto):
    pyperclip.copy(texto)
    pyautogui.hotkey('ctrl', 'v')


# ----====== MAIN ======----
cmW = 0
try:
    cmW = int(input("""\n\n
    [0] Sem WhatsApp
    [1] Com WhatsApp
      -->  """))
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + f"==== MONITORANDO - {datetime.now().strftime('%H:%M:%S')} ====")
        saldo_conta = API.get_balance()
        print(Fore.YELLOW + f"Saldo da Conta: R$ {saldo_conta:.2f}")
        print(Fore.MAGENTA + f"ML: {'SIM' if ml_pronto else 'NÃO'} | Ciclo: {contador_ciclo} | Precisão: {calcular_precisao():.2f}%\n")

        if stop_loss():
            break

        for par in paridades:
            candles = obter_candles(par, timeframe, 30)
            if not candles:
                continue

            features, preco_atual, timestamp = extrair_features(candles)

            rsi = features[0]
            boll_upper = features[6]
            boll_lower = features[7]

            sinal = 'none'

            # Estratégia combinada: Bollinger + RSI
            if preco_atual < boll_lower and rsi < 20:
                sinal = 'call'
            elif preco_atual > boll_upper and rsi > 80:
                sinal = 'put'

            if sinal != 'none' and timestamp not in sinais_enviados:
                valor = 0.0
                usar_ia = False
                precisao = calcular_precisao()

                if ml_pronto and precisao >= 55:
                    try:
                        Xp = pd.DataFrame([features], columns=FEATURE_COLS)
                        pred = ml_modelo.predict(Xp)[0]
                        ia_sinal = 'call' if pred == 1 else 'put'
                        usar_ia = True
                        if ia_sinal != sinal:
                            continue
                    except Exception as e:
                        print(Fore.RED + f"[ERRO IA] {e}")
                        continue


                valor = aplicar_dql(precisao)
                sucesso, id_op = entrar_operacao(par, sinal, valor)
                if sucesso:
                    sinais_enviados[timestamp] = True
                    cont_trades += 1
                    print(Fore.GREEN + f"Operação: {par} | {sinal.upper()} | Valor: R${valor:.2f}")
                    time.sleep(timeframe * 60 + 5)
                    lucro = API.check_win_v3(id_op)
                    valor_total += lucro
                    if lucro > 0: cont_acertos += 1
                    registrar_operacao(par, 'acerto' if lucro > 0 else 'erro', len(candles), valor, lucro)
                    print(Fore.BLUE + f"Resultado: {'✅' if lucro > 0 else '❌'} | Lucro: R${lucro:.2f}")
                    print(Fore.YELLOW + f"Valor Total Acumulado Bot: R${valor_total:.2f}")
                    if cmW == 1:
                        escrever("----= IQ Option Bot 🤖 3.0 =----")
                        pyautogui.hotkey("shift", "enter"); pyautogui.hotkey("shift", "enter")
                        escrever(f"Par: {par}")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Direção: {sinal.upper()}")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Resultado: {'🟢' if lucro > 0 else '🔴' if lucro < 0 else '🟡'}")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Lucro: R${lucro:.2f}")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Acertos: {cont_acertos}/{cont_trades} ({calcular_precisao():.2f}%)")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Lucro total: R${valor_total:.2f}")
                        pyautogui.hotkey("shift", "enter")
                        escrever(f"- Saldo Conta: R${API.get_balance():.2f}")
                        time.sleep(2)
                        pyautogui.press("enter")

            macd, signal_line = features[4], features[5]
            print(Fore.WHITE + f"{par:<15} | RSI: {rsi:.1f} | MACD: {'↑' if macd > signal_line else '↓'} | Direção: {sinal.upper():<5}")

        contador_ciclo += 1
        time.sleep(5)

except KeyboardInterrupt:
    print(Fore.RED + "\nEncerrando bot...")
