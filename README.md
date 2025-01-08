### Bot de Trading Automatizado para MetaTrader 5 em Python (2025)

Este projeto é um **bot de trading automatizado** desenvolvido em Python para operar no mercado financeiro através da plataforma **MetaTrader 5 (MT5)**. O bot foi projetado para monitorar múltiplos ativos simultaneamente, realizar análises de volatilidade e executar ordens de compra ou venda de forma automática, com base em parâmetros configurados. 

Ele é ideal para traders que desejam automatizar estratégias e economizar tempo, utilizando uma solução robusta e flexível para operar em mercados como Forex, índices, commodities, criptomoedas e outros.

---

### Funcionalidades do Bot

1. **Execução Automática de Ordens**  
   - Suporte a múltiplos ativos simultaneamente com diferentes horários de abertura e fechamento.  
   - Envio de ordens de compra ou venda com base em análises automatizadas e condições de mercado.  
   - Fechamento automático das posições no horário configurado.  

2. **Análise de Volatilidade**  
   - Obtenção de dados históricos de preços via API do MT5.  
   - Cálculo do desvio padrão para determinar a volatilidade do ativo.  
   - Implementação de filtros para evitar operações em momentos de alta volatilidade.  

3. **Registro em Arquivo de Texto**  
   - Registra automaticamente o resultado de cada operação (sucesso ou erro).  
   - Relatórios detalhados sobre ordens abertas, fechadas e condições de mercado.  

4. **Gestão de Riscos**  
   - Configuração de volumes personalizados por ativo.  
   - Controle de execução com desvio configurável.  

5. **Configurações Personalizáveis**  
   - Lista de ativos, volume, horários de operação e tipo de ordem definidos diretamente no código.  
   - Suporte para criar e ajustar estratégias específicas de acordo com as necessidades do trader.  

---

### Estrutura do Código

O código é dividido em várias funções para garantir modularidade e fácil manutenção:

1. **Inicialização e Configuração**  
   - Conexão inicial com o MT5.  
   - Definição dos ativos a serem monitorados, incluindo parâmetros como volume, tipo de ordem, horário de abertura e fechamento.  

2. **Funções de Negociação**  
   - **`get_historical_data()`**: Obtém dados históricos de preços para análise.  
   - **`calcular_volatilidade()`**: Calcula o desvio padrão para determinar a volatilidade.  
   - **`enviar_ordem()`**: Envia ordens de compra ou venda para a plataforma.  
   - **`fechar_ordem()`**: Fecha ordens abertas no horário configurado ou com base em outras condições.  

3. **Execução Contínua**  
   - Loop principal que verifica continuamente os horários de cada ativo.  
   - Integração de lógica para abrir ou fechar posições automaticamente.  

---

### Configuração dos Ativos

A lista de ativos é configurada diretamente no código. Cada ativo possui os seguintes parâmetros:

- **Ativo**: Símbolo do ativo a ser negociado (ex.: "EURUSD", "XAUUSD").  
- **Volume**: Quantidade do lote a ser negociado.  
- **Tipo de Ordem**: Compra ("compra") ou venda ("venda").  
- **Horário de Abertura**: Hora para enviar a ordem.  
- **Horário de Fechamento**: Hora para fechar a posição.  

Exemplo de configuração de ativo:  

```python
ativos = [
    {"ativo": "EURUSD", "volume": 0.01, "tipo_ordem": "compra", "horario_abrir": "05:00", "horario_fechar": "10:00"},
    {"ativo": "XAUUSD", "volume": 0.01, "tipo_ordem": "venda", "horario_abrir": "16:00", "horario_fechar": "19:00"}
]
```

---

### Dependências

- **Python 3.8 ou superior**  
- **MetaTrader 5 Python API**: Biblioteca oficial para integração com o MT5.  
- **NumPy**: Utilizado para cálculos matemáticos e estatísticos.  

Instale as dependências com o seguinte comando:  

```bash
pip install MetaTrader5 numpy
```

---

### Como Executar

1. **Certifique-se de que o MetaTrader 5 esteja instalado e conectado a uma conta válida.**  
2. **Edite a lista de ativos no código conforme sua estratégia.**  
3. **Execute o script:**  

```bash
python bot_mt5.py
```

4. **Acompanhe os logs em tempo real ou verifique os registros no arquivo de texto gerado.**  

---

### Observações Importantes

- **Cuidado com o Risco**: Sempre teste o bot em uma conta demo antes de utilizá-lo em uma conta real.  
- **Horários Configurados**: Certifique-se de que os horários configurados estejam alinhados ao fuso horário do servidor MT5.  
- **Condições de Mercado**: O bot pode não funcionar em condições de mercado extremas ou com ativos que possuem alta volatilidade.  

---

### Contribuições

Contribuições são bem-vindas! Caso você tenha melhorias ou ideias para adicionar ao projeto, sinta-se à vontade para enviar pull requests ou abrir issues.

---

### Licença

Este projeto é licenciado sob a **MIT License**. Use-o livremente, mas lembre-se de que ele é fornecido "como está", sem garantias de qualquer tipo.

---

Com este bot, você terá uma base sólida para explorar e automatizar estratégias de trading no MetaTrader 5. 🚀
