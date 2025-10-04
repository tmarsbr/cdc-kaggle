# 📊 Sistema de CDC (Change Data Capture) - Kaggle para AWS S3# 📊 Sistema de CDC (Change Data Capture) - Kaggle para AWS S3# Sistema de CDC (Change Data Capture) - Kaggle para S3# CDC com dados do Kaggle



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

[![Pandas](https://img.shields.io/badge/Pandas-2.2.0-green.svg)](https://pandas.pydata.org/)[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

> **Pipeline automatizado de ETL para captura incremental de dados (CDC) com integração Kaggle → AWS S3**

[![Pandas](https://img.shields.io/badge/Pandas-2.2.0-green.svg)](https://pandas.pydata.org/)Sistema completo de **Change Data Capture** que automatiza o download de datasets do Kaggle, processa snapshots em formato Parquet e envia para um data lake no AWS S3.## Sobre

---

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Sobre o Projeto



Este projeto implementa um **pipeline completo de Change Data Capture (CDC)** que automatiza o processo de extração, transformação e carga de dados do Kaggle para um Data Lake na AWS S3. O sistema detecta automaticamente mudanças nos dados (inserções, atualizações e deleções), converte os arquivos para formato Parquet otimizado e mantém um histórico incremental de alterações.

> Pipeline automatizado de ETL para captura incremental de dados (CDC) com integração Kaggle → AWS S3

### 🎓 Objetivo de Aprendizado

## 📋 CaracterísticasAutomação para baixar dados do Kaggle e criar arquivos de CDC (Change Data Capture) comparando as duas últimas versões.

Desenvolvido como projeto de portfólio para demonstrar competências em:

- **Engenharia de Dados**: ETL, CDC, Data Lakes## 🎯 Sobre o Projeto

- **Cloud Computing**: AWS S3, Boto3

- **Python**: Pandas, Logging, Automação

- **Boas Práticas**: Código limpo, documentação, tratamento de erros

Este projeto implementa um **pipeline completo de Change Data Capture (CDC)** que automatiza o processo de extração, transformação e carga de dados do Kaggle para um Data Lake na AWS S3. O sistema detecta automaticamente mudanças nos dados (inserções, atualizações e deleções), converte os arquivos para formato Parquet otimizado e mantém um histórico incremental de alterações.

---

- ✅ Download automatizado de datasets do KaggleOs arquivos de CDC estarão disponíveis no diretório `./data/cdc/` no seguinte formato: `{tabela}_YYYMMDD_HHMMSS.csv`

## ✨ Principais Funcionalidades

### 🎓 Objetivo de Aprendizado

### 🔄 Change Data Capture (CDC)

- ✅ Detecção automática de **inserções**, **atualizações** e **deleções**- ✅ Conversão de CSV para Parquet

- ✅ Comparação baseada em Primary Keys e campos de data

- ✅ Geração de snapshots incrementais em ParquetDesenvolvido como projeto de portfólio para demonstrar competências em:

- ✅ Timestamps automáticos para rastreabilidade

- **Engenharia de Dados**: ETL, CDC, Data Lakes- ✅ Upload de full-load para S3## Setup

### 🚀 Pipeline Automatizado

- ✅ Download automático de datasets do Kaggle via API- **Cloud Computing**: AWS S3, Boto3

- ✅ Conversão otimizada de CSV para Parquet (redução de ~70% no tamanho)

- ✅ Upload incremental para AWS S3 com estrutura organizada- **Python**: Pandas, Logging, Automação- ✅ Detecção de CDC (inserções, atualizações e deleções)

- ✅ Limpeza automática de arquivos antigos (retention configurável)

- **Boas Práticas**: Código limpo, documentação, tratamento de erros

### 📊 Gestão de Dados

- ✅ Suporte a múltiplas tabelas configuráveis via JSON- ✅ Logging estruturado com timestamps### Instalando dependências

- ✅ Full-load inicial + cargas incrementais (CDC)

- ✅ Versionamento automático com timestamps---

- ✅ Logging estruturado com níveis de severidade

- ✅ Tratamento robusto de erros

### ⚙️ Configuração Flexível

- ✅ Configuração via JSON (`config.json`)## ✨ Principais Funcionalidades

- ✅ Variáveis de ambiente para credenciais (`.env`)

- ✅ Agendamento automático de execuções- ✅ Suporte a execução única ou agendadaSugirimos criar um ambiente virtual apropriado para execução do programa. Após isso, pode instalar as depedências usando `pip`:

- ✅ Tratamento robusto de erros e retry logic

### 🔄 Change Data Capture (CDC)

---

- ✅ Detecção automática de **inserções**, **atualizações** e **deleções**- ✅ Configuração via JSON e variáveis de ambiente

## 🏗️ Arquitetura do Sistema

- ✅ Comparação baseada em Primary Keys e campos de data

```

┌─────────────┐      ┌──────────────┐      ┌─────────────┐- ✅ Geração de snapshots incrementais em Parquet```bash

│   Kaggle    │──1──▶│  ETL Python  │──2──▶│   AWS S3    │

│   Dataset   │      │   Pipeline   │      │ Data Lake   │- ✅ Timestamps automáticos para rastreabilidade

└─────────────┘      └──────────────┘      └─────────────┘

                            │## 🛠️ Requisitospip install -r requirements.txt

                            │ 3. CDC Detection

                            ▼### 🚀 Pipeline Automatizado

                     ┌──────────────┐

                     │  Local Cache │- ✅ Download automático de datasets do Kaggle via API```

                     │ (Last/Actual)│

                     └──────────────┘- ✅ Conversão otimizada de CSV para Parquet (redução de ~70% no tamanho)

```

- ✅ Upload incremental para AWS S3 com estrutura organizada- Python 3.8+

### Fluxo de Dados

- ✅ Limpeza automática de arquivos antigos (configurable retention)

1. **Extração**: Download do dataset via Kaggle API

2. **Transformação**: Conversão CSV → Parquet + CDC Detection- Conta Kaggle com credenciais de APIPara garantir que a execução funciona corretamente, as seguintes variáveis ambientes devem estar configuradas:

3. **Carga**: Upload para S3 com estrutura particionada

4. **Histórico**: Manutenção de snapshots locais e remotos### 📊 Gestão de Dados



---- ✅ Suporte a múltiplas tabelas configuráveis via JSON- Credenciais AWS com permissões no S3



## 🛠️ Tecnologias Utilizadas- ✅ Full-load inicial + cargas incrementais (CDC)



| Categoria | Tecnologias |- ✅ Versionamento automático com timestamps- Bucket S3 criado```bash

|-----------|-------------|

| **Linguagem** | Python 3.8+ |- ✅ Logging estruturado com níveis de severidade

| **Data Processing** | Pandas, PyArrow (Parquet) |

| **Cloud** | AWS S3, Boto3 |KAGGLE_USERNAME=

| **APIs** | Kaggle API |

| **Automação** | Schedule, Windows Task Scheduler |### ⚙️ Configuração Flexível

| **Ambiente** | python-dotenv, logging |

- ✅ Configuração via JSON (`config.json`)## 📦 InstalaçãoKAGGLE_KEY=

---

- ✅ Variáveis de ambiente para credenciais (`.env`)

## 📋 Pré-requisitos

- ✅ Agendamento automático de execuções```

- Python 3.8 ou superior

- Conta Kaggle (com API Token)- ✅ Tratamento robusto de erros e retry logic

- Conta AWS (com acesso ao S3)

- Git1. Clone o repositório:



------



## 🚀 Instalação Rápida```bashCaso tenha interesse em alterar a periodicidade de atualização da carga, altere o valor da variável `timer` em `config.json`.



### 1. Clone o Repositório## 🏗️ Arquitetura do Sistema



```bashgit clone https://github.com/TeoMeWhy/cdc-kaggle.git

git clone https://github.com/TeoMeWhy/cdc-kaggle.git

cd cdc-kaggle```

```

┌─────────────┐      ┌──────────────┐      ┌─────────────┐cd cdc-kaggle## Execução

### 2. Instale as Dependências

│   Kaggle    │──1──▶│  ETL Python  │──2──▶│   AWS S3    │

```bash

# Crie um ambiente virtual (recomendado)│   Dataset   │      │   Pipeline   │      │ Data Lake   │```

python -m venv .venv

.venv\Scripts\activate  # Windows└─────────────┘      └──────────────┘      └─────────────┘



# Instale as dependências                            │```bash

pip install -r requirements.txt

```                            │ 3. CDC Detection



### 3. Configure as Credenciais                            ▼2. Instale as dependências:python main.py



Crie um arquivo `.env` na raiz do projeto:                     ┌──────────────┐



```env                     │  Local Cache │```bash```

# Kaggle API

KAGGLE_USERNAME=seu_usuario                     │ (Last/Actual)│pip install -r requirements.txt

KAGGLE_KEY=sua_chave_api

                     └──────────────┘```

# AWS Credentials

AWS_ACCESS_KEY_ID=sua_access_key```

AWS_SECRET_ACCESS_KEY=sua_secret_key

AWS_REGION=us-east-13. Configure as credenciais no arquivo `.env`:

```

### Fluxo de Dados```env

### 4. Configure o Pipeline

# Credenciais Kaggle

Edite o arquivo `config.json`:

1. **Extração**: Download do dataset via Kaggle APIKAGGLE_USERNAME=seu_usuario

```json

{2. **Transformação**: Conversão CSV → Parquet + CDC DetectionKAGGLE_KEY=sua_chave_api

    "dataset_name": "teocalvo/teomewhy-loyalty-system",

    "aws": {3. **Carga**: Upload para S3 com estrutura particionada

        "bucket": "seu-bucket-s3",

        "prefix": "seu-prefixo",4. **Histórico**: Manutenção de snapshots locais e remotos# Credenciais AWS

        "region": "us-east-1"

    },AWS_ACCESS_KEY_ID=sua_access_key

    "tables": [

        {### Estrutura de DiretóriosAWS_SECRET_ACCESS_KEY=sua_secret_key

            "name": "clientes",

            "pk": "idCliente",AWS_REGION=us-east-1

            "date_field": "DtAtualizacao",

            "sep": ";"``````

        }

    ]cdc-kaggle/

}

```├── data/4. Configure o arquivo `config.json` com suas preferências:



### 5. Execute o Pipeline│   ├── actual/         # Dados atuais baixados```json



```bash│   ├── last/           # Snapshot anterior (para CDC){

python main.py

```│   └── cdc/            # Arquivos CDC gerados    "dataset_name": "teocalvo/teomewhy-loyalty-system",



**Para instruções detalhadas de instalação e configuração, consulte o [Guia de Setup](docs/SETUP.md).**├── docs/               # Documentação adicional    "aws": {



---├── main.py             # Pipeline principal        "bucket": "meudatalake-raw",



## 💡 Exemplos de Uso├── config.json         # Configurações do pipeline        "prefix": "upcell",



### Estrutura CDC Gerada├── requirements.txt    # Dependências Python        "region": "us-east-1"



```├── start_pipeline.bat  # Script de inicialização    },

data/cdc/

├── clientes_20251004_095645.parquet└── .env               # Credenciais (não versionado)    "timer": {

├── produtos_20251004_095646.parquet

└── transacoes_20251004_095647.parquet```        "unit": "hours",

```

        "value": 6

### Estrutura no S3

---    },

```

s3://seu-bucket/    "tables": [...]

└── seu-prefixo/

    ├── full-load/## 🛠️ Tecnologias Utilizadas}

    │   ├── clientes.parquet

    │   ├── produtos.parquet```

    │   └── transacoes.parquet

    └── cdc/| Categoria | Tecnologias |

        ├── clientes_20251004_095645.parquet

        ├── produtos_20251004_095646.parquet|-----------|-------------|## 🚀 Uso

        └── transacoes_20251004_095647.parquet

```| **Linguagem** | Python 3.8+ |



### Logs do Sistema| **Data Processing** | Pandas, PyArrow (Parquet) |### Modo Agendado (Loop Contínuo)



```| **Cloud** | AWS S3, Boto3 |

2025-10-04 09:56:43 - INFO - Iniciando pipeline CDC

2025-10-04 09:56:45 - INFO - Dataset baixado com sucesso| **APIs** | Kaggle API |Executa o pipeline continuamente com o intervalo configurado:

2025-10-04 09:56:47 - INFO - CDC detectado: 15 inserções, 3 atualizações, 0 deleções

2025-10-04 09:56:50 - INFO - Upload para S3 concluído| **Automação** | Schedule, Windows Task Scheduler |

```

| **Ambiente** | python-dotenv, logging |```bash

---

python main.py

## 🎓 Conceitos Implementados

---```

### Change Data Capture (CDC)



O sistema implementa CDC através de:

## 📋 Pré-requisitos### Modo Execução Única

1. **Snapshot Comparison**: Compara estado atual vs. anterior

2. **Primary Key Tracking**: Identifica registros únicos via PK

3. **Timestamp Detection**: Detecta atualizações via campos de data

4. **Operation Types**: Classifica mudanças como INSERT/UPDATE/DELETE### SoftwareExecuta o pipeline apenas uma vez:



### Otimizações- Python 3.8 ou superior



- **Formato Parquet**: Reduz tamanho em ~70% vs. CSV- Conta Kaggle (com API Token)```bash

- **Compressão Snappy**: Balanço entre velocidade e tamanho

- **Batch Processing**: Processa múltiplas tabelas em paralelo- Conta AWS (com acesso ao S3)python main.py --once

- **Retry Logic**: Reexecuta operações em caso de falha

- Git```

---



## 📖 Documentação Completa

### Credenciais Necessárias### Pular Download (Para Testes)

- 📘 [**Guia de Setup**](docs/SETUP.md) - Instalação e configuração detalhada

- 🏗️ [**Arquitetura**](docs/ARCHITECTURE.md) - Detalhes técnicos e fluxo de dados

- ⏰ [**Agendamento**](docs/AGENDAMENTO.md) - Como configurar execuções automáticas

**Kaggle API**:Executa o pipeline usando dados já baixados localmente:

---

1. Acesse https://www.kaggle.com/settings

## 📁 Estrutura do Projeto

2. Clique em "Create New API Token"```bash

```

cdc-kaggle/3. Baixe o arquivo `kaggle.json`python main.py --once --skip-download

├── data/

│   ├── actual/         # Dados atuais baixados```

│   ├── last/           # Snapshot anterior (para CDC)

│   └── cdc/            # Arquivos CDC gerados**AWS S3**:

├── docs/               # Documentação adicional

│   ├── SETUP.md1. Acesse AWS IAM Console### Usar Arquivo de Configuração Customizado

│   ├── ARCHITECTURE.md

│   └── AGENDAMENTO.md2. Crie usuário com permissões S3

├── main.py             # Pipeline principal

├── config.json         # Configurações3. Gere Access Key ID e Secret Access Key```bash

├── requirements.txt    # Dependências

└── .env               # Credenciais (não versionado)python main.py --config minha_config.json

```

---```

---



## 📈 Melhorias Futuras

## 🚀 Como Usar## 📁 Estrutura de Diretórios

- [ ] Integração com Apache Airflow para orquestração

- [ ] Suporte a Delta Lake para ACID transactions

- [ ] Dashboard de monitoramento com Grafana

- [ ] Testes unitários e de integração### 1. Clone o Repositório```

- [ ] CI/CD com GitHub Actions

- [ ] Suporte a múltiplas fontes de dadoscdc-kaggle/

- [ ] Notificações via SNS/Email

- [ ] Métricas de qualidade de dados```bash├── main.py              # Script principal



---git clone https://github.com/TeoMeWhy/cdc-kaggle.git├── config.json          # Configurações



## 👤 Autorcd cdc-kaggle├── .env                 # Credenciais (não commitar!)



**Tiago Mendes (TeoMeWhy)**```├── requirements.txt     # Dependências Python



- 💼 LinkedIn: [linkedin.com/in/seu-perfil](https://linkedin.com/in/seu-perfil)├── cdc_pipeline.log     # Log de execução

- 🐙 GitHub: [@TeoMeWhy](https://github.com/TeoMeWhy)

- 📧 Email: contato@exemplo.com### 2. Instale as Dependências└── data/



---    ├── actual/          # Snapshot atual (após download)



## 📄 Licença```bash    ├── last/            # Snapshot anterior (referência)



Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.# Crie um ambiente virtual (recomendado)    └── cdc/             # Arquivos CDC gerados



---python -m venv .venv```



## 🙏 Agradecimentos.venv\Scripts\activate  # Windows



- Comunidade Kaggle pelos datasets públicos## 🗂️ Estrutura no S3

- AWS Free Tier para testes

- Comunidade Python pela excelente documentação# Instale as dependências



---pip install -r requirements.txtOs arquivos são organizados da seguinte forma:



<div align="center">```



**⭐ Se este projeto foi útil para você, considere dar uma estrela!**```



**📧 Aberto a oportunidades de trabalho em Engenharia de Dados**### 3. Configure as Credenciaiss3://meudatalake-raw/upcell/



</div>├── full-load/


Crie um arquivo `.env` na raiz do projeto:│   ├── clientes/

│   │   └── clientes.parquet

```env│   ├── produtos/

# Kaggle API│   │   └── produtos.parquet

KAGGLE_USERNAME=seu_usuario│   ├── transacoes/

KAGGLE_KEY=sua_chave_api│   │   └── transacoes.parquet

│   └── transacao_produto/

# AWS Credentials│       └── transacao_produto.parquet

AWS_ACCESS_KEY_ID=sua_access_key└── cdc/

AWS_SECRET_ACCESS_KEY=sua_secret_key    ├── clientes/

AWS_REGION=us-east-1    │   └── clientes_20251002_143025.parquet

```    ├── produtos/

    │   └── produtos_20251002_143025.parquet

### 4. Configure o Pipeline    ├── transacoes/

    │   └── transacoes_20251002_143025.parquet

Edite o arquivo `config.json`:    └── transacao_produto/

        └── transacao_produto_20251002_143025.parquet

```json```

{

    "dataset_name": "teocalvo/teomewhy-loyalty-system",## 🔄 Fluxo do Pipeline

    "aws": {

        "bucket": "seu-bucket-s3",1. **Download**: Baixa o dataset do Kaggle e descompacta em `./data/actual/`

        "prefix": "seu-prefixo",2. **Full-load**: 

        "region": "us-east-1"   - Lê arquivos CSV

    },   - Converte para Parquet

    "timer": {   - Faz upload para `s3://bucket/prefix/full-load/`

        "unit": "hours",3. **CDC**:

        "value": 6   - Compara snapshot atual com anterior

    },   - Identifica inserções (op='I'), atualizações (op='U') e deleções (op='D')

    "tables": [   - Salva em Parquet com timestamp

        {   - Faz upload para `s3://bucket/prefix/cdc/`

            "name": "clientes",4. **Pós-processamento**: Move arquivos de `actual/` para `last/` para próximo ciclo

            "pk": "idCliente",

            "date_field": "DtAtualizacao",## 📊 Operações de CDC

            "sep": ";"

        }| Operação | Código | Descrição |

    ]|----------|--------|-----------|

}| Inserção | `I` | Registros presentes no snapshot atual mas não no anterior |

```| Atualização | `U` | Registros com PK igual e campo de data maior no snapshot atual |

| Deleção | `D` | Registros presentes no snapshot anterior mas não no atual |

### 5. Execute o Pipeline

## 🔧 Configuração das Tabelas

```bash

# Execução únicaNo `config.json`, configure cada tabela com:

python main.py

- `name`: Nome da tabela (e do arquivo CSV)

# Ou use o script de inicialização- `sep`: Separador usado no CSV (ex: `;`, `,`)

start_pipeline.bat- `pk`: Nome da coluna de chave primária

```- `date_field`: Campo usado para detectar atualizações



### 6. (Opcional) Configure AgendamentoExemplo:



Veja a documentação em [`docs/AGENDAMENTO.md`](docs/AGENDAMENTO.md) para configurar execuções automáticas no Windows Task Scheduler.```json

{

---    "sep": ";",

    "name": "clientes",

## 📊 Exemplos de Uso    "date_field": "DtAtualizacao",

    "pk": "IdCliente"

### Estrutura CDC Gerada}

```

```

data/cdc/## 📝 Logs

├── clientes_20251004_095645.parquet

├── produtos_20251004_095646.parquetOs logs são salvos em dois locais:

└── transacoes_20251004_095647.parquet- **Console** (stdout): Logs em tempo real

```- **Arquivo** (`cdc_pipeline.log`): Histórico completo com encoding UTF-8



### Estrutura no S3Níveis de log:

- `INFO`: Operações principais

```- `WARNING`: Avisos (ex: arquivo não encontrado)

s3://seu-bucket/- `ERROR`: Erros com traceback completo

└── seu-prefixo/- `DEBUG`: Informações detalhadas (ativável alterando `logging.INFO` para `logging.DEBUG`)

    ├── full-load/

    │   ├── clientes.parquet## 🛡️ Tratamento de Erros

    │   ├── produtos.parquet

    │   └── transacoes.parquetO sistema possui tratamento robusto de erros:

    └── cdc/

        ├── clientes_20251004_095645.parquet- **Download falha**: Pipeline interrompido, erro registrado

        ├── produtos_20251004_095646.parquet- **Upload S3 falha**: Erro registrado, continua com próximas tabelas

        └── transacoes_20251004_095647.parquet- **Snapshot anterior ausente**: Considera todas as linhas como inserções

```- **Erro em iteração agendada**: Aguarda próximo ciclo automaticamente



### Logs do Sistema## 🔐 Segurança



```⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` com credenciais!

2025-10-04 09:56:43 - INFO - Iniciando pipeline CDC

2025-10-04 09:56:45 - INFO - Dataset baixado com sucessoAdicione ao `.gitignore`:

2025-10-04 09:56:47 - INFO - CDC detectado: 15 inserções, 3 atualizações, 0 deleções```

2025-10-04 09:56:50 - INFO - Upload para S3 concluído.env

```*.log

data/

---```



## 🎓 Conceitos Implementados## 📖 Exemplos de Uso



### Change Data Capture (CDC)### Executar uma vez e verificar logs

```bash

O sistema implementa CDC através de:python main.py --once

tail -f cdc_pipeline.log

1. **Snapshot Comparison**: Compara estado atual vs. anterior```

2. **Primary Key Tracking**: Identifica registros únicos via PK

3. **Timestamp Detection**: Detecta atualizações via campos de data### Testar com dados locais

4. **Operation Types**: Classifica mudanças como INSERT/UPDATE/DELETE```bash

python main.py --once --skip-download

### Otimizações```



- **Formato Parquet**: Reduz tamanho em ~70% vs. CSV### Executar em background (Linux/Mac)

- **Compressão Snappy**: Balanço entre velocidade e tamanho```bash

- **Batch Processing**: Processa múltiplas tabelas em paralelonohup python main.py > output.log 2>&1 &

- **Retry Logic**: Reexecuta operações em caso de falha```



---### Executar em background (Windows PowerShell)

```powershell

## 📈 Melhorias FuturasStart-Process python -ArgumentList "main.py" -WindowStyle Hidden

```

- [ ] Integração com Apache Airflow para orquestração

- [ ] Suporte a Delta Lake para ACID transactions## 🤝 Contribuindo

- [ ] Dashboard de monitoramento com Grafana

- [ ] Testes unitários e de integraçãoContribuições são bem-vindas! Sinta-se à vontade para:

- [ ] CI/CD com GitHub Actions

- [ ] Suporte a múltiplas fontes de dados1. Fazer fork do projeto

- [ ] Notificações via SNS/Email2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)

- [ ] Métricas de qualidade de dados3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)

4. Push para a branch (`git push origin feature/MinhaFeature`)

---5. Abrir um Pull Request



## 📖 Documentação Adicional## 📄 Licença



- [**Instruções de Agendamento**](docs/AGENDAMENTO.md) - Como configurar execuções automáticasEste projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.



---## 👨‍💻 Autor



## 👤 Autor**TeoMeWhy**

- GitHub: [@TeoMeWhy](https://github.com/TeoMeWhy)

**Tiago (TeoMeWhy)**- Kaggle: [teocalvo](https://www.kaggle.com/teocalvo)



- GitHub: [@TeoMeWhy](https://github.com/TeoMeWhy)## 🙏 Agradecimentos

- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)

- Kaggle pela API de datasets

---- AWS pela infraestrutura S3

- Comunidade Python por bibliotecas incríveis

## 📄 Licença

---

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

**Desenvolvido com ❤️ e GitHub Copilot**

---

## 🙏 Agradecimentos

- Comunidade Kaggle pelos datasets
- AWS Free Tier para testes
- Comunidade Python pela excelente documentação

---

<div align="center">

**⭐ Se este projeto foi útil, considere dar uma estrela!**

</div>
