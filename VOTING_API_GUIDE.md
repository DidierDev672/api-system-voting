# API de Sistema de Votación de Consultas Populares

## Overview

Esta API proporciona endpoints completos para la gestión de consultas populares de votación, con validaciones de permisos y restricciones de membresía en partidos políticos.

## Requisitos para Votar

Para que un usuario pueda votar en una consulta popular, debe cumplir con:

1. **Ser miembro de un partido político** activo
2. **Tener permiso explícito** para votar en la consulta específica
3. **No haber votado antes** en la misma consulta
4. **La consulta debe estar activa** (dentro del período de votación)

## Endpoints

### 1. Dashboard de Votación
```
GET /api/users/voting/dashboard/
```

**Response:**
```json
{
  "success": true,
  "message": "Dashboard obtenido exitosamente",
  "data": {
    "statistics": {
      "total_consultations": 10,
      "active_consultations": 3,
      "total_votes": 1250,
      "total_voters": 890
    },
    "recent_consultations": [...],
    "active_consultations": [...]
  }
}
```

### 2. Listar Consultas Populares
```
GET /api/users/voting/consultations/?status=ACTIVE&limit=50
```

**Parámetros:**
- `status` (opcional): ACTIVE, FINISHED, CANCELLED
- `limit` (opcional): Número máximo de resultados (default: 50)

**Response:**
```json
{
  "success": true,
  "message": "Consultas obtenidas exitosamente",
  "data": [
    {
      "id": "uuid-consulta",
      "title": "Consulta sobre presupuesto participativo",
      "description": "Decida cómo se distribuirá el presupuesto...",
      "status": "ACTIVE",
      "start_date": "2026-03-10T00:00:00Z",
      "end_date": "2026-03-17T23:59:59Z",
      "min_votes": 100,
      "total_votes": 45,
      "total_options": 4,
      "is_active": true,
      "created_at": "2026-03-10T12:00:00Z"
    }
  ],
  "count": 1
}
```

### 3. Crear Consulta Popular
```
POST /api/users/voting/consultations/create/
```

**Request Body:**
```json
{
  "title": "Nueva consulta popular",
  "description": "Descripción detallada de la consulta (mínimo 50 caracteres)",
  "start_date": "2026-03-10T00:00:00Z",
  "end_date": "2026-03-17T23:59:59Z", 
  "min_votes": 100
}
```

**Validaciones:**
- Título: Mínimo 10 caracteres, máximo 255
- Descripción: Mínimo 50 caracteres
- Fechas: Inicio debe ser futuro y anterior a fin
- Duración: Mínimo 24 horas, máximo 30 días
- Votos mínimos: Entre 1 y 10,000

### 4. Detalle de Consulta Popular
```
GET /api/users/voting/consultations/<uuid>/
```

**Response:**
```json
{
  "success": true,
  "message": "Consulta obtenida exitosamente",
  "data": {
    "consultation": {
      "id": "uuid-consulta",
      "title": "Consulta sobre presupuesto participativo",
      "status": "ACTIVE",
      "is_active": true,
      "is_finished": false
    },
    "options": [
      {
        "id": "uuid-opcion-1",
        "title": "Opción A",
        "description": "Descripción de la opción A",
        "order_index": 1,
        "votes_count": 15
      }
    ],
    "voting_stats": {
      "total_votes": 45,
      "unique_voters": 45,
      "total_options": 4,
      "permissions_granted": 120
    }
  }
}
```

### 5. Verificar Elegibilidad para Votar
```
GET /api/users/voting/consultations/<uuid>/eligibility/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "message": "Elegibilidad verificada",
  "data": {
    "user_id": "uuid-usuario",
    "consultation_id": "uuid-consulta",
    "is_eligible": true,
    "has_voted": false,
    "reasons": [],
    "is_party_member": true,
    "has_permission": true
  }
}
```

**Posibles razones de no elegibilidad:**
- "Ya ha votado en esta consulta"
- "No es miembro de partido político"
- "No tiene permiso de votación"
- "La consulta no está activa para votación"

### 6. Votar en Consulta Popular
```
POST /api/users/voting/consultations/<uuid>/vote/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "option_id": "uuid-opcion-seleccionada"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Voto registrado exitosamente",
  "data": {
    "vote_id": "uuid-voto",
    "consultation_id": "uuid-consulta",
    "option_id": "uuid-opcion",
    "voted_at": "2026-03-10T15:30:00Z"
  }
}
```

### 7. Resultados de Consulta Popular
```
GET /api/users/voting/consultations/<uuid>/results/
```

**Response:**
```json
{
  "success": true,
  "message": "Resultados obtenidos exitosamente",
  "data": {
    "consultation_id": "uuid-consulta",
    "consultation_title": "Consulta sobre presupuesto participativo",
    "total_votes": 45,
    "status": "FINISHED",
    "is_finished": true,
    "options": [
      {
        "option_id": "uuid-opcion-1",
        "title": "Opción A",
        "votes": 25,
        "percentage": 55.56
      },
      {
        "option_id": "uuid-opcion-2",
        "title": "Opción B",
        "votes": 20,
        "percentage": 44.44
      }
    ],
    "winner": {
      "option_id": "uuid-opcion-1",
      "title": "Opción A",
      "votes": 25,
      "percentage": 55.56
    }
  }
}
```

### 8. Gestionar Permisos de Votación
```
POST /api/users/voting/consultations/<uuid>/permissions/
DELETE /api/users/voting/consultations/<uuid>/permissions/<uuid>/
```

**Otorgar Permiso (POST):**
```json
{
  "user_id": "uuid-usuario",
  "can_vote": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Permiso otorgado exitosamente",
  "data": {
    "permission_id": "uuid-permiso",
    "user_id": "uuid-usuario",
    "consultation_id": "uuid-consulta",
    "can_vote": true,
    "granted_at": "2026-03-10T12:00:00Z"
  }
}
```

### 9. Historial de Votos del Usuario
```
GET /api/users/voting/history/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "success": true,
  "message": "Historial de votos obtenido exitosamente",
  "data": [
    {
      "vote_id": "uuid-voto",
      "consultation_id": "uuid-consulta",
      "consultation_title": "Consulta sobre presupuesto participativo",
      "option_id": "uuid-opcion",
      "option_title": "Opción A",
      "voted_at": "2026-03-10T15:30:00Z"
    }
  ],
  "count": 1
}
```

## Schema de Base de Datos Supabase

El sistema utiliza las siguientes tablas en Supabase:

### Tablas Principales

1. **popular_consultations**: Consultas populares
2. **voting_options**: Opciones de votación
3. **votes**: Votos registrados
4. **voting_permissions**: Permisos de votación

### Vistas Útiles

1. **active_consultations**: Consultas activas con estadísticas
2. **eligible_voters**: Usuarios elegibles para votar

### Funciones SQL

1. **can_user_vote()**: Verifica elegibilidad para votar
2. **get_consultation_results()**: Obtiene resultados con porcentajes

## Reglas de Negocio

### Validaciones de Votación

1. **Un voto por usuario**: Un usuario solo puede votar una vez por consulta
2. **Membresía requerida**: Solo miembros de partidos políticos pueden votar
3. **Permiso explícito**: Se requiere permiso específico por consulta
4. **Período activo**: Solo se puede votar durante el período definido

### Auto-finalización

Las consultas se finalizan automáticamente cuando:
- Se alcanza el mínimo de votos requerido
- La fecha de finalización expira

### Límites y Restricciones

- **Máximo 10 opciones** por consulta
- **Duración**: 24 horas mínimo, 30 días máximo
- **Votos mínimos**: 1 a 10,000 votos
- **Títulos**: 10 a 255 caracteres
- **Descripciones**: Mínimo 50 caracteres

## Configuración de Supabase

Para usar en producción, configurar en `settings.py`:

```python
SUPABASE_URL = 'https://tu-proyecto.supabase.co'
SUPABASE_ANON_KEY = 'tu-anon-key'
SUPABASE_SERVICE_ROLE_KEY = 'tu-service-role-key'
```

## Ejecutar Schema en Supabase

```sql
-- Ejecutar el archivo database/supabase_voting_schema.sql
-- en la consola SQL de Supabase
```

## Modo Demo

El sistema incluye un modo demo que funciona sin conexión real a Supabase:
- Simula todas las operaciones
- Genera datos de prueba
- Útil para desarrollo y pruebas

## Seguridad

- **RLS (Row Level Security)**: Habilitado en todas las tablas
- **Validaciones estrictas**: En todas las operaciones
- **Auditoría**: Todos los votos son registrados con timestamp
- **No manipulación**: Los contadores se actualizan automáticamente

## Errores Comunes

### 400 Bad Request
- Datos inválidos o faltantes
- Fechas inválidas
- Usuario ya votó
- No es elegible para votar

### 401 Unauthorized
- Token inválido o expirado
- Usuario no autenticado

### 403 Forbidden
- No tiene permiso para la operación
- No es elegible para votar

### 404 Not Found
- La consulta no existe
- La opción no existe

### 500 Internal Server Error
- Error de conexión con Supabase
- Error interno del servidor

## Ejemplo de Flujo Completo

1. **Crear consulta**: `POST /api/users/voting/consultations/create/`
2. **Agregar opciones**: `POST /api/users/voting/consultations/<uuid>/options/`
3. **Otorgar permisos**: `POST /api/users/voting/consultations/<uuid>/permissions/`
4. **Verificar elegibilidad**: `GET /api/users/voting/consultations/<uuid>/eligibility/`
5. **Votar**: `POST /api/users/voting/consultations/<uuid>/vote/`
6. **Ver resultados**: `GET /api/users/voting/consultations/<uuid>/results/`
