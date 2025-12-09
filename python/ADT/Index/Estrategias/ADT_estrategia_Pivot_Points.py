verificar_True_dia = False
verificar_True_semana = False
verificar_True_mes = False
verificar_True_ano = False

lista_dados = []
tempo_um = None

ticker_ant = None
pp = 0
r1 = 0
s1 = 0

def BCKT_estrategia(resultados):
    global verificar_True_dia, verificar_True_semana
    global verificar_True_mes, verificar_True_ano
    global lista_dados, tempo_um
    global pp, r1, s1,ticker_ant

    for item in resultados:
        periodo = item["periodo"] 
        intervalo = item["intervalo"]
        ticker_atual = item["ticker"]
        if ticker_ant == None:
            ticker_ant = ticker_atual
        high_atual = float(item["high"])
        low_atual = float(item["low"])
        tempo_atual = item["hora"]
        close_atual = float(item["close"])
        atr = float(item["atr"])

    # print(f"{periodo} - {intervalo} - {tempo_atual}")
        if ticker_atual != ticker_ant:
            lista_dados.clear()
            verificar_True_dia = False
            verificar_True_semana = False
            verificar_True_mes = False
            verificar_True_ano = False
            
        if (intervalo == "5min" or intervalo == "15min") and verificar_True_dia == False:
            lista_dados.clear()
            verificar_True_dia = True
            verificar_True_semana = False
            verificar_True_mes = False
            verificar_True_ano = False
            
                
        elif intervalo == "1hr" and verificar_True_semana == False: 
            lista_dados.clear()
            verificar_True_dia = False
            verificar_True_semana = True
            verificar_True_mes = False
            verificar_True_ano = False  
        elif intervalo == "1D" and verificar_True_mes == False:
            lista_dados.clear()
            verificar_True_dia = False
            verificar_True_semana = False
            verificar_True_mes = True
            verificar_True_ano = False
        elif (intervalo == "1sem" or intervalo == "1mes") and verificar_True_ano == False: 
            lista_dados.clear()
            verificar_True_dia = False
            verificar_True_semana = False
            verificar_True_mes = False
            verificar_True_ano = True


        if verificar_True_dia == True:
            if periodo != "1Dia":
                
                if len(lista_dados) != 0:
                    tempo_um = lista_dados[0][0]
                    if tempo_atual.to_pydatetime().date() !=  tempo_um.to_pydatetime().date():
                        
                        high_pp = max([item[1] for item in lista_dados])
                        low_pp = min([item[2] for item in lista_dados])
                        close_pp = lista_dados[-1][3]
                        pp = (high_pp + low_pp + close_pp) / 3
                        r1 = (2 * pp) - low_pp
                        s1 = (2 * pp) - high_pp
                        '''r2 = pp + (high_pp - low_pp)
                        s2 = pp - (high_pp - low_pp)
                        r3 = high_pp + 2 * (pp - low_pp)
                        s3 = low_pp - 2 * (high_pp - pp)'''
                        
                        

                        lista_dados.clear()

                    
                lista_dados.append([tempo_atual,high_atual,low_atual,close_atual])
        elif verificar_True_semana == True:
            if periodo != "1Dia" and periodo != "1Semana":
                if len(lista_dados) != 0:
                    tempo_um = lista_dados[0][0]
                    #print(f"{tempo_atual.to_pydatetime().date()} - {tempo_um.to_pydatetime().date()}   = { (tempo_atual.to_pydatetime().date() - tempo_um.to_pydatetime().date()).days }")
                    if abs(tempo_atual.to_pydatetime().date() - tempo_um.to_pydatetime().date()).days >= 7:
                        
                        
                        high_pp = max([item[1] for item in lista_dados])
                        low_pp = min([item[2] for item in lista_dados])
                        close_pp = lista_dados[-1][3]
                        pp = (high_pp + low_pp + close_pp) / 3
                        r1 = (2 * pp) - low_pp
                        s1 = (2 * pp) - high_pp
                        '''r2 = pp + (high_pp - low_pp)
                        s2 = pp - (high_pp - low_pp)
                        r3 = high_pp + 2 * (pp - low_pp)
                        s3 = low_pp - 2 * (high_pp - pp)'''
                        
                        

                        lista_dados.clear()

                    
                lista_dados.append([tempo_atual,high_atual,low_atual,close_atual])
        elif verificar_True_mes == True:
            if periodo != "1Dia" and periodo != "1Semana" and periodo != "1Mes":
            
                if len(lista_dados) != 0:
                    tempo_um = lista_dados[0][0]
                    tempo_atual_date = tempo_atual.to_pydatetime().date()
                    tempo_um_date = tempo_um.to_pydatetime().date()
                    meses = (tempo_atual_date.year - tempo_um_date.year) * 12 + (tempo_atual_date.month - tempo_um_date.month)
                    
                    if abs(meses)>= 1:
                        
                        high_pp = max([item[1] for item in lista_dados])
                        low_pp = min([item[2] for item in lista_dados])
                        close_pp = lista_dados[-1][3]
                        pp = (high_pp + low_pp + close_pp) / 3
                        r1 = (2 * pp) - low_pp
                        s1 = (2 * pp) - high_pp
                        '''r2 = pp + (high_pp - low_pp)
                        s2 = pp - (high_pp - low_pp)
                        r3 = high_pp + 2 * (pp - low_pp)
                        s3 = low_pp - 2 * (high_pp - pp)'''
                        
                        

                        lista_dados.clear()

                
                lista_dados.append([tempo_atual,high_atual,low_atual,close_atual])  
        elif verificar_True_ano == True:
            if periodo != "1Dia" and periodo != "1Semana" and periodo != "1Mes":
            
                if len(lista_dados) != 0:
                    tempo_um = lista_dados[0][0]
                    tempo_atual_date = tempo_atual.to_pydatetime().date()
                    tempo_um_date = tempo_um.to_pydatetime().date()
                    anos = tempo_atual_date.year - tempo_um_date.year
                    
                    if abs(anos)>= 1:
                        #print(f"{tempo_atual.to_pydatetime().date()} - {tempo_um.to_pydatetime().date()} = {anos}")
                        
                        
                        high_pp = max([item[1] for item in lista_dados])
                        low_pp = min([item[2] for item in lista_dados])
                        close_pp = lista_dados[-1][3]
                        pp = (high_pp + low_pp + close_pp) / 3
                        r1 = (2 * pp) - low_pp
                        s1 = (2 * pp) - high_pp
                        '''r2 = pp + (high_pp - low_pp)
                        s2 = pp - (high_pp - low_pp)
                        r3 = high_pp + 2 * (pp - low_pp)
                        s3 = low_pp - 2 * (high_pp - pp)'''
                        
                        

                        lista_dados.clear()

                
                lista_dados.append([tempo_atual,high_atual,low_atual,close_atual])  




    ticker_ant = ticker_atual        
    buffer = atr*0.1  # 0,2%
    if close_atual > r1 + buffer:
        return "🟢compra"
    elif close_atual < s1 - buffer:
        return "🔴venda"
    
