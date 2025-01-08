import MetaTrader5 as mt5
from datetime import datetime, timedelta
import time
import numpy as np

# Inicialize a conexão com o MetaTrader 5
if not mt5.initialize():
    with open("trading_log.txt", "a") as log_file:
        log_file.write("Erro ao inicializar MetaTrader 5\n")
    mt5.shutdown()

# Lista de ativos com parâmetros definidos
ativos = [
    {"ativo": "GBPUSD", "volume": 0.01, "tipo_ordem": "venda", "horario_abrir": "05:30", "horario_fechar": "10:00"},
    # ... (resto dos ativos)
]

# Função para registrar eventos no arquivo de log
def registrar_log(mensagem):
    with open("trading_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {mensagem}\n")

# Função para obter dados históricos de preços
def get_historical_data(symbol, start_time, end_time, timeframe=mt5.TIMEFRAME_H1):
    rates = mt5.copy_rates_range(symbol, timeframe, start_time, end_time)
    if rates is None or len(rates) == 0:
        registrar_log(f"Erro ao obter dados históricos para {symbol}")
        return None
    return [rate['close'] for rate in rates]

# Função para calcular a volatilidade (desvio padrão) dos preços históricos
def calcular_volatilidade(precos):
    return np.std(precos)

# Função para enviar a ordem
def enviar_ordem(ativo, volume, tipo_ordem):
    symbol = ativo
    tick_info = mt5.symbol_info_tick(symbol)
    
    if tick_info is None:
        registrar_log(f"Erro: Não foi possível obter o preço para {symbol}")
        return

    price = tick_info.ask
    order_type = mt5.ORDER_TYPE_BUY if tipo_ordem == "compra" else mt5.ORDER_TYPE_SELL
    deviation = 10
    stop_loss = 0.0
    take_profit = 0.0
    
    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "price": price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "type": order_type,
        "type_filling": mt5.ORDER_FILLING_IOC,
        "type_time": mt5.ORDER_TIME_GTC,
        "comment": "Automated trading"
    }
    
    result = mt5.order_send(order_request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        registrar_log(f"Erro ao enviar ordem para {symbol}: Retcode {result.retcode}, Detalhes: {result.comment}")
    else:
        registrar_log(f"Ordem de {tipo_ordem} para {symbol} enviada com sucesso! Ticket: {result.order}")
        return result.order

# Função para fechar a ordem
def fechar_ordem(symbol, order_ticket):
    positions = mt5.positions_get(symbol=symbol)
    if positions is not None:
        for position in positions:
            if position.ticket == order_ticket:
                close_request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": position.volume,
                    "type": mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                    "position": position.ticket,
                    "price": mt5.symbol_info_tick(symbol).bid,
                    "deviation": 10,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                    "type_time": mt5.ORDER_TIME_GTC,
                    "comment": "Fechamento automatizado"
                }
                result = mt5.order_send(close_request)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    registrar_log(f"Ordem de {symbol} fechada com sucesso! Ticket: {order_ticket}")
                else:
                    registrar_log(f"Erro ao fechar ordem de {symbol}: Retcode {result.retcode}, Detalhes: {result.comment}")
                return

# Função principal que verifica os horários e envia as ordens com base em análises
def executar_trades():
    ordens_abertas = {}
    while True:
        hora_atual = datetime.now().strftime("%H:%M")
        for ativo in ativos:
            horario_abrir = datetime.strptime(ativo["horario_abrir"], "%H:%M").time()
            horario_fechar = datetime.strptime(ativo["horario_fechar"], "%H:%M").time()

            if hora_atual == horario_abrir.strftime("%H:%M"):
                start_time = datetime.now() - timedelta(days=1)
                end_time = datetime.now()
                precos = get_historical_data(ativo["ativo"], start_time, end_time)

                if precos:
                    volatilidade = calcular_volatilidade(precos)
                    registrar_log(f"Volatilidade de {ativo['ativo']} para {hora_atual}: {volatilidade}")

                    if volatilidade < 0.01:
                        registrar_log(f"Condições favoráveis para {ativo['tipo_ordem']} de {ativo['ativo']}")
                        order_ticket = enviar_ordem(ativo['ativo'], ativo['volume'], ativo['tipo_ordem'])
                        if order_ticket:
                            ordens_abertas[ativo['ativo']] = order_ticket
                    else:
                        registrar_log(f"Volatilidade alta para {ativo['ativo']}, não abrindo ordem.")
            
            elif hora_atual == horario_fechar.strftime("%H:%M"):
                registrar_log(f"Fechando ordem para {ativo['ativo']} às {hora_atual}")
                if ativo['ativo'] in ordens_abertas:
                    fechar_ordem(ativo['ativo'], ordens_abertas[ativo['ativo']])
                    del ordens_abertas[ativo['ativo']]
        time.sleep(60)

# Iniciar a execução
executar_trades()
