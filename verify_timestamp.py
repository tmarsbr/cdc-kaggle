import pandas as pd
from pathlib import Path

print("=" * 70)
print("VERIFICANDO COLUNA DtAtualizacao NOS ARQUIVOS CDC GERADOS")
print("=" * 70)

# Encontra os arquivos CDC mais recentes
cdc_dir = Path('data/cdc')
latest_files = {}

for pattern in ['clientes_20251003_163731.parquet', 
                'produtos_20251003_163731.parquet',
                'transacoes_20251003_163733.parquet',
                'transacao_produto_20251003_163734.parquet']:
    file_path = cdc_dir / pattern
    if file_path.exists():
        df = pd.read_parquet(file_path)
        table_name = pattern.split('_')[0]
        
        print(f"\n📁 {pattern}")
        print(f"   Colunas: {list(df.columns)}")
        print(f"   ✅ DtAtualizacao presente: {'DtAtualizacao' in df.columns}")
        
        if 'DtAtualizacao' in df.columns:
            print(f"   📅 Sample: {df['DtAtualizacao'].iloc[0]}")

print("\n" + "=" * 70)
