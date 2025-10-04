"""
Verifica se os arquivos FULL-LOAD no S3 contêm a coluna DtAtualizacao
"""
import boto3
import pandas as pd
from dotenv import load_dotenv
import os
from io import BytesIO

# Carrega credenciais
load_dotenv()

# Cliente S3
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

print("=" * 70)
print("VERIFICANDO COLUNA DtAtualizacao NO FULL-LOAD (S3)")
print("=" * 70)

tables = ['clientes', 'produtos', 'transacoes', 'transacao_produto']

for table_name in tables:
    try:
        key = f'upcell/full-load/{table_name}/{table_name}.parquet'
        
        # Baixa o arquivo do S3
        obj = s3.get_object(Bucket='meudatalake-raw', Key=key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        
        has_dt = 'DtAtualizacao' in df.columns
        
        print(f"\n📁 {table_name.upper()}")
        print(f"   Colunas: {list(df.columns)}")
        print(f"   {'✅' if has_dt else '❌'} DtAtualizacao presente: {has_dt}")
        
        if has_dt:
            print(f"   📅 Sample: {df['DtAtualizacao'].iloc[0]}")
            print(f"   📊 Total registros: {len(df):,}")
        
    except Exception as e:
        print(f"\n❌ {table_name.upper()}")
        print(f"   ERRO: {e}")

print("\n" + "=" * 70)
