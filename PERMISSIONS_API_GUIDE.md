# API de Permisos - Sistema de Votación

## Overview

Se ha creado un sistema completo de gestión de permisos con los roles solicitados:
- **Super Admin**: Control total del sistema
- **Representante**: Gestión de grupos y votaciones  
- **Miembros**: Participación en votaciones
- **Citizen**: Rol por defecto (acceso básico)

## Arquitectura

El sistema sigue los patrones de **Vertical Slicing + Hexagonal Architecture**:

### Domain Layer
- `permissions.py`: Enums de permisos y roles
- `permission.py`: Entidades de dominio
- `permission_repository.py`: Puerto del repositorio

### Application Layer  
- `permission_service.py`: Lógica de negocio de permisos

### Infrastructure Layer
- `supabase_permission_repository.py`: Implementación con Supabase

### API Layer
- `permission_views.py`: Vistas REST API
- `urls.py`: Endpoints configurados

## Endpoints API

### Gestión de Permisos

#### Crear Permisos de Usuario
```
POST /api/users/permissions/
Content-Type: application/json

{
  "user_id": "uuid-del-usuario",
  "role": "SUPER_ADMIN|REPRESENTATIVE|MEMBER|CITIZEN",
  "additional_permissions": ["VOTE", "VIEW_RESULTS"],
  "assigned_by": "uuid-admin"
}
```

#### Obtener Permisos de Usuario
```
GET /api/users/{user_id}/permissions/
```

#### Actualizar Permisos
```
PUT /api/users/permissions/{permission_id}/
Content-Type: application/json

{
  "role": "REPRESENTATIVE",
  "additional_permissions": ["CREATE_VOTING"],
  "is_active": true
}
```

#### Listar Todos los Permisos
```
GET /api/users/permissions/list/
GET /api/users/permissions/list/?role=REPRESENTATIVE
```

### Asignación/Revocación de Permisos

#### Asignar Permiso Adicional
```
POST /api/users/permissions/assign/
Content-Type: application/json

{
  "user_id": "uuid-del-usuario",
  "permission": "MANAGE_VOTING",
  "assigned_by": "uuid-admin"
}
```

#### Revocar Permiso Adicional
```
DELETE /api/users/{user_id}/permissions/{permission}/
```

### Información y Verificación

#### Obtener Roles y Permisos Disponibles
```
GET /api/users/permissions/info/
```

#### Verificar Permisos de Usuario
```
POST /api/users/permissions/check/
Content-Type: application/json

{
  "user_id": "uuid-del-usuario",
  "permission": "MANAGE_USERS",
  "required_permissions": ["MANAGE_USERS", "ASSIGN_ROLES"]
}
```

## Jerarquía de Permisos

### Super Admin
- `manage_users`: Gestionar cualquier usuario
- `manage_system`: Administración del sistema
- `view_all_reports`: Ver todos los reportes
- `delete_any_user`: Eliminar cualquier usuario
- `assign_roles`: Asignar roles a usuarios
- Hereda todos los permisos de roles inferiores

### Representante
- `manage_group_users`: Gestionar usuarios del grupo
- `view_group_reports`: Ver reportes del grupo
- `create_voting`: Crear votaciones
- `manage_voting`: Administrar votaciones
- Hereda todos los permisos de Miembros

### Miembros
- `vote`: Participar en votaciones
- `view_results`: Ver resultados
- `update_profile`: Actualizar perfil propio
- `view_own_data`: Ver datos propios

### Citizen (Rol por defecto)
- `update_profile`: Actualizar perfil propio
- `view_own_data`: Ver datos propios

## Ejemplos de Uso

### 1. Crear Super Admin
```bash
curl -X POST http://localhost:8000/api/users/permissions/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "role": "SUPER_ADMIN"
  }'
```

### 2. Asignar Representante
```bash
curl -X POST http://localhost:8000/api/users/permissions/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440001",
    "role": "REPRESENTATIVE"
  }'
```

### 3. Verificar Permisos
```bash
curl -X POST http://localhost:8000/api/users/permissions/check/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "permission": "manage_users"
  }'
```

### 4. Obtener Información de Roles
```bash
curl -X GET http://localhost:8000/api/users/permissions/info/
```

## Integración con Registro de Usuarios

El sistema de permisos se integra automáticamente con el registro de usuarios existente. Al registrar un nuevo usuario, se puede especificar el rol:

```json
{
  "full_name": "Juan Pérez",
  "document_type": "CC",
  "document_number": "12345678",
  "email": "juan@ejemplo.com",
  "role": "MEMBER"
}
```

## Validaciones y Seguridad

- Validación de roles permitidos
- Verificación de existencia de usuarios
- Control de permisos adicionales
- Manejo de errores y validaciones
- Estructura de respuestas consistente

## Próximos Pasos

1. Configurar middleware de autenticación
2. Implementar decoradores de permisos
3. Crear endpoints específicos para votaciones
4. Configurar base de datos real (Supabase)
5. Implementar logging y auditoría

El sistema está listo para ser utilizado y extendido según las necesidades del proyecto.
