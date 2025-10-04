# Script PowerShell para criar tarefa agendada automaticamente
# Execute como Administrador

$taskName = "CDC-Pipeline-Kaggle"
$scriptPath = "C:\Users\tiago\Documentos\GitHub\cdc-kaggle\start_pipeline.bat"
$workingDir = "C:\Users\tiago\Documentos\GitHub\cdc-kaggle"

# Remove tarefa existente se houver
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Cria ação
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory $workingDir

# Cria gatilho
$trigger = New-ScheduledTaskTrigger -AtStartup

# Configurações
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 0) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 10)

# Principal
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest

# Registra a tarefa
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Pipeline CDC automatico"

Write-Host "Tarefa criada com sucesso!" -ForegroundColor Green
Write-Host "Nome: $taskName" -ForegroundColor Cyan
