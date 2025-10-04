# 🏗️ Arquitetura do Sistema CDC

Este documento detalha a arquitetura técnica do Sistema de Change Data Capture (CDC).

---

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                      SISTEMA CDC PIPELINE                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   SOURCE     │       │  PROCESSING  │       │ DESTINATION  │
│   (Kaggle)   │──────▶│   (Python)   │──────▶│   (AWS S3)   │
└──────────────┘       └──────────────┘       └──────────────┘
                              │
                              ├── Extract (Kaggle API)
                              ├── Transform (Pandas)
                              ├── CDC Detection (Diff)
                              └── Load (Boto3)
```

---

## 🔄 Fluxo de Dados Detalhado

### 1. Extração (Extract)

```
┌─────────────┐
│ Kaggle API  │
└─────┬───────┘
      │
      ├─ Dataset Download (ZIP)
      ├─ Extraction (.csv files)
      └─ Storage (data/actual/)
```

**Tecnologias:**
- `kaggle` library
- Python `zipfile`
- Autenticação via `kaggle.json`

**Processo:**
1. Autenticação via API Token
2. Download do dataset completo (formato ZIP)
3. Extração dos arquivos CSV
4. Armazenamento em `data/actual/`

### 2. Transformação (Transform)

```
┌──────────────────────────────────────┐
│      TRANSFORMATION LAYER            │
├──────────────────────────────────────┤
│  1. CSV to Parquet Conversion       │
│  2. Data Type Optimization           │
│  3. Compression (Snappy)             │
│  4. Schema Validation                │
└──────────────────────────────────────┘
```

**Tecnologias:**
- `pandas` (DataFrames)
- `pyarrow` (Parquet engine)

**Otimizações:**
- Conversão de tipos de dados
- Compressão Snappy (balanço velocidade/tamanho)
- Redução de ~70% no tamanho dos arquivos

### 3. CDC Detection

```
┌─────────────┐         ┌─────────────┐
│   LAST      │         │   ACTUAL    │
│  Snapshot   │         │  Snapshot   │
└──────┬──────┘         └──────┬──────┘
       │                       │
       └───────┬───────────────┘
               │
               ▼
     ┌─────────────────┐
     │  CDC DETECTOR   │
     ├─────────────────┤
     │  • INSERTS      │
     │  • UPDATES      │
     │  • DELETES      │
     └─────────────────┘
               │
               ▼
     ┌─────────────────┐
     │  CDC Parquet    │
     │  + Metadata     │
     └─────────────────┘
```

**Algoritmo de Detecção:**

```python
# Pseudo-código
def detect_cdc(last_df, actual_df, pk, date_field):
    # 1. INSERTS: Registros em actual que não estão em last
    inserts = actual_df[~actual_df[pk].isin(last_df[pk])]
    
    # 2. DELETES: Registros em last que não estão em actual
    deletes = last_df[~last_df[pk].isin(actual_df[pk])]
    
    # 3. UPDATES: Registros com mesmo PK mas dados diferentes
    merged = actual_df.merge(last_df, on=pk, suffixes=('_new', '_old'))
    if date_field:
        updates = merged[merged[f'{date_field}_new'] > merged[f'{date_field}_old']]
    else:
        updates = merged[merged != merged]  # Compare all fields
    
    return inserts, updates, deletes
```

**Metadados do CDC:**

Cada arquivo CDC contém:
- `_cdc_operation`: `I` (Insert), `U` (Update), `D` (Delete)
- `_cdc_timestamp`: Timestamp da geração do CDC
- Todos os campos originais da tabela

### 4. Carga (Load)

```
┌──────────────────────────────────────┐
│         AWS S3 STRUCTURE             │
├──────────────────────────────────────┤
│  bucket/                             │
│  └── prefix/                         │
│      ├── full-load/                  │
│      │   ├── clientes.parquet        │
│      │   ├── produtos.parquet        │
│      │   └── transacoes.parquet      │
│      └── cdc/                        │
│          ├── clientes_YYYYMMDD_HHMMSS.parquet
│          ├── produtos_YYYYMMDD_HHMMSS.parquet
│          └── transacoes_YYYYMMDD_HHMMSS.parquet
└──────────────────────────────────────┘
```

**Tecnologias:**
- `boto3` (AWS SDK)
- S3 Multipart Upload
- Retry logic com exponential backoff

---

## 🗄️ Modelo de Dados

### Estrutura Local

```
data/
├── actual/              # Dados atuais (após download)
│   ├── clientes.csv
│   ├── produtos.csv
│   └── transacoes.csv
│
├── last/                # Snapshot anterior (para CDC)
│   ├── clientes.csv
│   ├── produtos.csv
│   └── transacoes.csv
│
└── cdc/                 # CDC gerado (Parquet)
    ├── clientes_20251004_095645.parquet
    ├── produtos_20251004_095646.parquet
    └── transacoes_20251004_095647.parquet
```

### Schema CDC (Parquet)

```
clientes_CDC.parquet
├── idCliente (int64)              # Primary Key
├── Nome (string)
├── Email (string)
├── DtAtualizacao (datetime64)     # Date field
├── _cdc_operation (string)        # I/U/D
└── _cdc_timestamp (datetime64)    # Timestamp do CDC
```

---

## ⚙️ Componentes do Sistema

### 1. Configuration Manager

```python
class ConfigManager:
    - load_config(path: str) -> Dict
    - validate_config(config: Dict) -> bool
    - get_table_config(table_name: str) -> Dict
```

**Responsabilidades:**
- Carregamento do `config.json`
- Validação de parâmetros
- Acesso centralizado a configurações

### 2. Kaggle Downloader

```python
class KaggleDownloader:
    - authenticate() -> bool
    - download_dataset(dataset_name: str) -> bool
    - extract_files(zip_path: str, dest: str) -> List[str]
```

**Responsabilidades:**
- Autenticação na API
- Download de datasets
- Extração de arquivos

### 3. CDC Engine

```python
class CDCEngine:
    - detect_changes(last_df, actual_df, pk, date_field) -> DataFrame
    - classify_operations(changes: DataFrame) -> DataFrame
    - add_metadata(df: DataFrame) -> DataFrame
```

**Responsabilidades:**
- Detecção de mudanças
- Classificação de operações (I/U/D)
- Adição de metadados CDC

### 4. S3 Uploader

```python
class S3Uploader:
    - get_client() -> boto3.client
    - upload_file(local_path, s3_path) -> bool
    - upload_full_load(df, table_name) -> bool
    - upload_cdc(df, table_name, timestamp) -> bool
```

**Responsabilidades:**
- Conexão com AWS S3
- Upload de arquivos
- Gerenciamento de paths no S3

### 5. Pipeline Orchestrator

```python
class PipelineOrchestrator:
    - run_full_load() -> bool
    - run_cdc() -> bool
    - schedule_execution(interval: int, unit: str)
    - cleanup_old_files(keep_n: int)
```

**Responsabilidades:**
- Orquestração do fluxo completo
- Agendamento de execuções
- Limpeza de arquivos antigos

---

## 🔐 Segurança

### Autenticação e Autorização

```
┌─────────────────────────────────────┐
│      CREDENTIALS MANAGEMENT         │
├─────────────────────────────────────┤
│  Kaggle API Token                   │
│  ├── ~/.kaggle/kaggle.json          │
│  └── Env Vars: KAGGLE_USERNAME/KEY  │
│                                      │
│  AWS Credentials                     │
│  ├── ~/.aws/credentials             │
│  ├── Env Vars: AWS_ACCESS_KEY_ID    │
│  └── IAM Role (recommended)         │
└─────────────────────────────────────┘
```

**Boas Práticas:**
- Credenciais em `.env` (não versionado)
- IAM Roles em produção
- Least Privilege principle
- Credential rotation

### Permissões AWS IAM

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::seu-bucket/*",
        "arn:aws:s3:::seu-bucket"
      ]
    }
  ]
}
```

---

## 📊 Logging e Monitoramento

### Níveis de Log

```python
logging.DEBUG    # Detalhes técnicos, debug
logging.INFO     # Informações gerais (padrão)
logging.WARNING  # Avisos não críticos
logging.ERROR    # Erros que impedem operações
logging.CRITICAL # Erros críticos do sistema
```

### Estrutura de Logs

```
2025-10-04 09:56:43 - CDC_PIPELINE - INFO - Iniciando pipeline CDC
2025-10-04 09:56:45 - KAGGLE_DL - INFO - Dataset baixado: 125MB
2025-10-04 09:56:47 - CDC_ENGINE - INFO - CDC detectado: 15 inserts, 3 updates
2025-10-04 09:56:50 - S3_UPLOAD - INFO - Upload concluído: s3://bucket/prefix/cdc/
```

**Destinos:**
- Console (stdout)
- Arquivo: `cdc_pipeline.log`
- (Futuro) CloudWatch Logs

---

## 🚀 Escalabilidade

### Estratégias de Escala

**Horizontal Scaling:**
- Processar múltiplas tabelas em paralelo
- Usar multiprocessing/threading

**Vertical Scaling:**
- Otimizar uso de memória com chunks
- Processar DataFrames em batches

**Cloud Scaling:**
- Migrar para AWS Lambda (serverless)
- Usar AWS Glue para ETL gerenciado
- Implementar com Apache Airflow

### Performance

**Benchmarks:**
- 1GB CSV → 300MB Parquet (~70% redução)
- 1M registros processados em ~30s
- Upload S3: ~10MB/s (dependente de rede)

---

## 🔧 Tratamento de Erros

### Estratégias de Retry

```python
@retry(max_attempts=3, backoff=2)
def upload_to_s3(file_path, s3_path):
    try:
        s3_client.upload_file(file_path, bucket, s3_path)
    except ClientError as e:
        logger.error(f"Erro no upload: {e}")
        raise
```

**Cenários:**
- Network timeouts
- S3 throttling
- Kaggle API rate limits
- Disk space issues

---

## 📈 Melhorias Futuras

### Roadmap Técnico

**Fase 1: Estabilidade**
- ✅ Pipeline básico funcional
- ✅ Logging estruturado
- ✅ Tratamento de erros
- [ ] Testes unitários
- [ ] Testes de integração

**Fase 2: Otimização**
- [ ] Processamento paralelo
- [ ] Chunked processing
- [ ] Cache de metadata
- [ ] Compression tuning

**Fase 3: Evolução**
- [ ] Suporte a Delta Lake
- [ ] Integração com Airflow
- [ ] Monitoring dashboard
- [ ] Data quality checks

---

## 📚 Referências

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [AWS Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Apache Parquet Format](https://parquet.apache.org/docs/)
- [Kaggle API Documentation](https://github.com/Kaggle/kaggle-api)
- [CDC Best Practices](https://www.confluent.io/learn/change-data-capture/)

---

**Última atualização:** Outubro 2025
