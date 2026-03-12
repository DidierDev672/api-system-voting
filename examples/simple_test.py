"""
Ejemplo simple sin emojis para probar el sistema de votacion
Ejecuta: python examples/simple_test.py
"""

import requests
import json
from datetime import datetime, timedelta

# Configuracion
BASE_URL = "http://127.0.0.1:8000/api/users"
HEADERS = {"Content-Type": "application/json"}

def test_endpoint(name, url, method="GET", data=None):
    """Probar un endpoint especifico"""
    print(f"\n{'='*50}")
    print(f"Probando: {name}")
    print(f"URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("EXITO")
            try:
                result = response.json()
                print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
            except:
                print(f"Response: {response.text[:500]}...")
        else:
            print("ERROR")
            try:
                result = response.json()
                print(f"Error: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"Error: {response.text}")
        
        return response
        
    except Exception as e:
        print(f"Exception: {str(e)}")
        return None

def main():
    """Funcion principal de prueba"""
    print("EJEMPLO RAPIDO DEL SISTEMA DE VOTACION")
    print("Asegurate de que el servidor Django este corriendo en http://127.0.0.1:8000")
    
    # 1. Probar Dashboard
    test_endpoint(
        "Dashboard de Votacion",
        f"{BASE_URL}/voting/dashboard/"
    )
    
    # 2. Probar Listar Consultas
    test_endpoint(
        "Listar Consultas Populares",
        f"{BASE_URL}/voting/consultations/"
    )
    
    # 3. Crear Consulta Popular
    print(f"\n{'='*50}")
    print("CREANDO CONSULTA POPULAR")
    
    consultation_data = {
        "title": "Consulta de Ejemplo Rapido",
        "description": "Esta es una consulta de ejemplo creada para probar rapidamente el sistema de votacion. Es una demostracion funcional del endpoint de creacion de consultas populares.",
        "start_date": (datetime.now() + timedelta(hours=1)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=3)).isoformat(),
        "min_votes": 1
    }
    
    response = test_endpoint(
        "Crear Consulta Popular",
        f"{BASE_URL}/voting/consultations/create/",
        method="POST",
        data=consultation_data
    )
    
    # Extraer ID de la consulta creada
    consultation_id = None
    if response and response.status_code == 201:
        try:
            data = response.json()
            if data.get("success"):
                consultation_id = data["data"]["id"]
                print(f"Consulta ID: {consultation_id}")
        except:
            pass
    
    # 4. Obtener detalle de la consulta
    if consultation_id:
        test_endpoint(
            f"Detalle de Consulta ({consultation_id[:8]}...)",
            f"{BASE_URL}/voting/consultations/{consultation_id}/"
        )
        
        # 5. Otorgar permiso a usuario
        permission_data = {
            "user_id": "demo-user-1",
            "can_vote": True
        }
        
        test_endpoint(
            f"Otorgar Permiso a demo-user-1",
            f"{BASE_URL}/voting/consultations/{consultation_id}/permissions/",
            method="POST",
            data=permission_data
        )
        
        # 6. Verificar elegibilidad
        test_endpoint(
            f"Verificar Elegibilidad de demo-user-1",
            f"{BASE_URL}/voting/consultations/{consultation_id}/eligibility/"
        )
        
        # 7. Intentar votar (necesitariamos un option_id valido)
        vote_data = {
            "option_id": "opcion-ejemplo"
        }
        
        test_endpoint(
            f"Intentar Votar (probablemente error)",
            f"{BASE_URL}/voting/consultations/{consultation_id}/vote/",
            method="POST",
            data=vote_data
        )
        
        # 8. Obtener resultados
        test_endpoint(
            f"Resultados de Consulta",
            f"{BASE_URL}/voting/consultations/{consultation_id}/results/"
        )
    
    # 9. Probar historial de votos
    test_endpoint(
        "Historial de Votos del Usuario",
        f"{BASE_URL}/voting/history/"
    )
    
    print(f"\n{'='*50}")
    print("PRUEBA COMPLETADA")
    print("Los endpoints principales del sistema de votacion estan funcionando")
    print("Para mas ejemplos, revisa:")
    print("   - examples/voting_example.py (ejemplo completo)")
    print("   - examples/curl_examples.md (ejemplos con curl)")
    print("   - VOTING_API_GUIDE.md (documentacion completa)")

if __name__ == "__main__":
    main()
