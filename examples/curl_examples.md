# Ejemplos de CURL para Sistema de Votación

## Configuración
```bash
BASE_URL="http://127.0.0.1:8000/api/users"
CONTENT_TYPE="Content-Type: application/json"
```

## 1. Dashboard de Votación
```bash
curl -X GET "$BASE_URL/voting/dashboard/" \
  -H "$CONTENT_TYPE"
```

## 2. Listar Consultas Populares
```bash
curl -X GET "$BASE_URL/voting/consultations/" \
  -H "$CONTENT_TYPE"
```

## 3. Crear Consulta Popular
```bash
curl -X POST "$BASE_URL/voting/consultations/create/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "title": "Consulta Popular Ejemplo",
    "description": "Esta es una consulta de ejemplo para demostrar el sistema de votación. Permite a los ciudadanos elegir entre diferentes opciones de presupuesto participativo.",
    "start_date": "2026-03-11T12:00:00Z",
    "end_date": "2026-03-18T12:00:00Z",
    "min_votes": 3
  }'
```

## 4. Obtener Detalle de Consulta
```bash
# Reemplazar UUID con el ID real
CONSULTATION_ID="uuid-de-la-consulta"

curl -X GET "$BASE_URL/voting/consultations/$CONSULTATION_ID/" \
  -H "$CONTENT_TYPE"
```

## 5. Otorgar Permiso de Votación
```bash
CONSULTATION_ID="uuid-de-la-consulta"
USER_ID="demo-user-1"

curl -X POST "$BASE_URL/voting/consultations/$CONSULTATION_ID/permissions/" \
  -H "$CONTENT_TYPE" \
  -d '{
    "user_id": "'$USER_ID'",
    "can_vote": true
  }'
```

## 6. Verificar Elegibilidad para Votar
```bash
CONSULTATION_ID="uuid-de-la-consulta"

curl -X GET "$BASE_URL/voting/consultations/$CONSULTATION_ID/eligibility/" \
  -H "$CONTENT_TYPE" \
  -H "Authorization: Bearer tu-token-de-acceso"
```

## 7. Votar en Consulta
```bash
CONSULTATION_ID="uuid-de-la-consulta"
OPTION_ID="uuid-de-la-opcion"

curl -X POST "$BASE_URL/voting/consultations/$CONSULTATION_ID/vote/" \
  -H "$CONTENT_TYPE" \
  -H "Authorization: Bearer tu-token-de-acceso" \
  -d '{
    "option_id": "'$OPTION_ID'"
  }'
```

## 8. Obtener Resultados
```bash
CONSULTATION_ID="uuid-de-la-consulta"

curl -X GET "$BASE_URL/voting/consultations/$CONSULTATION_ID/results/" \
  -H "$CONTENT_TYPE"
```

## 9. Historial de Votos del Usuario
```bash
curl -X GET "$BASE_URL/voting/history/" \
  -H "$CONTENT_TYPE" \
  -H "Authorization: Bearer tu-token-de-acceso"
```

## Ejemplo Completo con PowerShell

```powershell
# Configuración
$BASE_URL = "http://127.0.0.1:8000/api/users"
$HEADERS = @{
    "Content-Type" = "application/json"
}

# 1. Crear consulta
$consultaData = @{
    title = "Consulta PowerShell"
    description = "Ejemplo de consulta creada desde PowerShell"
    start_date = "2026-03-11T12:00:00Z"
    end_date = "2026-03-18T12:00:00Z"
    min_votes = 2
}

$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/create/" -Method POST -Headers $HEADERS -Body ($consultaData | ConvertTo-Json)
$response | ConvertTo-Json -Depth 10

# 2. Obtener ID de la consulta
$CONSULTATION_ID = $response.data.id

# 3. Obtener detalle
$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/$CONSULTATION_ID/" -Method GET -Headers $HEADERS
$response | ConvertTo-Json -Depth 10

# 4. Otorgar permiso
$permissionData = @{
    user_id = "demo-user-1"
    can_vote = $true
}

$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/$CONSULTATION_ID/permissions/" -Method POST -Headers $HEADERS -Body ($permissionData | ConvertTo-Json)
$response | ConvertTo-Json -Depth 10

# 5. Verificar elegibilidad
$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/$CONSULTATION_ID/eligibility/" -Method GET -Headers $HEADERS
$response | ConvertTo-Json -Depth 10

# 6. Votar (necesitarás obtener un option_id válido primero)
$voteData = @{
    option_id = "uuid-opcion-ejemplo"
}

$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/$CONSULTATION_ID/vote/" -Method POST -Headers $HEADERS -Body ($voteData | ConvertTo-Json)
$response | ConvertTo-Json -Depth 10

# 7. Obtener resultados
$response = Invoke-RestMethod -Uri "$BASE_URL/voting/consultations/$CONSULTATION_ID/results/" -Method GET -Headers $HEADERS
$response | ConvertTo-Json -Depth 10
```

## Flujo de Ejemplo Rápido

```bash
# Paso 1: Crear consulta
echo "🚀 Creando consulta..."
RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/api/users/voting/consultations/create/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Consulta Rápida",
    "description": "Descripción de la consulta rápida para demostración",
    "start_date": "2026-03-11T12:00:00Z",
    "end_date": "2026-03-12T12:00:00Z",
    "min_votes": 1
  }')

CONSULTATION_ID=$(echo $RESPONSE | jq -r '.data.id')
echo "✅ Consulta creada: $CONSULTATION_ID"

# Paso 2: Obtener opciones
echo "📋 Obteniendo opciones..."
RESPONSE=$(curl -s -X GET "http://127.0.0.1:8000/api/users/voting/consultations/$CONSULTATION_ID/" \
  -H "Content-Type: application/json")

# Extraer el primer option_id (necesitarás jq instalado)
OPTION_ID=$(echo $RESPONSE | jq -r '.data.options[0].id')
echo "✅ Opción seleccionada: $OPTION_ID"

# Paso 3: Otorgar permiso
echo "🔓 Otorgando permiso..."
curl -s -X POST "http://127.0.0.1:8000/api/users/voting/consultations/$CONSULTATION_ID/permissions/" \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"demo-user-1\",
    \"can_vote\": true
  }"

# Paso 4: Votar
echo "🗳 Registrando voto..."
curl -s -X POST "http://127.0.0.1:8000/api/users/voting/consultations/$CONSULTATION_ID/vote/" \
  -H "Content-Type: application/json" \
  -d "{
    \"option_id\": \"$OPTION_ID\"
  }"

# Paso 5: Obtener resultados
echo "📊 Obteniendo resultados..."
curl -s -X GET "http://127.0.0.1:8000/api/users/voting/consultations/$CONSULTATION_ID/results/" \
  -H "Content-Type: application/json" | jq .
```

## Notas Importantes

1. **Reemplaza los UUID** con los IDs reales que obtengas de las respuestas
2. **Modo Demo**: El sistema funciona en modo demo sin Supabase
3. **Autenticación**: Para endpoints protegidos, necesitarás un token JWT válido
4. **Fechas**: Usan formato ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
5. **Permisos**: Los usuarios necesitan ser miembros de partido y tener permiso explícito

## Errores Comunes y Soluciones

### 404 Not Found
- **Causa**: URL incorrecta o UUID no válido
- **Solución**: Verifica que el servidor esté corriendo y los IDs sean correctos

### 400 Bad Request
- **Causa**: Datos inválidos o faltantes
- **Solución**: Revisa el formato JSON y los campos requeridos

### 401 Unauthorized
- **Causa**: Token inválido o no proporcionado
- **Solución**: Inicia sesión y usa el token en headers

### 403 Forbidden
- **Causa**: No tienes permiso para votar
- **Solución**: Verifica elegibilidad y solicita permiso

### 500 Internal Server Error
- **Causa**: Error interno del servidor
- **Solución**: Revisa los logs del servidor
