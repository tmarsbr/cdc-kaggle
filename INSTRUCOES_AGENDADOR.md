# 🕐 Como Agendar o Pipeline no Windows

## Opção 1: Agendador de Tarefas (Task Scheduler)

### Passo a passo:

1. **Abra o Agendador de Tarefas:**
   - Pressione `Win + R`
   - Digite: `taskschd.msc`
   - Pressione Enter

2. **Criar Nova Tarefa:**
   - Clique em **"Criar Tarefa Básica"** (lado direito)
   - Nome: `CDC Pipeline - Kaggle`
   - Descrição: `Pipeline automático de CDC para dataset Kaggle`
   - Clique em **Avançar**

3. **Configurar Gatilho (Quando executar):**
   - Escolha: **"Quando o computador iniciar"**
   - Clique em **Avançar**

4. **Configurar Ação:**
   - Escolha: **"Iniciar um programa"**
   - Clique em **Avançar**
   - **Programa/script:** `C:\Users\tiago\Documentos\GitHub\cdc-kaggle\start_pipeline.bat`
   - Clique em **Avançar**

5. **Finalizar:**
   - Marque: **"Abrir a caixa de diálogo Propriedades..."**
   - Clique em **Concluir**

6. **Configurações Avançadas:**
   - Aba **"Geral"**:
     - ✅ Marque: **"Executar estando o usuário conectado ou não"**
     - ✅ Marque: **"Executar com privilégios mais altos"**
   - Aba **"Configurações"**:
     - ✅ Marque: **"Se a tarefa falhar, reiniciar a cada"**: 10 minutos
     - ✅ Marque: **"Tentar reiniciar até"**: 3 vezes
     - ✅ Desmarque: **"Parar a tarefa se ela for executada por mais de"**
   - Clique em **OK**

7. **Digite sua senha do Windows** quando solicitado

---

## Opção 2: NSSM (Non-Sucking Service Manager)

Transforma o script Python em um **serviço do Windows** verdadeiro.

### Instalação:

```powershell
# 1. Baixar NSSM
# Acesse: https://nssm.cc/download
# Extraia para: C:\nssm

# 2. Instalar o serviço
cd C:\nssm\win64
.\nssm.exe install CDCPipeline "C:\Users\tiago\AppData\Local\Programs\Python\Python313\python.exe" "C:\Users\tiago\Documentos\GitHub\cdc-kaggle\main.py"

# 3. Configurar diretório de trabalho
.\nssm.exe set CDCPipeline AppDirectory "C:\Users\tiago\Documentos\GitHub\cdc-kaggle"

# 4. Configurar saída de logs
.\nssm.exe set CDCPipeline AppStdout "C:\Users\tiago\Documentos\GitHub\cdc-kaggle\nssm_output.log"
.\nssm.exe set CDCPipeline AppStderr "C:\Users\tiago\Documentos\GitHub\cdc-kaggle\nssm_error.log"

# 5. Iniciar o serviço
.\nssm.exe start CDCPipeline

# 6. Para parar o serviço
.\nssm.exe stop CDCPipeline

# 7. Para remover o serviço
.\nssm.exe remove CDCPipeline confirm
```

---

## Opção 3: Docker (Para servidores/produção)

Se você quiser rodar em um servidor ou container:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
# Build
docker build -t cdc-pipeline .

# Run
docker run -d --name cdc-pipeline --restart unless-stopped cdc-pipeline
```

---

## Opção 4: AWS Lambda + EventBridge (Cloud)

Para execução 100% automática na nuvem (sem depender do seu computador):

1. **Zipar o código**
2. **Criar função Lambda**
3. **Configurar EventBridge** para disparar a cada 6 horas
4. **Vantagens:**
   - ✅ Não precisa deixar computador ligado
   - ✅ Escalável
   - ✅ Integração nativa com S3

---

## ⚡ Qual escolher?

| Opção | Vantagem | Desvantagem |
|-------|----------|-------------|
| **Agendador de Tarefas** | Nativo do Windows, simples | Precisa deixar PC ligado |
| **NSSM** | Serviço verdadeiro, robusto | Requer instalação extra |
| **Docker** | Portável, isolado | Requer Docker instalado |
| **AWS Lambda** | Cloud, sem servidor | Requer configuração AWS |

---

## 📝 Status Atual

O pipeline já está rodando no modo agendado com o comando:
```powershell
python main.py
```

**Intervalo:** A cada 6 horas (21600 segundos)

**Para verificar se está rodando:**
```powershell
Get-Process python | Where-Object {$_.Path -like "*python*"}
```

**Para ver os logs:**
```powershell
Get-Content .\cdc_pipeline.log -Tail 20 -Wait
```
