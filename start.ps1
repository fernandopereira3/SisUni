$ErrorActionPreference = "Stop"

cd C:

Write-Host 'Verificando pasta SisUni' -ForegroundColor Yellow
if (Test-Path ".\SisUni") {
    Write-Host 'Atualizando Programa...' -ForegroundColor Yellow
    cd C:SisUni
    git pull origin main
}else {
    Write-Host 'Clonando repositorio' -ForegroundColor Yellow
    cd C:
    git clone git https://github.com/fernandopereira3/SisUni.git
}

cd C:
Write-Host 'Entrando na pasta SisUni' -ForegroundColor Yellow
cd C:SisUni

Write-Host "Inicializando ambiente..." -ForegroundColor Green

try {
    python --version | Out-Null
} catch {
    Write-Host "Python nao instalado ou nao está no PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".\Lib")) {
    Write-Host "Criando venv" -ForegroundColor Yellow
    python -m venv .venv
}

& .\.venv\Scripts\Activate.ps1

if (Test-Path ".\requirements.txt") {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "Iniciando aplicacao..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "C:SisUni\src\main.py" -WindowStyle Hidden
Clear-Host
Write-Host "Aplicao rodando em segundo plano, voce ja pode fechar esta janela." -ForegroundColor Green

if ($LASTEXITCODE -ne 0) {
    Write-Host "Application com erro $LASTEXITCODE" -ForegroundColor Red
    Write-Host "Aperte qualquer botao para sair" -ForegroundColor Red
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
