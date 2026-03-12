# Ejemplo de PowerShell para Sistema de Votación
# Ejecutar: .\examples\powershell_example.ps1

# Configuración
$BASE_URL = "http://127.0.0.1:8000/api/users"
$HEADERS = @{
    "Content-Type" = "application/json"
}

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Data = $null
    )
    
    Write-Host "`n$('='*50)" -ForegroundColor Cyan
    Write-Host "Probando: $Name" -ForegroundColor Yellow
    Write-Host "URL: $Url" -ForegroundColor Gray
    
    try {
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $HEADERS
        } elseif ($Method -eq "POST") {
            $body = $Data | ConvertTo-Json -Depth 10
            $response = Invoke-RestMethod -Uri $Url -Method $Method -Headers $HEADERS -Body $body
        }
        
        Write-Host "Status: 200 (OK)" -ForegroundColor Green
        Write-Host "Response:" -ForegroundColor White
        $response | ConvertTo-Json -Depth 10 | Write-Host
        
        return $response
    }
    catch {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
            Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
            try {
                $errorBody = $_.Exception.Response.GetResponseStream() | 
                    [System.IO.StreamReader]::new().ReadToEnd() | 
                    ConvertFrom-Json
                $errorBody | ConvertTo-Json -Depth 10 | Write-Host
            } catch {
                Write-Host "No se pudo parsear el error" -ForegroundColor Gray
            }
        }
        return $null
    }
}

# Iniciar ejemplo
Write-Host "EJEMPLO DE SISTEMA DE VOTACION CON POWERSHELL" -ForegroundColor Magenta
Write-Host "Asegurate de que el servidor Django este corriendo en http://127.0.0.1:8000" -ForegroundColor Yellow

# 1. Probar Dashboard
Test-Endpoint "Dashboard de Votación" "$BASE_URL/voting/dashboard/"

# 2. Probar Listar Consultas
Test-Endpoint "Listar Consultas Populares" "$BASE_URL/voting/consultations/"

# 3. Crear Consulta Popular
Write-Host "`n$('='*50)" -ForegroundColor Cyan
Write-Host "CREANDO CONSULTA POPULAR" -ForegroundColor Yellow

$consultaData = @{
    title = "Consulta PowerShell Ejemplo"
    description = "Esta es una consulta de ejemplo creada desde PowerShell para demostrar el sistema de votación. Permite a los ciudadanos participar en decisiones importantes sobre el presupuesto municipal."
    start_date = (Get-Date).AddHours(1).ToString("yyyy-MM-ddTHH:mm:ssZ")
    end_date = (Get-Date).AddDays(7).ToString("yyyy-MM-ddTHH:mm:ssZ")
    min_votes = 2
}

$response = Test-Endpoint "Crear Consulta Popular" "$BASE_URL/voting/consultations/create/" -Method "POST" -Data $consultaData

# Extraer ID de la consulta
$consultationId = $null
if ($response -and $response.success) {
    $consultationId = $response.data.id
    Write-Host "Consulta ID: $consultationId" -ForegroundColor Green
}

# 4. Obtener detalle de la consulta
if ($consultationId) {
    Test-Endpoint "Detalle de Consulta" "$BASE_URL/voting/consultations/$consultationId/"
    
    # 5. Otorgar permiso a usuario
    $permissionData = @{
        user_id = "demo-user-1"
        can_vote = $true
    }
    
    Test-Endpoint "Otorgar Permiso" "$BASE_URL/voting/consultations/$consultationId/permissions/" -Method "POST" -Data $permissionData
    
    # 6. Verificar elegibilidad
    Test-Endpoint "Verificar Elegibilidad" "$BASE_URL/voting/consultations/$consultationId/eligibility/"
    
    # 7. Intentar votar (necesitaríamos un option_id válido)
    $voteData = @{
        option_id = "opcion-ejemplo"
    }
    
    Test-Endpoint "Intentar Votar" "$BASE_URL/voting/consultations/$consultationId/vote/" -Method "POST" -Data $voteData
    
    # 8. Obtener resultados
    Test-Endpoint "Resultados" "$BASE_URL/voting/consultations/$consultationId/results/"
}

# 9. Probar historial de votos
Test-Endpoint "Historial de Votos" "$BASE_URL/voting/history/"

Write-Host "`n$('='*50)" -ForegroundColor Cyan
Write-Host "PRUEBA COMPLETADA" -ForegroundColor Green
Write-Host "Los endpoints principales del sistema de votación han sido probados" -ForegroundColor White
Write-Host "Para más ejemplos, revisa:" -ForegroundColor Yellow
Write-Host "   - examples/voting_example.py (ejemplo completo)" -ForegroundColor Gray
Write-Host "   - examples/curl_examples.md (ejemplos con curl)" -ForegroundColor Gray
Write-Host "   - VOTING_API_GUIDE.md (documentación completa)" -ForegroundColor Gray
