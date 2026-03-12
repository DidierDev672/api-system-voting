#!/bin/bash

# Script para configurar Supabase con las tablas necesarias
# Este script ejecuta todos los schemas SQL en el orden correcto

echo "🚀 Configurando Supabase para el Sistema de Votación"
echo "=================================================="

# Verificar variables de entorno
if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "❌ Error: Las variables de entorno SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY son requeridas"
    echo "Por favor, configúralas en tu archivo .env"
    exit 1
fi

echo "✅ Variables de entorno verificadas"
echo ""

# Directorio de schemas
SCHEMAS_DIR="supabase_integration/schemas"

# Lista de schemas en orden de ejecución
SCHEMAS=(
    "01_party_members.sql"
    "02_political_parties.sql"
    "03_users.sql"
    "04_popular_consultations.sql"
    "05_functions_and_triggers.sql"
)

echo "📋 Ejecutando schemas SQL en orden:"
echo ""

# Ejecutar cada schema
for schema in "${SCHEMAS[@]}"; do
    echo "🔄 Ejecutando $schema..."
    
    # Leer el contenido del archivo
    if [ -f "$SCHEMAS_DIR/$schema" ]; then
        # Aquí deberías usar el cliente de Supabase CLI o curl para ejecutar el SQL
        # Por ahora, mostramos el contenido para que lo copies manualmente
        echo "📝 Contenido de $schema:"
        echo "----------------------------------------"
        cat "$SCHEMAS_DIR/$schema"
        echo "----------------------------------------"
        echo ""
        echo "✅ $schema listo para ejecutar en Supabase Dashboard"
        echo ""
    else
        echo "❌ Error: No se encuentra el archivo $schema"
        exit 1
    fi
done

echo "🎉 Todos los schemas han sido preparados!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Ve a https://pbesvbrclrmjarouyler.supabase.co"
echo "2. Inicia sesión y ve a SQL Editor"
echo "3. Copia y ejecuta cada schema en el orden mostrado"
echo "4. Verifica que las tablas se creen correctamente"
echo ""
echo "🚀 Una vez configurado, prueba los endpoints:"
echo "- POST http://127.0.0.1:8000/api/party-members/register/"
echo "- GET http://127.0.0.1:8000/api/party-members/"
echo "- POST http://127.0.0.1:8000/api/political-parties/register/"
echo "- GET http://127.0.0.1:8000/api/political-parties/"
