# CDC com dados do Kaggle

## Sobre

Automação para baixar dados do Kaggle e criar arquivos de CDC (Change Data Capture) comparando as duas últimas versões.

Os arquivos de CDC estarão disponíveis no diretório `./data/cdc/` no seguinte formato: `{tabela}_YYYMMDD_HHMMSS.csv`

## Setup

### Instalando dependências

Sugirimos criar um ambiente virtual apropriado para execução do programa. Após isso, pode instalar as depedências usando `pip`:

```bash
pip install -r requirements.txt
```

Para garantir que a execução funciona corretamente, as seguintes variáveis ambientes devem estar configuradas:

```bash
KAGGLE_USERNAME=
KAGGLE_KEY=
```

Caso tenha interesse em alterar a periodicidade de atualização da carga, altere o valor da variável `timer` em `config.json`.

## Execução

```bash
python main.py
```