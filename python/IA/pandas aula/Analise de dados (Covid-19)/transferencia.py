import pandas as pd

import os

file_path = "D:\Pen Drive\programaçao\Python luan\python\IA\pandas aula\Analise de dados (Covid-19)\covid19.csv"
if os.path.exists(file_path):
    print("Arquivo encontrado.")
    tra = pd.read_csv(file_path)
    tra.to_excel("D:\Pen Drive\programaçao\Python luan\python\IA\pandas aula\Analise de dados (Covid-19)\covid19.xlsx", index=False)
else:
    print("Arquivo não encontrado!")
