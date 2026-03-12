# Guía de Configuración del Sistema de Votación con Supabase

## 🚀 **Configuración Rápida (Recomendado)**

### Paso 1: Ejecutar Script Automático
```bash
python setup_supabase.py
```

Este script te guiará paso a paso para:
- ✅ Configurar tus credenciales de Supabase
- ✅ Actualizar settings.py automáticamente
- ✅ Probar la conexión
- ✅ Validar que todo funcione

---

## 📋 **Configuración Manual**

### Paso 1: Obtener Credenciales de Supabase

1. Ve a [Supabase Dashboard](https://app.supabase.com)
2. Selecciona tu proyecto
3. Ve a **Settings → API**
4. Copia los siguientes valores:
   - **Project URL**: `https://tu-proyecto.supabase.co`
   - **anon public**: `eyJ...` (llave pública)
   - **service_role**: `eyJ...` (llave privada, no compartirla)

### Paso 2: Configurar Variables de Entorno

#### Opción A: Archivo .env (Recomendado)
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env
nano .env  # o usa tu editor preferido
```

**Contenido del archivo .env:**
```env
# Configuración de Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_ANON_KEY=eyJ...tu-anon-key...
SUPABASE_SERVICE_ROLE_KEY=eyJ...tu-service-role-key...
```

#### Opción B: Variables de Sistema (Windows)
```powershell
# En PowerShell (administrador)
$env:SUPABASE_URL="https://tu-proyecto.supabase.co"
$env:SUPABASE_ANON_KEY="eyJ...tu-anon-key..."
$env:SUPABASE_SERVICE_ROLE_KEY="eyJ...tu-service-role-key..."
```

#### Opción C: Directamente en settings.py
```python
# system_voting/settings.py
SUPABASE_URL = 'https://tu-proyecto.supabase.co'
SUPABASE_ANON_KEY = 'eyJ...tu-anon-key...'
SUPABASE_SERVICE_ROLE_KEY = 'eyJ...tu-service-role-key...'
```

### Paso 3: Ejecutar Schema de Base de Datos

1. Ve a tu [Dashboard Supabase](https://app.supabase.com)
2. Selecciona tu proyecto
3. Ve a **SQL Editor**
4. Abre el archivo: `database/supabase_voting_schema.sql`
5. Copia todo el contenido del archivo SQL
6. Pégalo en el editor SQL de Supabase
7. Haz clic en **Run** ▶️

**El schema crea:**
- `popular_consultations` - Consultas populares
- `voting_options` - Opciones de votación  
- `votes` - Votos registrados
- `voting_permissions` - Permisos de votación
- Vistas y funciones útiles
- Políticas RLS para seguridad

### Paso 4: Verificar Configuración

```bash
# Probar conexión
python -c "
from system_voting.src.users.infrastructure.repositories.supabase_voting_repository import SupabaseVotingRepository
repo = SupabaseVotingRepository()
print('Demo mode:', repo.demo_mode)
if not repo.demo_mode:
    print('✅ Conectado a Supabase')
else:
    print('❌ Modo demo activo')
"
```

---

## 🧪 **Probar el Sistema**

### 1. Iniciar Servidor
```bash
python manage.py runserver
```

### 2. Probar Endpoint de Creación
```powershell
# Crear consulta (ahora se guardará en Supabase)
$data = @{
    title = "Consulta Supabase Test"
    description = "Esta consulta se guardará en Supabase"
    start_date = "2026-03-11T18:00:00Z"
    end_date = "2026-03-18T18:00:00Z"
    min_votes = 2
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/voting/consultations/create/" -Method POST -Headers @{"Content-Type"="application/json"} -Body ($data | ConvertTo-Json)
```

### 3. Verificar en Supabase
1. Ve al Dashboard de Supabase
2. **Table Editor** → `popular_consultations`
3. Deberías ver la consulta creada

---

## 🔧 **Troubleshooting**

### Error: "Demo mode activo"
**Causa:** Las variables de entorno no están configuradas
**Solución:**
```bash
# Verificar variables
echo $SUPABASE_URL
echo $SUPABASE_ANON_KEY

# O verificar en Python
import os
print(os.getenv('SUPABASE_URL'))
```

### Error: "Invalid API key"
**Causa:** Credenciales incorrectas
**Solución:** Verifica que las llaves sean correctas y no tengan espacios

### Error: "Permission denied"
**Causa:** El schema no se ejecutó correctamente
**Solución:** Re-ejecuta el schema SQL en Supabase

### Error: "Table not found"
**Causa:** Las tablas no se crearon
**Solución:** Verifica en Table Editor que existan las 4 tablas principales

---

## 📊 **Verificación de Funcionalidad**

### Test Completo:
```bash
# Ejecutar test completo
python examples/simple_test.py
```

### Verificar en Supabase:
1. **popular_consultations**: Debe tener la consulta creada
2. **voting_options**: Debe tener opciones automáticas
3. **votes**: Vacío inicialmente
4. **voting_permissions**: Permisos otorgados

### Dashboard:
```bash
# Ver dashboard con datos reales
curl http://127.0.0.1:8000/api/users/voting/dashboard/
```

---

## 🚨 **Consideraciones de Seguridad**

### 1. Service Role Key
- **Nunca** exponer en el frontend
- **Siempre** mantener en variables de entorno
- **Solo** usar en backend

### 2. Políticas RLS
- El schema incluye políticas de seguridad
- Verifica que estén activas en Supabase
- Revisa los permisos por tabla

### 3. Variables de Entorno
- Añadir `.env` a `.gitignore`
- No commitear credenciales
- Usar diferentes claves para dev/prod

---

## 🎯 **Resumen de Configuración**

| Componente | Estado | Verificación |
|------------|---------|-------------|
| **Variables de entorno** | ✅ Configuradas | `echo $SUPABASE_URL` |
| **Schema SQL** | ✅ Ejecutado | Table Editor en Supabase |
| **Conexión** | ✅ Activa | Script de prueba |
| **Endpoints** | ✅ Funcionando | `python examples/simple_test.py` |
| **Datos** | ✅ Guardando | Ver en Supabase Dashboard |

---

## 📞 **Soporte**

Si tienes problemas:
1. **Revisa los logs** del servidor Django
2. **Verifica credenciales** en Supabase Dashboard
3. **Ejecuta el script** `setup_supabase.py`
4. **Revisa el schema** SQL

**¡Tu sistema de votación estará conectado a Supabase en minutos!**
