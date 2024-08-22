import os
import openpyxl

arquivo = openpyxl.load_workbook("Produtos.xlsx")
#print(arquivo.sheetnames)
pagina = arquivo.active



#.row == linha  --  .column == coluna


for linhaC in pagina["C"]:
    if linhaC.value == "Serviço":
        print(linhaC.value)
        linhaC_row = linhaC.row
        print(linhaC_row)
        pagina[f"D{linhaC_row}"] = 100.5


arquivo.save("Produtos.xlsx")

os.startfile("Produtos.xlsx")