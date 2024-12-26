

import pandas as pd

df = pd.read_csv("tabela.csv")
media = 0
print(df)
print(10*"\n")
for num in df["idade"]:

    media+=num


print(f"{media/df.shape[0]}")

