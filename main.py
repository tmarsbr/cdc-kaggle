"""
Sistema de CDC (Change Data Capture) para datasets do Kaggle
Autor: GitHub Copilot
Data: 2025-10-02

Este script automatiza:
- Download de datasets do Kaggle
- Upload de snapshots completos (full-load) para S3 em formato Parquet
- Geração de arquivos CDC comparando versões atual e anterior
- Upload de CDC para S3
- Agendamento automático de execuções

Funcionalidades principais:
1. Full-load: Download, conversão para Parquet e upload para S3
2. CDC: Detecção de inserções, atualizações e deleções
3. Logging estruturado com timestamps
4. Tratamento de erros e resiliência
5. Suporte a execução única ou agendada
"""

import argparse
import datetime
import json
import logging
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import boto3
import pandas as pd
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

# ==================== CONFIGURAÇÃO DE LOGGING ====================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('cdc_pipeline.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ==================== CONFIGURAÇÃO GLOBAL ====================

# Carrega variáveis de ambiente
load_dotenv(".env")

# Credenciais Kaggle
KAGGLE_USERNAME = os.getenv("KAGGLE_USERNAME")
KAGGLE_KEY = os.getenv("KAGGLE_KEY")

# Credenciais AWS
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")  # Opcional

# Diretórios locais
DIR_ACTUAL = Path("./data/actual")
DIR_LAST = Path("./data/last")
DIR_CDC = Path("./data/cdc")

# ==================== FUNÇÕES DE CONFIGURAÇÃO ====================

def load_config(config_path: str = "config.json") -> Dict:
    """
    Carrega o arquivo de configuração JSON.
    
    Args:
        config_path: Caminho para o arquivo config.json
        
    Returns:
        Dicionário com as configurações
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se o JSON for inválido
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        logger.info(f"Configuração carregada de {config_path}")
        return config
    except FileNotFoundError:
        logger.error(f"Arquivo de configuração não encontrado: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        raise


def validate_config(config: Dict) -> bool:
    """
    Valida se todas as configurações necessárias estão presentes.
    
    Args:
        config: Dicionário de configuração
        
    Returns:
        True se válido, False caso contrário
    """
    required_keys = ["dataset_name", "aws", "timer", "tables"]
    aws_keys = ["bucket", "prefix", "region"]
    
    for key in required_keys:
        if key not in config:
            logger.error(f"Chave obrigatória ausente no config.json: {key}")
            return False
    
    for key in aws_keys:
        if key not in config["aws"]:
            logger.error(f"Chave obrigatória ausente em aws: {key}")
            return False
    
    if not KAGGLE_USERNAME or not KAGGLE_KEY:
        logger.error("Credenciais Kaggle não configuradas no .env")
        return False
    
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        logger.error("Credenciais AWS não configuradas no .env")
        return False
    
    logger.info("Configuração validada com sucesso")
    return True


def create_directories():
    """
    Cria os diretórios necessários para o funcionamento do pipeline.
    """
    directories = [DIR_ACTUAL, DIR_LAST, DIR_CDC]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Diretório garantido: {directory}")


# ==================== FUNÇÕES DE DOWNLOAD (KAGGLE) ====================

def download_dataset(dataset_name: str) -> bool:
    """
    Faz o download do dataset do Kaggle para o diretório ./data/actual/.
    
    Args:
        dataset_name: Nome do dataset no formato 'usuario/nome-dataset'
        
    Returns:
        True se o download foi bem-sucedido, False caso contrário
    """
    try:
        logger.info(f"Iniciando download do dataset: {dataset_name}")
        
        # Configura credenciais do Kaggle
        os.environ['KAGGLE_USERNAME'] = KAGGLE_USERNAME
        os.environ['KAGGLE_KEY'] = KAGGLE_KEY
        
        # Inicializa API do Kaggle
        api = KaggleApi()
        api.authenticate()
        
        # Limpa diretório atual se existir
        if DIR_ACTUAL.exists():
            shutil.rmtree(DIR_ACTUAL)
            logger.debug(f"Diretório {DIR_ACTUAL} limpo")
        
        DIR_ACTUAL.mkdir(parents=True, exist_ok=True)
        
        # Faz o download e descompacta
        api.dataset_download_files(
            dataset_name,
            path=str(DIR_ACTUAL),
            unzip=True
        )
        
        logger.info(f"Download concluído: {dataset_name}")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao baixar dataset {dataset_name}: {e}", exc_info=True)
        return False


# ==================== FUNÇÕES DE UPLOAD (S3) ====================

def get_s3_client():
    """
    Cria e retorna um cliente boto3 para S3.
    
    Returns:
        Cliente boto3 S3
    """
    try:
        session_kwargs = {
            'aws_access_key_id': AWS_ACCESS_KEY_ID,
            'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
            'region_name': AWS_REGION
        }
        
        if AWS_SESSION_TOKEN:
            session_kwargs['aws_session_token'] = AWS_SESSION_TOKEN
        
        s3_client = boto3.client('s3', **session_kwargs)
        logger.debug("Cliente S3 criado com sucesso")
        return s3_client
        
    except Exception as e:
        logger.error(f"Erro ao criar cliente S3: {e}", exc_info=True)
        raise


def upload_to_s3(
    local_path: str,
    bucket: str,
    s3_key: str,
    s3_client=None
) -> bool:
    """
    Faz upload de um arquivo local para o S3.
    
    Args:
        local_path: Caminho do arquivo local
        bucket: Nome do bucket S3
        s3_key: Chave (caminho) no S3
        s3_client: Cliente S3 (opcional, criará um se não fornecido)
        
    Returns:
        True se o upload foi bem-sucedido, False caso contrário
    """
    try:
        if s3_client is None:
            s3_client = get_s3_client()
        
        logger.info(f"Fazendo upload: {local_path} -> s3://{bucket}/{s3_key}")
        
        s3_client.upload_file(local_path, bucket, s3_key)
        
        logger.info(f"Upload concluído: s3://{bucket}/{s3_key}")
        return True
        
    except (BotoCoreError, ClientError) as e:
        logger.error(f"Erro ao fazer upload para S3: {e}", exc_info=True)
        return False
    except FileNotFoundError:
        logger.error(f"Arquivo local não encontrado: {local_path}")
        return False


# ==================== FUNÇÕES DE FULL-LOAD ====================

def process_full_load(config: Dict, s3_client=None) -> bool:
    """
    Processa o full-load de todas as tabelas:
    1. Lê CSV do diretório actual
    2. Converte para Parquet
    3. Faz upload para S3 em full-load/
    
    Args:
        config: Dicionário de configuração
        s3_client: Cliente S3 (opcional)
        
    Returns:
        True se todos os uploads foram bem-sucedidos, False caso contrário
    """
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESSO DE FULL-LOAD")
    logger.info("=" * 60)
    
    if s3_client is None:
        s3_client = get_s3_client()
    
    bucket = config["aws"]["bucket"]
    prefix = config["aws"]["prefix"]
    tables = config["tables"]
    
    success = True
    
    for table in tables:
        table_name = table["name"]
        separator = table["sep"]
        
        try:
            # Caminho do CSV original
            csv_path = DIR_ACTUAL / f"{table_name}.csv"
            
            if not csv_path.exists():
                logger.warning(f"Arquivo não encontrado: {csv_path}")
                success = False
                continue
            
            logger.info(f"Processando full-load: {table_name}")
            
            # Lê CSV
            df = pd.read_csv(csv_path, sep=separator)
            logger.debug(f"CSV lido: {df.shape[0]} linhas, {df.shape[1]} colunas")
            
            # Adiciona coluna DtAtualizacao se não existir (para compatibilidade com PySpark)
            if 'DtAtualizacao' not in df.columns:
                df['DtAtualizacao'] = datetime.datetime.now()
                logger.debug(f"Coluna DtAtualizacao adicionada em full-load de {table_name}")
            
            # Caminho temporário para Parquet
            parquet_path = DIR_ACTUAL / f"{table_name}.parquet"
            
            # Salva como Parquet
            df.to_parquet(parquet_path, index=False, engine='pyarrow')
            logger.debug(f"Parquet criado: {parquet_path}")
            
            # Chave S3 para full-load
            s3_key = f"{prefix}/full-load/{table_name}/{table_name}.parquet"
            
            # Upload para S3
            if not upload_to_s3(str(parquet_path), bucket, s3_key, s3_client):
                success = False
            
            # Remove arquivo Parquet temporário
            parquet_path.unlink()
            logger.debug(f"Arquivo temporário removido: {parquet_path}")
            
        except Exception as e:
            logger.error(f"Erro ao processar full-load de {table_name}: {e}", exc_info=True)
            success = False
    
    if success:
        logger.info("Full-load concluído com sucesso para todas as tabelas")
    else:
        logger.warning("Full-load concluído com alguns erros")
    
    return success


# ==================== FUNÇÕES DE CDC ====================

def get_insert_lines(df_last: pd.DataFrame, df_actual: pd.DataFrame, pk: str) -> pd.DataFrame:
    """
    Identifica linhas inseridas (presentes no atual mas não no anterior).
    
    Args:
        df_last: DataFrame do snapshot anterior
        df_actual: DataFrame do snapshot atual
        pk: Nome da coluna de chave primária
        
    Returns:
        DataFrame com as linhas inseridas e coluna 'op' = 'I'
    """
    df_insert = df_actual[~df_actual[pk].isin(df_last[pk])].copy()
    df_insert["op"] = "I"
    logger.debug(f"Inserções detectadas: {len(df_insert)}")
    return df_insert


def get_update_lines(
    df_last: pd.DataFrame,
    df_actual: pd.DataFrame,
    pk: str,
    date_field: str
) -> pd.DataFrame:
    """
    Identifica linhas atualizadas (PK existe em ambos e campo de data é maior no atual).
    Se date_field for None ou vazio, compara todas as colunas por hash.
    
    Args:
        df_last: DataFrame do snapshot anterior
        df_actual: DataFrame do snapshot atual
        pk: Nome da coluna de chave primária
        date_field: Nome do campo de data para comparação (pode ser None)
        
    Returns:
        DataFrame com as linhas atualizadas e coluna 'op' = 'U'
    """
    # Se não houver campo de data, compara todas as colunas por hash
    if not date_field or date_field == "":
        # Cria hash de todas as colunas (exceto PK)
        cols_to_hash = [c for c in df_last.columns if c != pk]
        df_last_hash = df_last.copy()
        df_actual_hash = df_actual.copy()
        df_last_hash['_hash'] = df_last_hash[cols_to_hash].apply(lambda x: hash(tuple(x)), axis=1)
        df_actual_hash['_hash'] = df_actual_hash[cols_to_hash].apply(lambda x: hash(tuple(x)), axis=1)
        
        # Merge para comparar hashes
        df_merged = df_last_hash[[pk, '_hash']].merge(
            df_actual_hash[[pk, '_hash']],
            how='inner',
            on=pk,
            suffixes=('_last', '_actual')
        )
        
        # Linhas com hash diferente são updates
        update_mask = df_merged['_hash_last'] != df_merged['_hash_actual']
        updated_pks = df_merged[update_mask][pk].tolist()
        
        df_update = df_actual[df_actual[pk].isin(updated_pks)].copy()
        df_update["op"] = "U"
        logger.debug(f"Atualizações detectadas (por hash): {len(df_update)}")
        return df_update
    
    # Merge para comparar
    df_merged = df_last.merge(
        df_actual,
        how='inner',
        on=pk,
        suffixes=('_last', '_actual')
    )
    
    # Identifica atualizações comparando o campo de data
    date_last = f"{date_field}_last"
    date_actual = f"{date_field}_actual"
    
    # Verifica se as colunas existem
    if date_last not in df_merged.columns or date_actual not in df_merged.columns:
        logger.warning(f"Campo de data '{date_field}' não encontrado. Usando comparação por hash.")
        # Fallback para comparação por hash
        return get_update_lines(df_last, df_actual, pk, None)
    
    # Converte para datetime se necessário
    try:
        df_merged[date_last] = pd.to_datetime(df_merged[date_last], errors='coerce')
        df_merged[date_actual] = pd.to_datetime(df_merged[date_actual], errors='coerce')
        update_mask = df_merged[date_actual] > df_merged[date_last]
    except Exception:
        # Se não for data, compara como string
        update_mask = df_merged[date_actual] != df_merged[date_last]
    
    updated_pks = df_merged[update_mask][pk].tolist()
    
    # Retorna as linhas atualizadas do snapshot atual
    df_update = df_actual[df_actual[pk].isin(updated_pks)].copy()
    df_update["op"] = "U"
    logger.debug(f"Atualizações detectadas: {len(df_update)}")
    return df_update


def get_delete_lines(df_last: pd.DataFrame, df_actual: pd.DataFrame, pk: str) -> pd.DataFrame:
    """
    Identifica linhas deletadas (presentes no anterior mas não no atual).
    
    Args:
        df_last: DataFrame do snapshot anterior
        df_actual: DataFrame do snapshot atual
        pk: Nome da coluna de chave primária
        
    Returns:
        DataFrame com as linhas deletadas e coluna 'op' = 'D'
    """
    df_delete = df_last[~df_last[pk].isin(df_actual[pk])].copy()
    df_delete["op"] = "D"
    logger.debug(f"Deleções detectadas: {len(df_delete)}")
    return df_delete


def create_cdc(
    df_actual: pd.DataFrame,
    df_last: pd.DataFrame,
    pk: str,
    date_field: str
) -> pd.DataFrame:
    """
    Cria o DataFrame de CDC combinando inserções, atualizações e deleções.
    
    Args:
        df_actual: DataFrame do snapshot atual (ordem corrigida)
        df_last: DataFrame do snapshot anterior (ordem corrigida)
        pk: Nome da coluna de chave primária
        date_field: Nome do campo de data para comparação
        
    Returns:
        DataFrame completo de CDC com coluna 'op'
    """
    df_insert = get_insert_lines(df_last, df_actual, pk)
    df_update = get_update_lines(df_last, df_actual, pk, date_field)
    df_delete = get_delete_lines(df_last, df_actual, pk)
    
    df_cdc = pd.concat([df_insert, df_update, df_delete], ignore_index=True)
    
    logger.info(
        f"CDC criado - Inserções: {len(df_insert)}, "
        f"Atualizações: {len(df_update)}, Deleções: {len(df_delete)}, "
        f"Total: {len(df_cdc)}"
    )
    
    return df_cdc


def process_cdc(config: Dict, s3_client=None) -> bool:
    """
    Processa o CDC de todas as tabelas:
    1. Compara snapshots atual e anterior
    2. Gera arquivo CDC em Parquet
    3. Faz upload para S3 em cdc/
    
    Args:
        config: Dicionário de configuração
        s3_client: Cliente S3 (opcional)
        
    Returns:
        True se todos os CDCs foram processados com sucesso, False caso contrário
    """
    logger.info("=" * 60)
    logger.info("INICIANDO PROCESSO DE CDC")
    logger.info("=" * 60)
    
    if s3_client is None:
        s3_client = get_s3_client()
    
    bucket = config["aws"]["bucket"]
    prefix = config["aws"]["prefix"]
    tables = config["tables"]
    
    success = True
    
    for table in tables:
        table_name = table["name"]
        separator = table["sep"]
        pk = table["pk"]
        date_field = table["date_field"]
        
        try:
            logger.info(f"Processando CDC: {table_name}")
            
            # Caminhos dos arquivos
            actual_csv = DIR_ACTUAL / f"{table_name}.csv"
            last_csv = DIR_LAST / f"{table_name}.csv"
            
            if not actual_csv.exists():
                logger.warning(f"Snapshot atual não encontrado: {actual_csv}")
                success = False
                continue
            
            # Lê snapshot atual
            df_actual = pd.read_csv(actual_csv, sep=separator)
            
            # Remove coluna 'op' se existir (de execuções anteriores)
            if 'op' in df_actual.columns:
                df_actual = df_actual.drop(columns=['op'])
            
            # Verifica se existe snapshot anterior
            if not last_csv.exists():
                logger.warning(
                    f"Snapshot anterior não encontrado para {table_name}. "
                    f"Todas as {len(df_actual)} linhas serão consideradas inserções."
                )
                df_cdc = df_actual.copy()
                df_cdc["op"] = "I"
            else:
                # Lê snapshot anterior
                df_last = pd.read_csv(last_csv, sep=separator)
                
                # Remove coluna 'op' se existir (de execuções anteriores)
                if 'op' in df_last.columns:
                    df_last = df_last.drop(columns=['op'])
                
                # Gera CDC (IMPORTANTE: ordem correta é df_actual, df_last)
                df_cdc = create_cdc(df_actual, df_last, pk, date_field)
            
            # Se não houver mudanças, pula
            if df_cdc.empty:
                logger.info(f"Nenhuma alteração detectada para {table_name}")
                continue
            
            # Adiciona coluna DtAtualizacao se não existir (para compatibilidade com PySpark)
            if 'DtAtualizacao' not in df_cdc.columns:
                df_cdc['DtAtualizacao'] = datetime.datetime.now()
                logger.debug(f"Coluna DtAtualizacao adicionada em {table_name}")
            
            # Gera timestamp para o nome do arquivo
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cdc_filename = f"{table_name}_{timestamp}.parquet"
            cdc_path = DIR_CDC / cdc_filename
            
            # Salva CDC como Parquet
            df_cdc.to_parquet(cdc_path, index=False, engine='pyarrow')
            logger.debug(f"CDC Parquet criado: {cdc_path}")
            
            # Chave S3 para CDC
            s3_key = f"{prefix}/cdc/{table_name}/{cdc_filename}"
            
            # Upload para S3
            if not upload_to_s3(str(cdc_path), bucket, s3_key, s3_client):
                success = False
            
            logger.info(f"CDC processado com sucesso: {table_name}")
            
        except Exception as e:
            logger.error(f"Erro ao processar CDC de {table_name}: {e}", exc_info=True)
            success = False
    
    if success:
        logger.info("CDC concluído com sucesso para todas as tabelas")
    else:
        logger.warning("CDC concluído com alguns erros")
    
    return success


# ==================== FUNÇÕES DE PÓS-PROCESSAMENTO ====================

def move_snapshots() -> bool:
    """
    Move arquivos de ./data/actual/ para ./data/last/ para uso no próximo ciclo.
    
    Returns:
        True se a movimentação foi bem-sucedida, False caso contrário
    """
    try:
        logger.info("Movendo snapshots de actual para last")
        
        if not DIR_ACTUAL.exists():
            logger.warning(f"Diretório {DIR_ACTUAL} não existe")
            return False
        
        # Cria diretório last se não existir
        DIR_LAST.mkdir(parents=True, exist_ok=True)
        
        # Move cada arquivo CSV
        csv_files = list(DIR_ACTUAL.glob("*.csv"))
        
        if not csv_files:
            logger.warning("Nenhum arquivo CSV encontrado em actual")
            return False
        
        for csv_file in csv_files:
            dest = DIR_LAST / csv_file.name
            
            # Remove arquivo de destino se existir
            if dest.exists():
                dest.unlink()
            
            # Move arquivo
            shutil.move(str(csv_file), str(dest))
            logger.debug(f"Movido: {csv_file.name}")
        
        logger.info(f"{len(csv_files)} arquivo(s) movido(s) com sucesso")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao mover snapshots: {e}", exc_info=True)
        return False


def cleanup_local_cdc(keep_last_n: int = 5) -> bool:
    """
    Remove arquivos CDC locais antigos, mantendo apenas os N mais recentes de cada tabela.
    
    Args:
        keep_last_n: Número de arquivos mais recentes a manter por tabela (padrão: 5)
        
    Returns:
        True se a limpeza foi bem-sucedida, False caso contrário
    """
    try:
        if not DIR_CDC.exists():
            logger.debug(f"Diretório CDC {DIR_CDC} não existe")
            return True
        
        # Lista todos os arquivos Parquet no diretório CDC
        cdc_files = list(DIR_CDC.glob("*.parquet"))
        
        if not cdc_files:
            logger.debug("Nenhum arquivo CDC local para limpar")
            return True
        
        # Agrupa arquivos por tabela
        files_by_table = {}
        for file in cdc_files:
            # Extrai nome da tabela do nome do arquivo (formato: tabela_YYYYMMDD_HHMMSS.parquet)
            parts = file.stem.split('_')
            if len(parts) >= 3:
                table_name = '_'.join(parts[:-2])  # Suporta nomes com underscore (ex: transacao_produto)
            else:
                table_name = parts[0]
            
            if table_name not in files_by_table:
                files_by_table[table_name] = []
            files_by_table[table_name].append(file)
        
        # Remove arquivos antigos de cada tabela
        total_removed = 0
        for table_name, files in files_by_table.items():
            # Ordena por data de modificação (mais recente primeiro)
            files_sorted = sorted(files, key=lambda f: f.stat().st_mtime, reverse=True)
            
            # Remove arquivos além dos N mais recentes
            files_to_remove = files_sorted[keep_last_n:]
            
            for file in files_to_remove:
                try:
                    file.unlink()
                    logger.debug(f"Removido arquivo CDC local: {file.name}")
                    total_removed += 1
                except Exception as e:
                    logger.warning(f"Erro ao remover {file.name}: {e}")
        
        if total_removed > 0:
            logger.info(f"Limpeza CDC local: {total_removed} arquivo(s) antigo(s) removido(s)")
        else:
            logger.debug("Nenhum arquivo CDC local precisou ser removido")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao limpar arquivos CDC locais: {e}", exc_info=True)
        return False


# ==================== PIPELINE PRINCIPAL ====================

def run_pipeline(config: Dict, skip_download: bool = False) -> bool:
    """
    Executa o pipeline completo de CDC.
    
    Args:
        config: Dicionário de configuração
        skip_download: Se True, pula o download (útil para testes)
        
    Returns:
        True se o pipeline foi executado com sucesso, False caso contrário
    """
    try:
        logger.info("=" * 60)
        logger.info("INICIANDO PIPELINE DE CDC")
        logger.info("=" * 60)
        
        # Cria diretórios necessários
        create_directories()
        
        # Move snapshots anteriores (se existirem) antes do download
        if DIR_ACTUAL.exists() and any(DIR_ACTUAL.glob("*.csv")):
            logger.info("Movendo snapshots existentes para last")
            move_snapshots()
        
        # Cria cliente S3 único para reutilização
        s3_client = get_s3_client()
        
        # 1. Download do dataset
        if not skip_download:
            dataset_name = config["dataset_name"]
            if not download_dataset(dataset_name):
                logger.error("Falha no download do dataset")
                return False
        else:
            logger.info("Download pulado (skip_download=True)")
        
        # 2. Full-load para S3
        if not process_full_load(config, s3_client):
            logger.error("Falha no processo de full-load")
            return False
        
        # 3. Geração e upload de CDC
        if not process_cdc(config, s3_client):
            logger.error("Falha no processo de CDC")
            return False
        
        # 4. Limpeza de arquivos CDC locais antigos (se habilitado)
        cleanup_config = config.get("cleanup", {})
        if cleanup_config.get("enabled", True):
            keep_n = cleanup_config.get("keep_last_n_cdc_files", 5)
            cleanup_local_cdc(keep_last_n=keep_n)
        
        logger.info("=" * 60)
        logger.info("PIPELINE CONCLUÍDO COM SUCESSO")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Erro fatal no pipeline: {e}", exc_info=True)
        return False


# ==================== AGENDADOR ====================

def calculate_sleep_seconds(timer_config: Dict) -> int:
    """
    Calcula o intervalo de sleep em segundos baseado na configuração.
    
    Args:
        timer_config: Dicionário com 'unit' e 'value'
        
    Returns:
        Número de segundos para sleep
    """
    unit = timer_config["unit"].lower()
    value = timer_config["value"]
    
    multipliers = {
        "minutes": 60,
        "hours": 3600,
        "days": 86400
    }
    
    if unit not in multipliers:
        logger.warning(f"Unidade de timer desconhecida: {unit}. Usando 'hours'.")
        unit = "hours"
    
    seconds = value * multipliers[unit]
    logger.info(f"Intervalo configurado: {value} {unit} ({seconds} segundos)")
    
    return seconds


def run_scheduler(config: Dict):
    """
    Executa o pipeline em loop contínuo com intervalos configurados.
    
    Args:
        config: Dicionário de configuração
    """
    sleep_seconds = calculate_sleep_seconds(config["timer"])
    
    logger.info("MODO AGENDADO ATIVADO")
    logger.info(f"O pipeline será executado a cada {config['timer']['value']} {config['timer']['unit']}")
    
    iteration = 1
    
    while True:
        try:
            logger.info(f"\n{'=' * 60}")
            logger.info(f"ITERAÇÃO {iteration}")
            logger.info(f"{'=' * 60}\n")
            
            # Executa o pipeline
            success = run_pipeline(config)
            
            if not success:
                logger.warning(f"Iteração {iteration} concluída com erros")
            else:
                logger.info(f"Iteração {iteration} concluída com sucesso")
            
            # Aguarda próximo ciclo
            next_run = datetime.datetime.now() + datetime.timedelta(seconds=sleep_seconds)
            logger.info(f"Próxima execução agendada para: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"Aguardando {sleep_seconds} segundos...\n")
            
            time.sleep(sleep_seconds)
            iteration += 1
            
        except KeyboardInterrupt:
            logger.info("\nInterrompido pelo usuário. Encerrando...")
            break
        except Exception as e:
            logger.error(f"Erro na iteração {iteration}: {e}", exc_info=True)
            logger.info(f"Aguardando {sleep_seconds} segundos antes de tentar novamente...")
            time.sleep(sleep_seconds)
            iteration += 1


# ==================== MAIN ====================

def main():
    """
    Função principal com suporte a argumentos de linha de comando.
    """
    parser = argparse.ArgumentParser(
        description="Pipeline de CDC para datasets do Kaggle com upload para S3"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Executa o pipeline apenas uma vez (sem agendamento)"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Pula o download do Kaggle (útil para testes com dados locais)"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Caminho para o arquivo de configuração (padrão: config.json)"
    )
    
    args = parser.parse_args()
    
    try:
        # Carrega configuração
        config = load_config(args.config)
        
        # Valida configuração
        if not validate_config(config):
            logger.error("Configuração inválida. Verifique o config.json e o .env")
            sys.exit(1)
        
        # Executa pipeline
        if args.once:
            logger.info("MODO EXECUÇÃO ÚNICA")
            success = run_pipeline(config, skip_download=args.skip_download)
            sys.exit(0 if success else 1)
        else:
            run_scheduler(config)
            
    except KeyboardInterrupt:
        logger.info("\nInterrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
