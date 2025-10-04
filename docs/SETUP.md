# 🚀 Guia de Instalação e Configuração

Este guia fornece instruções detalhadas para configurar e executar o Sistema de CDC (Change Data Capture).

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- **Python 3.8 ou superior** instalado
- **Git** instalado
- Conta no **Kaggle** (gratuita)
- Conta na **AWS** com acesso ao S3
- Editor de código (recomendado: VS Code)

---

## 🔧 Instalação Passo a Passo

### 1. Clone o Repositório

```bash
git clone https://github.com/TeoMeWhy/cdc-kaggle.git
cd cdc-kaggle
```

### 2. Crie um Ambiente Virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verifique a Instalação

```bash
python -c "import pandas; import boto3; import kaggle; print('Todas as dependências instaladas com sucesso!')"
```

---

## 🔑 Configuração de Credenciais

### Kaggle API

1. **Acesse sua conta Kaggle**:
   - Faça login em https://www.kaggle.com
   
2. **Gere o token de API**:
   - Vá para https://www.kaggle.com/settings
   - Clique em **"Create New API Token"**
   - Um arquivo `kaggle.json` será baixado

3. **Configure o arquivo kaggle.json**:

   **Windows:**
   ```bash
   mkdir %USERPROFILE%\.kaggle
   move kaggle.json %USERPROFILE%\.kaggle\
   ```

   **Linux/Mac:**
   ```bash
   mkdir -p ~/.kaggle
   mv kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

### AWS S3

1. **Acesse o Console AWS IAM**:
   - Faça login em https://console.aws.amazon.com/iam/

2. **Crie um novo usuário**:
   - Clique em **"Users"** → **"Add users"**
   - Nome: `cdc-pipeline-user`
   - Access type: **"Programmatic access"**

3. **Configure permissões**:
   - Attach policy: **"AmazonS3FullAccess"** (ou crie uma policy customizada)

4. **Salve as credenciais**:
   - Após criar o usuário, salve:
     - Access Key ID
     - Secret Access Key

5. **Crie um bucket S3**:
   ```bash
   aws s3 mb s3://meu-datalake-cdc --region us-east-1
   ```

---

## ⚙️ Arquivo de Configuração

### 1. Crie o arquivo `.env`

Na raiz do projeto, crie um arquivo `.env`:

```env
# Kaggle API Credentials
KAGGLE_USERNAME=seu_usuario_kaggle
KAGGLE_KEY=sua_chave_kaggle_api

# AWS Credentials
AWS_ACCESS_KEY_ID=sua_aws_access_key_id
AWS_SECRET_ACCESS_KEY=sua_aws_secret_access_key
AWS_REGION=us-east-1

# Opcional: AWS Session Token (para credenciais temporárias)
# AWS_SESSION_TOKEN=seu_token_temporario
```

### 2. Configure o arquivo `config.json`

Edite o arquivo `config.json` na raiz do projeto:

```json
{
    "dataset_name": "teocalvo/teomewhy-loyalty-system",
    
    "aws": {
        "bucket": "meu-datalake-cdc",
        "prefix": "raw/loyalty",
        "region": "us-east-1"
    },

    "timer": {
        "unit": "hours",
        "value": 6
    },

    "cleanup": {
        "enabled": true,
        "keep_last_n_cdc_files": 5
    },

    "tables": [
        {
            "name": "clientes",
            "sep": ";",
            "pk": "idCliente",
            "date_field": "DtAtualizacao"
        },
        {
            "name": "produtos",
            "sep": ";",
            "pk": "IdProduto",
            "date_field": ""
        },
        {
            "name": "transacoes",
            "sep": ";",
            "pk": "IdTransacao",
            "date_field": "DtCriacao"
        },
        {
            "name": "transacao_produto",
            "sep": ";",
            "pk": "idTransacaoProduto",
            "date_field": "vlProduto"
        }
    ]
}
```

#### Parâmetros do `config.json`:

| Parâmetro | Descrição |
|-----------|-----------|
| `dataset_name` | Nome do dataset no Kaggle (formato: `usuario/dataset`) |
| `aws.bucket` | Nome do bucket S3 onde os dados serão armazenados |
| `aws.prefix` | Prefixo (pasta) dentro do bucket |
| `aws.region` | Região AWS do bucket |
| `timer.unit` | Unidade de tempo para execuções agendadas (`hours`, `minutes`) |
| `timer.value` | Valor numérico do intervalo |
| `cleanup.enabled` | Habilita limpeza automática de arquivos antigos |
| `cleanup.keep_last_n_cdc_files` | Quantidade de arquivos CDC a manter |
| `tables[].name` | Nome da tabela/arquivo CSV |
| `tables[].sep` | Separador usado no CSV (`;` ou `,`) |
| `tables[].pk` | Campo que serve como Primary Key |
| `tables[].date_field` | Campo de data/timestamp para detecção de mudanças |

---

## 🧪 Teste a Configuração

### 1. Teste as credenciais Kaggle

```bash
python -c "from kaggle.api.kaggle_api_extended import KaggleApi; api = KaggleApi(); api.authenticate(); print('Kaggle OK!')"
```

### 2. Teste as credenciais AWS

```bash
python -c "import boto3; s3 = boto3.client('s3'); print('AWS OK! Buckets:', [b['Name'] for b in s3.list_buckets()['Buckets'][:3]])"
```

### 3. Execute o pipeline em modo de teste

```bash
python main.py
```

---

## 📁 Estrutura de Diretórios

Após a primeira execução, a seguinte estrutura será criada:

```
cdc-kaggle/
├── data/
│   ├── actual/              # Dados atuais baixados do Kaggle
│   │   ├── clientes.csv
│   │   ├── produtos.csv
│   │   └── transacoes.csv
│   ├── last/                # Snapshot anterior (para comparação CDC)
│   │   ├── clientes.csv
│   │   ├── produtos.csv
│   │   └── transacoes.csv
│   └── cdc/                 # Arquivos CDC gerados (Parquet)
│       ├── clientes_20251004_095645.parquet
│       ├── produtos_20251004_095646.parquet
│       └── transacoes_20251004_095647.parquet
├── docs/                    # Documentação
├── .venv/                   # Ambiente virtual (não versionado)
├── .env                     # Credenciais (não versionado)
├── config.json              # Configurações do pipeline
├── main.py                  # Script principal
└── requirements.txt         # Dependências Python
```

---

## 🎯 Modos de Execução

### Execução Única

Execute o pipeline uma vez:

```bash
python main.py
```

### Execução Agendada (Loop)

Execute o pipeline continuamente com intervalo configurado:

```bash
python main.py --schedule
```

Para parar a execução: `Ctrl + C`

### Agendamento no Windows Task Scheduler

Veja as instruções completas em [`docs/AGENDAMENTO.md`](AGENDAMENTO.md).

---

## 🐛 Solução de Problemas

### Erro: "Kaggle credentials not found"

**Solução:**
1. Verifique se o arquivo `kaggle.json` está em `~/.kaggle/` (Linux/Mac) ou `%USERPROFILE%\.kaggle\` (Windows)
2. Verifique as permissões do arquivo (deve ser 600 no Linux/Mac)

### Erro: "Could not connect to AWS"

**Solução:**
1. Verifique se as variáveis de ambiente estão configuradas no `.env`
2. Execute: `aws configure` para configurar credenciais via AWS CLI
3. Verifique se o usuário IAM tem permissões no S3

### Erro: "No module named 'pandas'"

**Solução:**
```bash
pip install --upgrade -r requirements.txt
```

### Erro: "Permission denied" ao escrever em data/

**Solução:**
1. Verifique permissões das pastas
2. Execute como administrador (Windows) ou com `sudo` (Linux/Mac)

---

## 📊 Verificação de Dados

### Verificar arquivos locais

```bash
# Listar arquivos CDC gerados
ls data/cdc/

# Ver conteúdo de um arquivo Parquet
python -c "import pandas as pd; print(pd.read_parquet('data/cdc/clientes_20251004_095645.parquet').head())"
```

### Verificar dados no S3

```bash
# Listar arquivos no bucket
aws s3 ls s3://meu-datalake-cdc/raw/loyalty/cdc/

# Baixar um arquivo para análise
aws s3 cp s3://meu-datalake-cdc/raw/loyalty/cdc/clientes_20251004_095645.parquet ./
```

---

## 🔒 Segurança

### Boas Práticas

1. **Nunca commit credenciais**: O `.env` já está no `.gitignore`
2. **Use IAM Roles**: Em produção, prefira IAM Roles ao invés de chaves estáticas
3. **Rotate credentials**: Renove suas credenciais AWS periodicamente
4. **Least privilege**: Dê apenas as permissões necessárias ao usuário IAM
5. **Encryption**: Configure encryption at rest no S3

---

## 📚 Próximos Passos

Após configurar o sistema:

1. ✅ Execute o pipeline manualmente para testar
2. ✅ Verifique os logs em `cdc_pipeline.log`
3. ✅ Confirme os uploads no S3
4. ✅ Configure agendamento automático (opcional)
5. ✅ Monitore a primeira execução agendada

---

## 📞 Suporte

- **Issues**: Abra uma issue no [GitHub](https://github.com/TeoMeWhy/cdc-kaggle/issues)
- **Email**: contato@exemplo.com
- **Documentação**: Consulte o [README principal](../README.md)

---

**🎉 Pronto! Seu ambiente está configurado e pronto para uso.**
