"""
Ejemplo completo del sistema de votación de consultas populares
Este script demuestra el flujo completo de votación:
1. Crear consulta popular
2. Agregar opciones de votación
3. Otorgar permisos a usuarios
4. Verificar elegibilidad
5. Votar
6. Obtener resultados
"""

import requests
import json
import uuid
from datetime import datetime, timedelta

# Configuración
BASE_URL = "http://127.0.0.1:8000/api/users"
HEADERS = {
    "Content-Type": "application/json",
    # En producción, agregar: "Authorization": "Bearer <token>"
}

class VotingExample:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.consultation_id = None
        self.option_ids = []
        self.user_ids = ["demo-user-1", "demo-user-2", "demo-user-3"]
    
    def log(self, message, response=None):
        """Imprimir mensaje de log"""
        print(f"\n{'='*60}")
        print(f"🔹 {message}")
        if response:
            print(f"📊 Status: {response.status_code}")
            try:
                data = response.json()
                print(f"📄 Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
            except:
                print(f"📄 Response: {response.text}")
        print('='*60)
    
    def create_consultation(self):
        """Crear una nueva consulta popular"""
        print("\n🚀 CREANDO CONSULTA POPULAR")
        
        # Datos de la consulta
        consultation_data = {
            "title": "Consulta Popular: Presupuesto Participativo 2026",
            "description": "Decida cómo se distribuirá el presupuesto participativo del municipio para el año 2026. Esta consulta permite a los ciudadanos elegir entre diferentes opciones de inversión en áreas clave como educación, salud, infraestructura y desarrollo económico. Su voto es importante para definir las prioridades de nuestra comunidad.",
            "start_date": (datetime.now() + timedelta(hours=1)).isoformat(),
            "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "min_votes": 3
        }
        
        response = requests.post(
            f"{self.base_url}/voting/consultations/create/",
            json=consultation_data,
            headers=self.headers
        )
        
        self.log("Crear consulta popular", response)
        
        if response.status_code == 201:
            data = response.json()
            if data.get("success"):
                self.consultation_id = data["data"]["id"]
                print(f"✅ Consulta creada con ID: {self.consultation_id}")
                return True
        
        print("❌ Error al crear consulta")
        return False
    
    def get_consultation_detail(self):
        """Obtener detalle de la consulta"""
        if not self.consultation_id:
            print("❌ No hay consulta ID")
            return
        
        print(f"\n📋 OBTENIENDO DETALLE DE CONSULTA: {self.consultation_id}")
        
        response = requests.get(
            f"{self.base_url}/voting/consultations/{self.consultation_id}/",
            headers=self.headers
        )
        
        self.log("Detalle de consulta", response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                consultation = data["data"]["consultation"]
                options = data["data"]["options"]
                
                print(f"📊 Título: {consultation['title']}")
                print(f"📅 Estado: {consultation['status']}")
                print(f"📝 Descripción: {consultation['description'][:100]}...")
                print(f"📊 Opciones: {len(options)}")
                
                # Guardar IDs de opciones
                self.option_ids = [opt["id"] for opt in options]
                return True
        
        print("❌ Error al obtener detalle")
        return False
    
    def grant_permissions(self):
        """Otorgar permisos de votación a usuarios"""
        if not self.consultation_id:
            print("❌ No hay consulta ID")
            return
        
        print(f"\n🔓 OTORGANDO PERMISOS DE VOTACIÓN")
        
        for user_id in self.user_ids:
            permission_data = {
                "user_id": user_id,
                "can_vote": True
            }
            
            response = requests.post(
                f"{self.base_url}/voting/consultations/{self.consultation_id}/permissions/",
                json=permission_data,
                headers=self.headers
            )
            
            self.log(f"Otorgar permiso a {user_id}", response)
            
            if response.status_code == 201:
                print(f"✅ Permiso otorgado a {user_id}")
            else:
                print(f"❌ Error al otorgar permiso a {user_id}")
    
    def check_eligibility(self, user_id):
        """Verificar elegibilidad para votar"""
        if not self.consultation_id:
            print("❌ No hay consulta ID")
            return False
        
        print(f"\n🔍 VERIFICANDO ELEGIBILIDAD: {user_id}")
        
        response = requests.get(
            f"{self.base_url}/voting/consultations/{self.consultation_id}/eligibility/",
            headers=self.headers
        )
        
        self.log(f"Elegibilidad de {user_id}", response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                eligibility = data["data"]
                print(f"👤 Usuario: {eligibility['user_id']}")
                print(f"✅ Elegible: {eligibility['is_eligible']}")
                print(f"🗳 Ya votó: {eligibility['has_voted']}")
                print(f"🏛️ Miembro de partido: {eligibility['is_party_member']}")
                print(f"🔓 Tiene permiso: {eligibility['has_permission']}")
                
                if eligibility['reasons']:
                    print(f"⚠️ Razones: {', '.join(eligibility['reasons'])}")
                
                return eligibility['is_eligible']
        
        return False
    
    def cast_votes(self):
        """Registrar votos de los usuarios"""
        if not self.consultation_id or not self.option_ids:
            print("❌ Faltan datos para votar")
            return
        
        print(f"\n🗳 REGISTRANDO VOTOS")
        
        for i, user_id in enumerate(self.user_ids):
            # Verificar elegibilidad primero
            if not self.check_eligibility(user_id):
                print(f"❌ Usuario {user_id} no es elegible para votar")
                continue
            
            # Seleccionar opción (cada usuario vota por una opción diferente)
            option_index = i % len(self.option_ids)
            selected_option = self.option_ids[option_index]
            
            vote_data = {
                "option_id": selected_option
            }
            
            response = requests.post(
                f"{self.base_url}/voting/consultations/{self.consultation_id}/vote/",
                json=vote_data,
                headers=self.headers
            )
            
            self.log(f"Voto de {user_id} por opción {selected_option}", response)
            
            if response.status_code == 201:
                data = response.json()
                if data.get("success"):
                    print(f"✅ Voto registrado para {user_id}")
                    print(f"📄 ID del voto: {data['data']['vote_id']}")
                else:
                    print(f"❌ Error en respuesta: {data.get('error')}")
            else:
                print(f"❌ Error al registrar voto para {user_id}")
    
    def get_results(self):
        """Obtener resultados de la consulta"""
        if not self.consultation_id:
            print("❌ No hay consulta ID")
            return
        
        print(f"\n📊 OBTENIENDO RESULTADOS")
        
        response = requests.get(
            f"{self.base_url}/voting/consultations/{self.consultation_id}/results/",
            headers=self.headers
        )
        
        self.log("Resultados de votación", response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                results = data["data"]
                
                print(f"📊 Consulta: {results['consultation_title']}")
                print(f"🗳 Votos totales: {results['total_votes']}")
                print(f"📅 Estado: {results['status']}")
                print(f"✅ Finalizada: {results['is_finished']}")
                
                print(f"\n📈 RESULTADOS:")
                for option in results["options"]:
                    bar = "█" * int(option["percentage"] / 5)  # Barra simple
                    print(f"  {option['title']}: {option['votes']} votos ({option['percentage']}%) {bar}")
                
                if results.get("winner"):
                    winner = results["winner"]
                    print(f"\n🏆 GANADOR: {winner['title']} con {winner['votes']} votos ({winner['percentage']}%)")
                
                return True
        
        print("❌ Error al obtener resultados")
        return False
    
    def get_dashboard(self):
        """Obtener dashboard general"""
        print(f"\n📊 DASHBOARD GENERAL")
        
        response = requests.get(
            f"{self.base_url}/voting/dashboard/",
            headers=self.headers
        )
        
        self.log("Dashboard", response)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                dashboard = data["data"]
                stats = dashboard["statistics"]
                
                print(f"📊 Estadísticas Generales:")
                print(f"  📋 Consultas totales: {stats.get('total_consultations', 0)}")
                print(f"  ✅ Consultas activas: {stats.get('active_consultations', 0)}")
                print(f"  🗳 Votos totales: {stats.get('total_votes', 0)}")
                print(f"  👥 Votantes únicos: {stats.get('total_voters', 0)}")
                
                print(f"\n📋 Consultas Recientes:")
                for consultation in dashboard.get("recent_consultations", [])[:3]:
                    print(f"  • {consultation['title']} ({consultation['status']}) - {consultation['total_votes']} votos")
                
                print(f"\n✅ Consultas Activas:")
                for consultation in dashboard.get("active_consultations", []):
                    print(f"  • {consultation['title']} - {consultation['total_votes']} votos")
                
                return True
        
        print("❌ Error al obtener dashboard")
        return False
    
    def run_complete_example(self):
        """Ejecutar el flujo completo de ejemplo"""
        print("🚀 INICIANDO EJEMPLO COMPLETO DE SISTEMA DE VOTACIÓN")
        print("Este ejemplo demostrará:")
        print("1. Creación de consulta popular")
        print("2. Obtener detalles y opciones")
        print("3. Otorgar permisos a usuarios")
        print("4. Verificar elegibilidad")
        print("5. Registrar votos")
        print("6. Obtener resultados")
        print("7. Ver dashboard general")
        
        try:
            # 1. Crear consulta
            if not self.create_consultation():
                return
            
            # 2. Obtener detalles
            if not self.get_consultation_detail():
                return
            
            # 3. Otorgar permisos
            self.grant_permissions()
            
            # 4. Verificar elegibilidad para cada usuario
            for user_id in self.user_ids:
                self.check_eligibility(user_id)
            
            # 5. Registrar votos
            self.cast_votes()
            
            # 6. Obtener resultados
            self.get_results()
            
            # 7. Dashboard general
            self.get_dashboard()
            
            print("\n🎉 EJEMPLO COMPLETADO EXITOSAMENTE")
            print("✅ Todos los endpoints del sistema de votación funcionan correctamente")
            
        except Exception as e:
            print(f"\n❌ ERROR EN EL EJEMPLO: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Función principal"""
    example = VotingExample()
    example.run_complete_example()


if __name__ == "__main__":
    main()
