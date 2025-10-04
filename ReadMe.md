# Pipeline de Ingestão CDC - Kaggle para AWS S3

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.0-green.svg)](https://pandas.pydata.org/)

> **Parte 1/2:** Pipeline de ingestão automatizada com Change Data Capture (CDC) para camada RAW de um Data Lake

---

## 📖 Contexto do Projeto

Este projeto é a **primeira etapa** de uma arquitetura completa de Data Lake/Lakehouse. Aqui, focamos na **ingestão e geração de dados CDC** que alimentam a camada RAW do data lake.

### 🔗 Jornada Completa do Dado

```
┌─────────────────────────────────────────────────────────────┐
│ PARTE 1 (Este Projeto) - Ingestão RAW                       │
│ Kaggle → Python CDC → AWS S3 (Parquet)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│ PARTE 2 - Data Lake/Lakehouse                               │
│ RAW → BRONZE (Delta + Streaming) → SILVER (CDF) → GOLD      │
│ 🔗 github.com/tmarsbr/meu-lago-mago                         │
└─────────────────────────────────────────────────────────────┘
```

**Parte 2** ([Meu Lago Mago](https://github.com/tmarsbr/meu-lago-mago)): Constrói um Data Lake/Lakehouse completo consumindo os dados gerados aqui, utilizando:
- **BRONZE**: Streaming com UPSERT em Delta Lake
- **SILVER**: Change Data Feed (CDF) para transformações
- **GOLD**: Cubos OLAP para dashboards e análises

---

## 🎯 Objetivo

Automatizar a **extração incremental de dados** (Full-Load + CDC) do Kaggle para um bucket S3, gerando arquivos Parquet otimizados que servirão como fonte para pipelines de dados downstream.

### O Problema Resolvido

Em ambientes de produção, dados transacionais mudam constantemente. Reprocessar datasets completos (full-load) a cada execução é ineficiente. Este pipeline:

1. **Detecta mudanças** (inserções, atualizações, deleções)
2. **Gera arquivos CDC incrementais** em Parquet
3. **Armazena no S3** com estrutura organizada
4. **Reduz custos** (~70% menos armazenamento vs. CSV)

---

## 🏗️ Arquitetura

```
┌──────────┐    Download    ┌───────────┐    Transform    ┌──────────┐
│  Kaggle  │───────────────▶│  Pipeline │────────────────▶│  AWS S3  │
│ Dataset  │     (API)      │  (Python) │   (Parquet)     │   RAW    │
└──────────┘                └─────┬─────┘                 └──────────┘
                                  │
                                  │ CDC Detection
                                  ▼
                          ┌───────────────┐
                          │ Snapshot      │
                          │ Comparison    │
                          │ (Last/Actual) │
                          └───────────────┘
```

### Fluxo de Dados

1. **Extract**: Download dataset via Kaggle API
2. **Transform**: Conversão CSV → Parquet + Detecção CDC
3. **Load**: Upload para S3 (full-load + CDC incremental)
4. **Repeat**: Agendamento automático para execuções periódicas

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Propósito |
|------------|------------|-----------|
| **Fonte de Dados** | Kaggle API | Download de datasets públicos |
| **Processamento** | Python + Pandas | ETL e detecção de CDC |
| **Formato** | Parquet (Snappy) | Armazenamento colunar otimizado |
| **Storage** | AWS S3 | Data Lake (camada RAW) |
| **Orquestração** | Python Schedule | Execuções automatizadas |

---

## 🚀 Quick Start

### 1. Configuração

```bash
# Clone e instale
git clone https://github.com/TeoMeWhy/cdc-kaggle.git
cd cdc-kaggle
pip install -r requirements.txt

# Configure credenciais (.env)
KAGGLE_USERNAME=seu_usuario
KAGGLE_KEY=sua_api_key
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
```

### 2. Execução

```bash
# Execução única
python main.py

# Modo agendado (loop contínuo)
python main.py --schedule
```

### 3. Resultado

```
s3://seu-bucket/prefix/
├── full-load/
│   ├── clientes.parquet
│   ├── produtos.parquet
│   └── transacoes.parquet
└── cdc/
    ├── clientes_20251004_120000.parquet
    ├── produtos_20251004_120001.parquet
    └── transacoes_20251004_120002.parquet
```

---

## 📊 Change Data Capture (CDC)

### Operações Detectadas

| Operação | Código | Lógica |
|----------|--------|--------|
| **INSERT** | `I` | Registros presentes apenas no snapshot atual |
| **UPDATE** | `U` | Registros com PK igual mas timestamp maior |
| **DELETE** | `D` | Registros presentes apenas no snapshot anterior |

### Estrutura do Arquivo CDC

```python
# Exemplo: clientes_20251004_120000.parquet
{
    "idCliente": 12345,
    "Nome": "João Silva",
    "Email": "joao@email.com",
    "DtAtualizacao": "2025-10-04 12:00:00",
    "_cdc_operation": "U",          # I, U ou D
    "_cdc_timestamp": "2025-10-04 12:00:00"
}
```

---

## 📈 Benefícios Técnicos

### Performance
- ✅ **Redução de 70%** no tamanho dos arquivos (Parquet vs CSV)
- ✅ **Compressão Snappy**: balanço ideal entre velocidade e espaço
- ✅ **Processamento incremental**: apenas mudanças são transferidas

### Escalabilidade
- ✅ Suporte a múltiplas tabelas via configuração JSON
- ✅ Retry logic com exponential backoff
- ✅ Logging estruturado para troubleshooting

### Integração
- ✅ Compatível com Databricks/Spark (Parquet)
- ✅ Pronto para Delta Lake UPSERT operations
- ✅ Metadados CDC facilitam merge operations

---

## 📁 Documentação Técnica

- 📘 [**Setup Completo**](docs/SETUP.md) - Instalação e configuração detalhada
- 🏗️ [**Arquitetura**](docs/ARCHITECTURE.md) - Design técnico e decisões arquiteturais
- ⏰ [**Agendamento**](docs/AGENDAMENTO.md) - Automação via Task Scheduler

---

## 🔄 Roadmap

### ✅ Implementado (Parte 1)
- [x] Download automatizado Kaggle
- [x] Detecção de CDC (Insert/Update/Delete)
- [x] Conversão para Parquet otimizado
- [x] Upload para S3 (full-load + CDC)
- [x] Logging e tratamento de erros

### 🚧 Em Andamento (Parte 2)
- [ ] Lakehouse com Delta Lake ([ver projeto](https://github.com/tmarsbr/meu-lago-mago))
- [ ] Streaming com Structured Streaming
- [ ] UPSERT operations em BRONZE
- [ ] Change Data Feed (CDF) para SILVER
- [ ] Cubos OLAP em GOLD

---

## 👨‍💻 Autor

**Tiago Mendes**
- GitHub: [@TeoMeWhy](https://github.com/TeoMeWhy)
- LinkedIn: [Tiago Mendes](https://linkedin.com/in/seu-perfil)
- Kaggle: [@teocalvo](https://www.kaggle.com/teocalvo)

---

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

<div align="center">

**⭐ Se este projeto agregou valor, considere deixar uma estrela**

**Parte 1/2** | [Veja a Parte 2 →](https://github.com/tmarsbr/meu-lago-mago)

</div>
