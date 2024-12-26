import pandas as pd

def test(reg,est,cas):
    def casos(est, qnt):
        if cas == 'CA':
            print(f'Em {est} tivemos {qnt} casos',end=" ")
        elif cas == 'OA':
            print(f'e {qnt} mortos!!')
            print()


    cod = df.loc[(df['regiao'] == reg) & (df['estado'] == est )]

    cod = cod.query('CN != 0 & CA != 0 & ON != 0 & OA != 0')

    cod = cod.reset_index(drop=True)

    if not cod.empty:
        valor = cod.iloc[-1][cas]
        casos(est, valor)



df = pd.read_csv("covid19.csv", sep=',')


df['regiao'] = df['regiao'].str.strip()
df['estado'] = df['estado'].str.strip()

esta = df['estado'].unique()
lista_estados= esta.tolist()
regi = df['regiao'].unique()
lista_regiao= regi.tolist()



print("Em um periodo de tempo tivemos:")
print(90 * "=")
for reg in lista_regiao:

    print(f"{reg}:")
    print(90 * "=")
    estados_regiao = df[df['regiao'] == reg]['estado'].unique()

    for est in estados_regiao:
        filtro = df[(df['regiao'] == reg) & (df['estado'] == est)]

        if not filtro.empty:
            test(reg, est, 'CA')
            test(reg, est, 'OA')

        else:
            print()
    print(90*"=")

print(10*"\n")
print("Dias sem casos e obito: ")
print(90 * "=")
for reg in lista_regiao:

    print(f"{reg}:")
    print(90 * "=")
    estados_regiao = df[df['regiao'] == reg]['estado'].unique()

    for est in estados_regiao:
        filtro = df[(df['regiao'] == reg) & (df['estado'] == est) & (df["CA"] == 0) & (df["OA"] == 0)]

        if not filtro.empty:

               # zero(est,"CA")
                print(f"No {est} tivemos {filtro.shape[0] - 1} dias sem caso e sem obito")
        else:
            print()

    print(90*"=")



