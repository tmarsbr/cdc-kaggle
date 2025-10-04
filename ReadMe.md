# Sistema de CDC (Change Data Capture) - Kaggle para S3# CDC com dados do Kaggle



Sistema completo de **Change Data Capture** que automatiza o download de datasets do Kaggle, processa snapshots em formato Parquet e envia para um data lake no AWS S3.## Sobre



## 📋 CaracterísticasAutomação para baixar dados do Kaggle e criar arquivos de CDC (Change Data Capture) comparando as duas últimas versões.



- ✅ Download automatizado de datasets do KaggleOs arquivos de CDC estarão disponíveis no diretório `./data/cdc/` no seguinte formato: `{tabela}_YYYMMDD_HHMMSS.csv`

- ✅ Conversão de CSV para Parquet

- ✅ Upload de full-load para S3## Setup

- ✅ Detecção de CDC (inserções, atualizações e deleções)

- ✅ Logging estruturado com timestamps### Instalando dependências

- ✅ Tratamento robusto de erros

- ✅ Suporte a execução única ou agendadaSugirimos criar um ambiente virtual apropriado para execução do programa. Após isso, pode instalar as depedências usando `pip`:

- ✅ Configuração via JSON e variáveis de ambiente

```bash

## 🛠️ Requisitospip install -r requirements.txt

```

- Python 3.8+

- Conta Kaggle com credenciais de APIPara garantir que a execução funciona corretamente, as seguintes variáveis ambientes devem estar configuradas:

- Credenciais AWS com permissões no S3

- Bucket S3 criado```bash

KAGGLE_USERNAME=

## 📦 InstalaçãoKAGGLE_KEY=

```

1. Clone o repositório:

```bashCaso tenha interesse em alterar a periodicidade de atualização da carga, altere o valor da variável `timer` em `config.json`.

git clone https://github.com/TeoMeWhy/cdc-kaggle.git

cd cdc-kaggle## Execução

```

```bash

2. Instale as dependências:python main.py

```bash```
pip install -r requirements.txt
```

3. Configure as credenciais no arquivo `.env`:
```env
# Credenciais Kaggle
KAGGLE_USERNAME=seu_usuario
KAGGLE_KEY=sua_chave_api

# Credenciais AWS
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_REGION=us-east-1
```

4. Configure o arquivo `config.json` com suas preferências:
```json
{
    "dataset_name": "teocalvo/teomewhy-loyalty-system",
    "aws": {
        "bucket": "meudatalake-raw",
        "prefix": "upcell",
        "region": "us-east-1"
    },
    "timer": {
        "unit": "hours",
        "value": 6
    },
    "tables": [...]
}
```

## 🚀 Uso

### Modo Agendado (Loop Contínuo)

Executa o pipeline continuamente com o intervalo configurado:

```bash
python main.py
```

### Modo Execução Única

Executa o pipeline apenas uma vez:

```bash
python main.py --once
```

### Pular Download (Para Testes)

Executa o pipeline usando dados já baixados localmente:

```bash
python main.py --once --skip-download
```

### Usar Arquivo de Configuração Customizado

```bash
python main.py --config minha_config.json
```

## 📁 Estrutura de Diretórios

```
cdc-kaggle/
├── main.py              # Script principal
├── config.json          # Configurações
├── .env                 # Credenciais (não commitar!)
├── requirements.txt     # Dependências Python
├── cdc_pipeline.log     # Log de execução
└── data/
    ├── actual/          # Snapshot atual (após download)
    ├── last/            # Snapshot anterior (referência)
    └── cdc/             # Arquivos CDC gerados
```

## 🗂️ Estrutura no S3

Os arquivos são organizados da seguinte forma:

```
s3://meudatalake-raw/upcell/
├── full-load/
│   ├── clientes/
│   │   └── clientes.parquet
│   ├── produtos/
│   │   └── produtos.parquet
│   ├── transacoes/
│   │   └── transacoes.parquet
│   └── transacao_produto/
│       └── transacao_produto.parquet
└── cdc/
    ├── clientes/
    │   └── clientes_20251002_143025.parquet
    ├── produtos/
    │   └── produtos_20251002_143025.parquet
    ├── transacoes/
    │   └── transacoes_20251002_143025.parquet
    └── transacao_produto/
        └── transacao_produto_20251002_143025.parquet
```

## 🔄 Fluxo do Pipeline

1. **Download**: Baixa o dataset do Kaggle e descompacta em `./data/actual/`
2. **Full-load**: 
   - Lê arquivos CSV
   - Converte para Parquet
   - Faz upload para `s3://bucket/prefix/full-load/`
3. **CDC**:
   - Compara snapshot atual com anterior
   - Identifica inserções (op='I'), atualizações (op='U') e deleções (op='D')
   - Salva em Parquet com timestamp
   - Faz upload para `s3://bucket/prefix/cdc/`
4. **Pós-processamento**: Move arquivos de `actual/` para `last/` para próximo ciclo

## 📊 Operações de CDC

| Operação | Código | Descrição |
|----------|--------|-----------|
| Inserção | `I` | Registros presentes no snapshot atual mas não no anterior |
| Atualização | `U` | Registros com PK igual e campo de data maior no snapshot atual |
| Deleção | `D` | Registros presentes no snapshot anterior mas não no atual |

## 🔧 Configuração das Tabelas

No `config.json`, configure cada tabela com:

- `name`: Nome da tabela (e do arquivo CSV)
- `sep`: Separador usado no CSV (ex: `;`, `,`)
- `pk`: Nome da coluna de chave primária
- `date_field`: Campo usado para detectar atualizações

Exemplo:

```json
{
    "sep": ";",
    "name": "clientes",
    "date_field": "DtAtualizacao",
    "pk": "IdCliente"
}
```

## 📝 Logs

Os logs são salvos em dois locais:
- **Console** (stdout): Logs em tempo real
- **Arquivo** (`cdc_pipeline.log`): Histórico completo com encoding UTF-8

Níveis de log:
- `INFO`: Operações principais
- `WARNING`: Avisos (ex: arquivo não encontrado)
- `ERROR`: Erros com traceback completo
- `DEBUG`: Informações detalhadas (ativável alterando `logging.INFO` para `logging.DEBUG`)

## 🛡️ Tratamento de Erros

O sistema possui tratamento robusto de erros:

- **Download falha**: Pipeline interrompido, erro registrado
- **Upload S3 falha**: Erro registrado, continua com próximas tabelas
- **Snapshot anterior ausente**: Considera todas as linhas como inserções
- **Erro em iteração agendada**: Aguarda próximo ciclo automaticamente

## 🔐 Segurança

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` com credenciais!

Adicione ao `.gitignore`:
```
.env
*.log
data/
```

## 📖 Exemplos de Uso

### Executar uma vez e verificar logs
```bash
python main.py --once
tail -f cdc_pipeline.log
```

### Testar com dados locais
```bash
python main.py --once --skip-download
```

### Executar em background (Linux/Mac)
```bash
nohup python main.py > output.log 2>&1 &
```

### Executar em background (Windows PowerShell)
```powershell
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**TeoMeWhy**
- GitHub: [@TeoMeWhy](https://github.com/TeoMeWhy)
- Kaggle: [teocalvo](https://www.kaggle.com/teocalvo)

## 🙏 Agradecimentos

- Kaggle pela API de datasets
- AWS pela infraestrutura S3
- Comunidade Python por bibliotecas incríveis

---

**Desenvolvido com ❤️ e GitHub Copilot**
