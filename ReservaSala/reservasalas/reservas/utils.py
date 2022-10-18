
def verificaConflitoDataReservas(reservas, data_inicio, data_fim):
    """metodo utilizando somente as listas de reservas diretamento do query object
    for reserva in reservas:
        inicio_mais_tardio = max(reserva.inicio, data_inicio)
        fim_mais_antecipado = min(reserva.fim, data_fim)
        if inicio_mais_tardio<=fim_mais_antecipado:
            return True"""
    for i in range(0, len(reservas[0])):
        inicio_mais_tardio = max(reservas[0][i], data_inicio)
        fim_mais_antecipado = min(reservas[1][i], data_fim)
        if inicio_mais_tardio<=fim_mais_antecipado:
            return True
    return False