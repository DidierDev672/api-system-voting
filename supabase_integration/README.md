# Configuración de Supabase para API REST

## Variables de Entorno

Asegúrate de tener estas variables en tu archivo `.env`:

```env
SUPABASE_URL=https://pbesvbrclrmjarouyler.supabase.co
SUPABASE_ANON_KEY=sb_publishable_1seK7gY_xUY3jeni96X9tw_fzTRt6tA
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

## Estructura de la Base de Datos

### 1. Party Members (Miembros de Partidos)
- **Tabla**: `party_members`
- **Endpoint**: `/api/party-members/register/`
- **Método**: POST

### 2. Political Parties (Partidos Políticos)
- **Tabla**: `political_parties`
- **Endpoints**: 
  - `/api/political-parties/register/` (POST)
  - `/api/political-parties/` (GET)

### 3. Users (Usuarios)
- **Tabla**: `users`
- **Endpoints**: Por implementar

### 4. Popular Consultations (Consultas Populares)
- **Tablas**: `popular_consultations`, `consultation_options`, `consultation_votes`
- **Endpoints**: Por implementar

## Instalación de Schemas

### Paso 1: Ejecutar los schemas en orden

1. `01_party_members.sql` - Tabla de miembros de partidos
2. `02_political_parties.sql` - Tabla de partidos políticos
3. `03_users.sql` - Tabla de usuarios
4. `04_popular_consultations.sql` - Tablas de consultas populares
5. `05_functions_and_triggers.sql` - Funciones y triggers comunes

### Paso 2: Configurar Row Level Security (RLS)

Todos los schemas incluyen políticas RLS básicas. Ajusta según tus necesidades de seguridad.

### Paso 3: Configurar API Keys

1. Ve a tu proyecto Supabase
2. Settings > API
3. Copia las keys necesarias y agrégalas a tu `.env`

## Características Implementadas

### Seguridad
- Row Level Security (RLS) en todas las tablas
- Validación de emails
- Auditoría automática de cambios
- Triggers para timestamps

### Optimización
- Índices optimizados para consultas frecuentes
- Vistas para estadísticas y resultados
- Funciones de utilidad

### Integridad de Datos
- Constraints y validaciones
- Relaciones con claves foráneas
- Triggers para normalización de datos

## Endpoints Disponibles

### Party Members
```http
POST /api/party-members/register/
Content-Type: application/json

{
    "full_name": "Juan Pérez",
    "document_type": "CC",
    "document_number": "12345678",
    "birth_date": "1990-01-01",
    "city": "Bogotá",
    "political_party_id": "uuid-del-partido",
    "consent": true,
    "data_authorization": true
}
```

### Political Parties
```http
POST /api/political-parties/register/
Content-Type: application/json

{
    "name": "Partido de Ejemplo",
    "acronym": "PDEJ",
    "party_type": "PARTY",
    "ideology": "Ideología de centro",
    "legal_representative": "Representante Legal",
    "representative_id": "ID_REP",
    "email": "contacto@partido.com",
    "foundation_date": "2020-01-15"
}
```

```http
GET /api/political-parties/
```

## Próximos Pasos

1. Implementar endpoints para Users
2. Implementar endpoints para Popular Consultations
3. Agregar autenticación con Supabase Auth
4. Implementar webhooks para sincronización
5. Agregar tests para los endpoints
