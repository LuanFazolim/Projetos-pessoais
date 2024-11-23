import pyautogui
import time
from datetime import datetime
import keyboard

pyautogui.press("f11")

lobby = "0"

def contagem_regressiva(data_alvo):
    # Converte a data alvo para um objeto datetime
    data_alvo = datetime.strptime(data_alvo, "%d/%m/%Y %H:%M:%S")

    while not keyboard.is_pressed("enter"):
        # Obtém a data e hora atuais
        data_atual = datetime.now()
        # Calcula a diferença entre as datas
        diferenca = data_alvo - data_atual
        # Extrai os dias, horas, minutos e segundos da diferença
        dias_restantes = diferenca.days
        horas_restantes, resto = divmod(diferenca.seconds, 3600)
        minutos_restantes, segundos_restantes = divmod(resto, 60)

        # Limpa a saída anterior e imprime a nova contagem regressiva
        print(
            f"\rFaltam {dias_restantes} dias, {horas_restantes} horas, {minutos_restantes} minutos e {segundos_restantes} segundos para 18/{data_alvo.month}/{data_alvo.year}.",
            end=""
        )

        # Pausa o loop por um segundo
        time.sleep(1)

while True:
    # Lobby
    if lobby == "0":
        print("\n" * 100)
        print("==" * 100)
        print("""
[1] Magica...
[2] Nosso Niver!!!
[3] sair X
    """)
        print("==" * 100)
        print()
        lobby = input(("Digite o numero que vc deseja executar -->:   "))
        print("\n" * 100)
        if lobby not in ["1", "2", "3"]:
            lobby = "0"

    elif lobby == "1":
        time.sleep(0.5)
        print("TIRE A MÃO DO TECLADO E DO MOUSE E DEIXE A MAGICA ACONTECER!!!")
        time.sleep(4)
        print("Aguarde um instante", end="")
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print()

        pyautogui.PAUSE = 0.5
        time.sleep(1)
        pyautogui.press("win")

        pyautogui.write("microsoft edge")
        pyautogui.press("enter")
        pyautogui.write("https://luanfazolim.github.io/Amor/")
        pyautogui.press("enter")
        lobby = "0"

    elif lobby == "2":
        print("Segure a tecla ENTER para voltar!!!")
        time.sleep(1)

        while not keyboard.is_pressed("enter"):
            now = datetime.now()
            if now.day > 17:
                target_month = now.month + 1 if now.month < 12 else 1
                target_year = now.year + 1 if target_month == 1 else now.year
            else:
                target_month = now.month
                target_year = now.year

            if now.day == 18:
                ano_niver = now.year - 2024
                mes_niver = (now.year - 2024) * 12 + now.month - 7
                if ano_niver > 0:
                    print(f"""
HOJE É NOSSO DIA MEU AMOR!!!
Parabéns minha vida, hoje completamos {ano_niver} anos e {mes_niver} meses!!!
Eu te amo muito muito muito!!! <3
                    """)
                else:
                    print(f"""
HOJE É NOSSO DIA MEU AMOR!!!
Parabéns minha vida, hoje completamos {mes_niver} meses!!!
Eu te amo muito muito muito!!! <3
                    """)

            data_alvo = f"18/{target_month}/{target_year} 00:00:00"
            contagem_regressiva(data_alvo)

        lobby = "0"

    # Sair
    elif lobby == "3":
        print("Thau meu Amor!! Eu Te Amo <3")
        break
