import pandas as pd
from pathlib import Path

print("=" * 60)
print("ANÁLISE DE ARQUIVOS CDC")
print("=" * 60)

cdc_dir = Path('data/cdc')
files = sorted([f for f in cdc_dir.glob('*.parquet')])

for f in files:
    try:
        df = pd.read_parquet(f)
        ops = df['op'].value_counts().to_dict()
        print(f"{f.name:45} | {ops}")
    except Exception as e:
        print(f"{f.name:45} | ERRO: {e}")
