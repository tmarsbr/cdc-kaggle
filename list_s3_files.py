"""
Lista arquivos CDC antigos no S3 (sem DtAtualizacao)
"""
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

print("=" * 70)
print("ARQUIVOS CDC NO S3")
print("=" * 70)

response = s3.list_objects_v2(Bucket='meudatalake-raw', Prefix='upcell/cdc/')

if 'Contents' not in response:
    print("Nenhum arquivo encontrado")
    exit()

# Separa arquivos antigos (sem DtAtualizacao) dos novos (com DtAtualizacao)
files_old = []
files_new = []

for obj in response['Contents']:
    key = obj['Key']
    # Arquivos com timestamp >= 163731 têm DtAtualizacao
    if '20251003_1637' in key or '20251003_164739' in key or '20251003_170552' in key:
        files_new.append(key)
    else:
        files_old.append(key)

print(f"\n📊 RESUMO:")
print(f"   ✅ Arquivos NOVOS (com DtAtualizacao): {len(files_new)}")
print(f"   ⚠️  Arquivos ANTIGOS (sem DtAtualizacao): {len(files_old)}")

print(f"\n⚠️  ARQUIVOS ANTIGOS (primeiros 15):")
for f in sorted(files_old)[:15]:
    print(f"   - {f.split('/')[-1]}")

print(f"\n✅ ARQUIVOS NOVOS:")
for f in sorted(files_new):
    print(f"   - {f.split('/')[-1]}")

print("\n" + "=" * 70)
print("💡 RECOMENDAÇÃO:")
print("   No Databricks, use clearCache() e leia apenas os arquivos novos,")
print("   ou especifique o timestamp no path:")
print("   spark.read.parquet('s3://bucket/cdc/produtos/produtos_20251003_*.parquet')")
print("=" * 70)
