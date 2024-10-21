class Calcular_CET:
    # Função para cálculo do IOF
    def calcular_iof(self, saldo_devedor, prazo):
        iof_fixo = saldo_devedor * 0.0038  # IOF fixo de 0,38%
        iof_diario = saldo_devedor * 0.000082 * prazo  # IOF diário de 0,0082% por dia
        iof_total = iof_fixo + iof_diario
        return iof_total / saldo_devedor

    # Função para cálculo no sistema Price
    def calcular_price(self, saldo_devedor, taxa_juros, prazo, iof):
        taxa_juros = taxa_juros  # Convertendo a taxa para decimal
        saldo_devedor_ajustado = saldo_devedor + iof  # Ajustando pelo IOF
        pmt = (saldo_devedor_ajustado * taxa_juros) / (1 - (1 + taxa_juros) ** -prazo)
        return pmt

    # Função para cálculo no sistema SAC
    def calcular_sac(self, saldo_devedor, taxa_juros, prazo, iof):
        amortizacao = (saldo_devedor + iof) / prazo  # Amortização constante ajustada pelo IOF
        parcelas = []
        saldo_atual = saldo_devedor + iof
        
        for t in range(1, prazo + 1):
            juros = saldo_atual * (taxa_juros)  # Cálculo do juros para o período
            parcela = amortizacao + juros
            saldo_atual -= amortizacao
            parcelas.append(parcela)
        
        return parcelas[0]

    # Função para calcular o CET (Custo Efetivo Total)
    def calcular_CET(self, taxa_juros, prazo, iof):
        # CET deve considerar a taxa de juros efetiva, o prazo e os custos adicionais
        taxa_juros = taxa_juros  # Convertendo para decimal
        custo_total = (1 + taxa_juros) ** prazo  # Juros compostos ao longo do prazo
        custo_adicional = iof  # Convertendo IOF para decimal
        cet = custo_total * (1 + custo_adicional)
        return cet
