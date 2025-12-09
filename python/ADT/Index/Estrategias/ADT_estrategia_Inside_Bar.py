vela_1 = None      # vela mãe
vela_2 = None      # inside bar
ISNB_onoff = False # dentro de um inside bar ativo?


def BCKT_estrategia(resultados):
    global vela_1, vela_2, ISNB_onoff

    for item in resultados:

        # Estrutura da vela atual
        vela_atual = {
            "close": item['close'],
            "open": item['open'],
            "high": item['high'],
            "low": item['low'],
            "vela_cor": item["vela_cor"],
            "forca_vela": item["forca_vela"]
        }

        close_ = vela_atual["close"]
        high_ = vela_atual["high"]
        low_  = vela_atual["low"]
        forca_atual = vela_atual["forca_vela"]
        #print(forca_atual)
        # =====================================================
        # 1) Preencher vela mãe
        # =====================================================
        if vela_1 is None:
            vela_1 = vela_atual
            continue

        # =====================================================
        # 2) Preencher inside bar
        # =====================================================
        if vela_2 is None:
            vela_2 = vela_atual
            continue

        # Agora temos vela_1 e vela_2 → verificar Inside Bar
        high_mae = vela_1["high"]
        low_mae  = vela_1["low"]
        high_in  = vela_2["high"]
        low_in   = vela_2["low"]

        # =====================================================
        # 3) Detectar se vela_2 realmente é Inside Bar
        # =====================================================
        if low_in > low_mae and high_in < high_mae:
            ISNB_onoff = True
        else:
            # NÃO formou inside bar → mover janela de velas
            vela_1 = vela_2
            vela_2 = vela_atual
            ISNB_onoff = False
            continue

        # =====================================================
        # 4) Estamos dentro do Inside Bar → aguardar rompimento
        # =====================================================

        if ISNB_onoff:
            
            # ----------- COMPRA -----------
            if close_ > high_mae:
                #print(f"close: {close_} > Mae: {high_mae}  |  {vela_1["forca_vela"]}  |  {vela_2["forca_vela"]}  |  {forca_atual}")
                if (
                    vela_1["forca_vela"] in ["A+", "A"] and
                    (vela_2["forca_vela"] in ["A+", "A", "B"] or
                    forca_atual in ["A+", "A", "B"])
                ):
                    # Reset após sinal
                    vela_1 = vela_atual
                    vela_2 = None
                    ISNB_onoff = False
                    
                    return "🟢compra"

            # ----------- VENDA -----------
            elif close_ < low_mae:
                #print(f"close: {close_} < Mae: {low_mae}  |  {vela_1["forca_vela"]}  |  {vela_2["forca_vela"]}  |  {forca_atual}")
                if (
                    vela_1["forca_vela"] in ["A+", "A"] and
                    (vela_2["forca_vela"] in ["A+", "A", "B"] or
                    forca_atual in ["A+", "A", "B"])
                ):
                    # Reset após sinal
                    vela_1 = vela_atual
                    vela_2 = None
                    ISNB_onoff = False
                    return "🔴venda"

        # =====================================================
        # Caso não haja rompimento → shift normal
        # =====================================================
        vela_1 = vela_2
        vela_2 = vela_atual

    # Caso não retorne nada
    return None
