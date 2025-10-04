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
print("ANÁLISE DE ARQUIVOS CDC NO S3")
print("=" * 70)

# Lista todos os arquivos CDC no S3
response = s3.list_objects_v2(Bucket='meudatalake-raw', Prefix='upcell/cdc/')

if 'Contents' not in response:
    print("Nenhum arquivo CDC encontrado no S3")
    exit()

files = sorted([obj['Key'] for obj in response['Contents']])

for key in files:
    try:
        # Baixa o arquivo
        obj = s3.get_object(Bucket='meudatalake-raw', Key=key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        
        # Obtém estatísticas da coluna op
        ops = df['op'].value_counts().to_dict()
        filename = key.split('/')[-1]
        
        print(f"{filename:50} | {ops}")
        
    except Exception as e:
        print(f"{key:50} | ERRO: {e}")

print("=" * 70)
