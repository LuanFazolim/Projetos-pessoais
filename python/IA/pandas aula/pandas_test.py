import pandas as pd
from IPython.display import display


#vendas ={'data':['04/07/2008','06/02/1980'],'valor':[500,300],'produto':['feijao','arroz'],'qtde':[50,70],}

vendas_df = pd.read_excel("Vendas.xlsx")
display(vendas_df)
print(vendas_df)
    