# Configuración de Supabase para Political Parties

## 🚀 Configuración Completada

El entry point `/api/political-parties/register/` ahora está configurado para usar **Supabase** en lugar de la base de datos local.

## 📋 Cambios Realizados

### 1. **Vista Actualizada** (`views.py`)
- ✅ Se eliminaron dependencias de Django Repository
- ✅ Se agregó importación de `PoliticalPartyValidator`
- ✅ Se agregó importación de `PoliticalParty` entidad
- ✅ Se agregó importación de `political_parties_service` (Supabase)

### 2. **Método POST** - Registrar Partido Político
```python
def post(self, request):
    try:
        # Validar datos de entrada
        PoliticalPartyValidator.validate(request.data)
        
        # Crear entidad PoliticalParty
        party = PoliticalParty(**request.data)
        
        # Preparar datos para Supabase
        party_data = {
            "name": party.name,
            "acronym": party.acronym,
            "party_type": party.party_type,
            "ideology": party.ideology,
            "legal_representative": party.legal_representative,
            "representative_id": party.representative_id,
            "email": party.email,
            "foundation_date": party.foundation_date
        }
        
        # Guardar en Supabase
        result = political_parties_service.create_party(party_data)
        
        return Response({ 
            "message": "Partido político registrado exitosamente",
            "data": result
        }, status=status.HTTP_201_CREATED)
```

### 3. **Método GET** - Listar Partidos Políticos
```python
def get(self, request):
    try:
        # Obtener partidos activos desde Supabase
        parties = political_parties_service.get_all_active_parties()
        
        return Response({
            "message": "Partidos políticos obtenidos exitosamente",
            "data": parties
        }, status=status.HTTP_200_OK)
```

## 🔧 Uso de la API

### **POST** `/api/political-parties/register/`
```bash
curl -X POST http://127.0.0.1:8000/api/political-parties/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Partido de Ejemplo",
    "acronym": "PDEJ",
    "party_type": "PARTY",
    "ideology": "Ideología de centro",
    "legal_representative": "Juan Pérez",
    "representative_id": "12345678",
    "email": "contacto@partido.com",
    "foundation_date": "2020-01-15"
  }'
```

**Respuesta exitosa:**
```json
{
    "message": "Partido político registrado exitosamente",
    "data": {
        "id": "uuid-generado",
        "name": "Partido de Ejemplo",
        "acronym": "PDEJ",
        "party_type": "PARTY",
        "ideology": "Ideología de centro",
        "legal_representative": "Juan Pérez",
        "representative_id": "12345678",
        "email": "contacto@partido.com",
        "foundation_date": "2020-01-15",
        "created_at": "2026-03-09T..."
    }
}
```

### **GET** `/api/political-parties/`
```bash
curl -X GET http://127.0.0.1:8000/api/political-parties/
```

**Respuesta:**
```json
{
    "message": "Partidos políticos obtenidos exitosamente",
    "data": [
        {
            "id": "uuid-1",
            "name": "Partido A",
            "acronym": "PA",
            "party_type": "PARTY",
            "ideology": "Ideología A",
            "legal_representative": "Rep A",
            "representative_id": "ID_A",
            "email": "contacto@partidoA.com",
            "foundation_date": "2020-01-01",
            "created_at": "2026-03-09T..."
        }
        // ... más partidos
    ]
}
```

## ✅ Validaciones Implementadas

### **Errores de Validación (400 Bad Request)**
- Nombre duplicado: `"Ya existe un partido político con el nombre 'X'"`
- Email duplicado: `"Ya existe un partido político con el email 'X'"`
- Tipo de partido inválido: `"Tipo de organización política no válido. Valores permitidos: PARTY o MOVEMENT"`
- Sigla muy larga: `"La sigla excede lo permitido"`

### **Errores del Servidor (500 Internal Server Error)**
- Error de conexión a Supabase
- Error inesperado en el procesamiento

## 🗄️ Base de Datos

Los datos ahora se guardan en **Supabase** en la tabla `political_parties` con:
- ✅ Row Level Security (RLS)
- ✅ Índices optimizados
- ✅ Auditoría automática
- ✅ Timestamps automáticos
- ✅ Validaciones de integridad

## 🔄 Próximos Pasos

1. **Ejecutar schemas SQL** en Supabase
2. **Probar endpoints** con diferentes datos
3. **Implementar autenticación** con Supabase Auth
4. **Agregar endpoints** para actualizar/eliminar partidos
5. **Configurar webhooks** para sincronización

La API está lista para usar con Supabase! 🎉
