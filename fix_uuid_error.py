"""
Script para solucionar el error de UUID en created_by
Ejecuta: python fix_uuid_error.py
"""

import os
import subprocess
import sys

def show_solution():
    """Mostrar la solución paso a paso"""
    print("🔧 SOLUCIÓN PARA ERROR DE UUID")
    print("="*60)
    
    print("\n❌ ERROR DETECTADO:")
    print("   'invalid input syntax for type uuid: \"None\"'")
    print("   Esto ocurre porque el campo created_by intenta guardar 'None' como UUID")
    
    print("\n🎯 SOLUCIÓN:")
    print("   Necesitas ejecutar el schema corregido en Supabase")
    
    print("\n📋 PASOS PARA SOLUCIONAR:")
    print("   1. Ve a tu dashboard de Supabase: https://app.supabase.com")
    print("   2. Selecciona tu proyecto")
    print("   3. Ve a 'SQL Editor' en el menú lateral")
    print("   4. Copia el contenido del archivo corregido:")
    print("      📁 database/supabase_voting_schema_fixed.sql")
    print("   5. Pégalo en el editor SQL")
    print("   6. Haz clic en 'Run' para ejecutar")
    print("   7. Espera a que se ejecuten todas las tablas")
    
    print("\n⚠️  IMPORTANTE:")
    print("   - Esto eliminará las tablas existentes")
    print("   - Se crearán nuevas tablas corregidas")
    print("   - Los datos existentes se perderán")
    
    print("\n✅ DESPUÉS DE EJECUTAR:")
    print("   - Reinicia el servidor Django")
    print("   - Vuelve a probar el endpoint")
    print("   - El error debería desaparecer")

def show_sql_fix():
    """Mostrar el SQL específico para arreglar el problema"""
    print("\n🔧 SQL CORRECTIVO (si no quieres recrear todo):")
    print("="*60)
    
    sql_fix = """
-- Corregir el campo created_by para permitir NULL
ALTER TABLE popular_consultations DROP CONSTRAINT IF EXISTS popular_consultations_created_by_fkey;
ALTER TABLE popular_consultations ALTER COLUMN created_by DROP NOT NULL;

-- Actualizar políticas RLS para modo demo
DROP POLICY IF EXISTS "Usuarios autenticados pueden crear consultas" ON popular_consultations;
DROP POLICY IF EXISTS "Creador puede actualizar su consulta" ON popular_consultations;

CREATE POLICY "Todos pueden crear consultas (modo demo)" ON popular_consultations
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Todos pueden actualizar consultas (modo demo)" ON popular_consultations
    FOR UPDATE USING (true);
"""
    
    print("Copia y ejecuta este SQL en Supabase SQL Editor:")
    print(sql_fix)

def show_repository_fix():
    """Mostrar cómo está corregido el repositorio"""
    print("\n🐍 REPOSITORIO CORREGIDO:")
    print("="*60)
    
    print("El repositorio ya está corregido:")
    print("   📁 system_voting/src/users/infrastructure/repositories/supabase_voting_repository.py")
    print("   Línea 73: Manejo de created_by None")
    
    print("\nCódigo corregido:")
    print("""
    data = {
        'title': command.title,
        'description': command.description,
        'start_date': command.start_date.isoformat(),
        'end_date': command.end_date.isoformat(),
        'min_votes': command.min_votes,
        'created_by': command.created_by if command.created_by != 'demo-user' else None
    }
    """)

def test_fix():
    """Probar si el fix funciona"""
    print("\n🧪 PARA PROBAR EL FIX:")
    print("="*60)
    
    print("1. Ejecuta el schema corregido en Supabase")
    print("2. Reinicia el servidor:")
    print("   python manage.py runserver")
    print("3. Prueba con PowerShell:")
    
    test_command = '''
$data = @{
    title = "Consulta Test UUID Fix"
    description = "Probando que el error de UUID está solucionado"
    start_date = "2026-03-11T18:00:00Z"
    end_date = "2026-03-18T18:00:00Z"
    min_votes = 1
}

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/users/voting/consultations/create/" -Method POST -ContentType "application/json" -Body ($data | ConvertTo-Json)
'''
    
    print(test_command)
    
    print("4. Resultado esperado:")
    print("""
{
  "success": true,
  "message": "Consulta creada exitosamente",
  "data": {
    "id": "uuid-generado",
    "title": "Consulta Test UUID Fix",
    "status": "ACTIVE"
  }
}
    """)

def main():
    """Función principal"""
    print("🚀 SOLUCIÓN AUTOMÁTICA PARA ERROR DE UUID")
    print("="*70)
    
    show_solution()
    show_sql_fix()
    show_repository_fix()
    test_fix()
    
    print("\n📚 RESUMEN:")
    print("="*60)
    print("✅ El repositorio está corregido")
    print("✅ El schema corregido está listo")
    print("✅ Solo necesitas ejecutar el SQL en Supabase")
    print("✅ Después de ejecutar el SQL, el error desaparecerá")
    
    print("\n🎯 ACCIÓN REQUERIDA:")
    print("   1. Ejecuta database/supabase_voting_schema_fixed.sql en Supabase")
    print("   2. Reinicia el servidor Django")
    print("   3. Prueba el endpoint")
    
    print(f"\n📁 ARCHIVOS IMPORTANTES:")
    print(f"   📄 database/supabase_voting_schema_fixed.sql - Schema corregido")
    print(f"   📄 system_voting/src/users/infrastructure/repositories/supabase_voting_repository.py - Repositorio corregido")

if __name__ == "__main__":
    main()
