import openpyxl

#== Ler arquivo Exel ==#
workbook = openpyxl.load_workbook("vendas_de_produtos.xlsx")#entre as aspas "Coloque o nome ou local do arquivo"
vendas_sheet = workbook["vendas"]#Ler a pagina escolhida
cont = 0
for linha in vendas_sheet.iter_rows(min_row=4):
    cont+=1
    print(f"====Cliente {cont}====")
    print("Cliente:",linha[0].value)
    print("Produto:",linha[1].value)
    print("Quantidade:",linha[2].value)
    print("Categoriaa:",linha[3].value,"\n")