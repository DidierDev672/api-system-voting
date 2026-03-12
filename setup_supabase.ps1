# Script para configurar Supabase con las tablas necesarias (PowerShell)
# Este script prepara todos los schemas SQL para ejecutar en Supabase

Write-Host "🚀 Configurando Supabase para el Sistema de Votación" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Verificar variables de entorno
$envPath = ".env"
if (-not (Test-Path $envPath)) {
    Write-Host "❌ Error: No se encuentra el archivo .env" -ForegroundColor Red
    exit 1
}

# Cargar variables de entorno
Get-Content $envPath | ForEach-Object {
    $line = $_.Trim()
    if ($line -and !$line.StartsWith('#')) {
        $key, $value = $line.Split('=', 2)
        [Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim())
    }
}

$supabaseUrl = $env:SUPABASE_URL
$serviceKey = $env:SUPABASE_SERVICE_ROLE_KEY

if ([string]::IsNullOrEmpty($supabaseUrl) -or [string]::IsNullOrEmpty($serviceKey)) {
    Write-Host "❌ Error: Las variables de entorno SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridas" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Variables de entorno verificadas" -ForegroundColor Green
Write-Host ""

# Directorio de schemas
$schemasDir = "supabase_integration/schemas"

# Lista de schemas en orden de ejecución
$schemas = @(
    "01_party_members.sql",
    "02_political_parties.sql", 
    "03_users.sql",
    "04_popular_consultations.sql",
    "05_functions_and_triggers.sql"
)

Write-Host "📋 Preparando schemas SQL para ejecutar:" -ForegroundColor Yellow
Write-Host ""

foreach ($schema in $schemas) {
    $schemaPath = Join-Path $schemasDir $schema
    
    if (Test-Path $schemaPath) {
        Write-Host "🔄 Preparando $schema..." -ForegroundColor Cyan
        Write-Host "📝 Abre el archivo: $schemaPath" -ForegroundColor White
        Write-Host "🌐 Ve a: https://pbesvbrclrmjarouyler.supabase.co" -ForegroundColor White
        Write-Host "📊 Ve a SQL Editor y copia el contenido del archivo" -ForegroundColor White
        Write-Host "✅ Ejecuta el SQL en Supabase Dashboard" -ForegroundColor Green
        Write-Host ""
        
        # Mostrar contenido del schema
        Write-Host "📄 Contenido de $schema:" -ForegroundColor Yellow
        Write-Host "----------------------------------------" -ForegroundColor Gray
        Get-Content $schemaPath | Write-Host
        Write-Host "----------------------------------------" -ForegroundColor Gray
        Write-Host ""
        
        Read-Host "Presiona Enter para continuar con el siguiente schema..."
    } else {
        Write-Host "❌ Error: No se encuentra el archivo $schema" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🎉 Todos los schemas han sido preparados!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. ✅ Todos los schemas ejecutados en Supabase" -ForegroundColor Green
Write-Host "2. 🧪 Prueba los endpoints de la API" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Endpoints disponibles:" -ForegroundColor Cyan
Write-Host "- POST http://127.0.0.1:8000/api/party-members/register/" -ForegroundColor White
Write-Host "- GET  http://127.0.0.1:8000/api/party-members/" -ForegroundColor White
Write-Host "- POST http://127.0.0.1:8000/api/political-parties/register/" -ForegroundColor White
Write-Host "- GET  http://127.0.0.1:8000/api/political-parties/" -ForegroundColor White
Write-Host ""
Write-Host "🎯 La API está lista para usar con Supabase!" -ForegroundColor Green
