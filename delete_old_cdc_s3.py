"""
Deleta arquivos CDC antigos do S3 (sem coluna DtAtualizacao)
Mantém apenas os arquivos novos gerados após 2025-10-03 16:37
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
print("DELETANDO ARQUIVOS CDC ANTIGOS DO S3")
print("=" * 70)

# Lista todos os arquivos CDC
response = s3.list_objects_v2(Bucket='meudatalake-raw', Prefix='upcell/cdc/')

if 'Contents' not in response:
    print("Nenhum arquivo encontrado")
    exit()

# Identifica arquivos antigos (sem DtAtualizacao)
# Arquivos com timestamp >= 20251003_1637 têm DtAtualizacao
files_to_delete = []

for obj in response['Contents']:
    key = obj['Key']
    # Mantém apenas arquivos novos (com DtAtualizacao)
    if '20251003_1637' not in key and '20251003_164739' not in key and '20251003_170552' not in key:
        files_to_delete.append(key)

print(f"\n📊 RESUMO:")
print(f"   ⚠️  Arquivos ANTIGOS (sem DtAtualizacao): {len(files_to_delete)}")
print(f"\n⚠️  ARQUIVOS QUE SERÃO DELETADOS:")

for f in sorted(files_to_delete):
    print(f"   - {f.split('/')[-1]}")

# Confirma
print(f"\n{'='*70}")
resposta = input("⚠️  ATENÇÃO! Deseja DELETAR estes arquivos? (sim/não): ").strip().lower()

if resposta == 'sim':
    print(f"\n🗑️  Deletando arquivos...")
    deleted_count = 0
    
    for key in files_to_delete:
        try:
            s3.delete_object(Bucket='meudatalake-raw', Key=key)
            print(f"   ✅ Deletado: {key.split('/')[-1]}")
            deleted_count += 1
        except Exception as e:
            print(f"   ❌ Erro ao deletar {key}: {e}")
    
    print(f"\n{'='*70}")
    print(f"✅ {deleted_count} arquivo(s) deletado(s) com sucesso!")
    print(f"{'='*70}")
    
else:
    print("\n❌ Operação cancelada. Nenhum arquivo foi deletado.")
    print("=" * 70)
