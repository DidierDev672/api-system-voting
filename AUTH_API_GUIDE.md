# API de Autenticación - Sistema de Votación

## Overview

Sistema completo de autenticación con JWT y Supabase.

## Endpoints

### Autenticación
- `POST /api/auth/login/` - Login
- `POST /api/auth/register/` - Registro
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/profile/` - Perfil

### Gestión de Contraseñas
- `POST /api/auth/change-password/` - Cambiar contraseña
- `POST /api/auth/reset-password/` - Resetear contraseña

## Ejemplos

### Login
```json
POST /api/auth/login/
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

### Registro
```json
POST /api/auth/register/
{
  "full_name": "Juan Pérez",
  "document_type": "CC",
  "document_number": "12345678",
  "email": "juan@ejemplo.com",
  "password": "password123",
  "role": "MEMBER"
}
```

### Refresh Token
```json
POST /api/auth/refresh/
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Uso de Tokens

Incluir token en header:
```
Authorization: Bearer <access_token>
```

## Middleware y Decoradores

### Autenticación
```python
from system_voting.src.users.middleware.jwt_authentication import JWTAuthentication

class MyView(APIView):
    authentication_classes = [JWTAuthentication]
```

### Permisos
```python
from system_voting.src.users.middleware.jwt_authentication import (
    require_permission, require_role, require_super_admin
)

@require_permission('manage_users')
def my_view(request):
    pass

@require_super_admin
def admin_view(request):
    pass
```

## Seguridad

- Tokens JWT con expiración
- Refresh tokens revocables
- Hashing de contraseñas SHA-256
- Validación de permisos por rol
