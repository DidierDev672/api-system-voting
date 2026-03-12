# API de Autenticación con Supabase

## Overview

Esta API proporciona endpoints para autenticación de usuarios utilizando Supabase Auth como backend.

## Endpoints

### 1. Registro de Usuario
```
POST /api/users/auth/register/
```

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123",
  "full_name": "Usuario Ejemplo",
  "phone": "+1234567890"  // Opcional
}
```

**Response Exitosa (201):**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "user": {
      "id": "uuid-del-usuario",
      "email": "usuario@ejemplo.com",
      "full_name": "Usuario Ejemplo",
      "phone": "+1234567890"
    },
    "session": {
      "access_token": "jwt-access-token",
      "refresh_token": "jwt-refresh-token",
      "expires_at": 1672531200
    }
  }
}
```

**Response de Error (400):**
```json
{
  "success": false,
  "error": "El correo electrónico ya está registrado"
}
```

### 2. Login de Usuario
```
POST /api/users/auth/login/
```

**Request Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "password123"
}
```

**Response Exitosa (200):**
```json
{
  "success": true,
  "message": "Login exitoso",
  "data": {
    "user": {
      "id": "uuid-del-usuario",
      "email": "usuario@ejemplo.com",
      "full_name": "Usuario Ejemplo",
      "phone": "+1234567890"
    },
    "session": {
      "access_token": "jwt-access-token",
      "refresh_token": "jwt-refresh-token",
      "expires_at": 1672531200
    }
  }
}
```

### 3. Obtener Perfil
```
GET /api/users/auth/profile/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response Exitosa (200):**
```json
{
  "success": true,
  "message": "Perfil obtenido exitosamente",
  "data": {
    "user": {
      "id": "uuid-del-usuario",
      "email": "usuario@ejemplo.com",
      "full_name": "Usuario Ejemplo",
      "phone": "+1234567890"
    }
  }
}
```

### 4. Logout
```
POST /api/users/auth/logout/
```

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response Exitosa (200):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

### 5. Refrescar Token
```
POST /api/users/auth/refresh/
```

**Request Body:**
```json
{
  "refresh_token": "jwt-refresh-token"
}
```

**Response Exitosa (200):**
```json
{
  "success": true,
  "message": "Token refrescado exitosamente",
  "data": {
    "session": {
      "access_token": "nuevo-jwt-access-token",
      "refresh_token": "nuevo-jwt-refresh-token",
      "expires_at": 1672531200
    }
  }
}
```

## Configuración Requerida

En el archivo `settings.py` de Django, asegúrate de tener:

```python
# Configuración de Supabase
SUPABASE_URL = 'https://your-project.supabase.co'
SUPABASE_ANON_KEY = 'your-anon-key'
SUPABASE_SERVICE_ROLE_KEY = 'your-service-role-key'
```

## Errores Comunes

### 400 Bad Request
- Campos obligatorios faltantes
- Formato de email inválido
- Contraseña demasiado corta (mínimo 6 caracteres)
- Email ya registrado

### 401 Unauthorized
- Token inválido o expirado
- Credenciales incorrectas
- Email no confirmado

### 500 Internal Server Error
- Error de configuración de Supabase
- Problemas de conexión con Supabase

## Uso de Tokens

Los tokens JWT deben incluirse en el header Authorization:

```
Authorization: Bearer <access_token>
```

El access token tiene una duración limitada (generalmente 1 hora).
Usa el refresh token para obtener un nuevo access token sin requerir login nuevamente.

## Seguridad

- Las contraseñas deben tener al menos 6 caracteres
- Los emails deben ser válidos
- Los tokens expiran automáticamente
- Se recomienda usar HTTPS en producción
