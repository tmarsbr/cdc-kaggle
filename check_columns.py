import pandas as pd

tables = ['clientes', 'produtos', 'transacoes', 'transacao_produto']

for t in tables:
    df = pd.read_csv(f'data/actual/{t}.csv', sep=';', nrows=1)
    print(f'\n{t.upper()}:')
    print(f'  Colunas: {list(df.columns)}')
