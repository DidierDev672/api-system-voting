from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from system_voting.src.bancada.application.use_cases import (
    GetAllBancadasUseCase,
    GetBancadaByIdUseCase,
    CreateBancadaUseCase,
    UpdateBancadaUseCase,
    DeleteBancadaUseCase,
    GetBancadasByMiembroUseCase,
    GetBancadasByPartidoUseCase,
)
from system_voting.src.bancada.infrastructure.adapters.supabase_bancada_repository import (
    SupabaseBancadaRepository,
)
from system_voting.src.bancada.domain.entities.bancada import Bancada
from system_voting.src.bancada.domain.value_objects.tipo_curul import (
    TipoCurul,
    ComisionPermanente,
)
from ..serializers import BancadaSerializer, BancadaListSerializer


class BancadaRepositorySingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SupabaseBancadaRepository()
        return cls._instance


class BancadaListCreateView(APIView):
    """Vista para listar y crear bancadas"""

    def get(self, request):
        repository = BancadaRepositorySingleton.get_instance()
        use_case = GetAllBancadasUseCase(repository)
        bancadas = use_case.execute()
        serializer = BancadaListSerializer(bancadas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BancadaSerializer(data=request.data)
        if serializer.is_valid():
            bancada = Bancada(
                id_miembro=str(serializer.validated_data["id_miembro"]),
                id_partido=str(serializer.validated_data["id_partido"]),
                tipo_curul=TipoCurul(serializer.validated_data["tipo_curul"]),
                fin_periodo=serializer.validated_data["fin_periodo"],
                declaraciones_bienes=serializer.validated_data.get(
                    "declaraciones_bienes", ""
                ),
                antecedentes_siri_sirus=serializer.validated_data.get(
                    "antecedentes_siri_sirus", "Sin antecedentes"
                ),
                comision_permanente=ComisionPermanente(
                    serializer.validated_data["comision_permanente"]
                ),
                correo_institucional=serializer.validated_data["correo_institucional"],
                profesion=serializer.validated_data["profesion"],
            )
            repository = BancadaRepositorySingleton.get_instance()
            use_case = CreateBancadaUseCase(repository)
            created = use_case.execute(bancada)
            response_serializer = BancadaSerializer(created)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BancadaDetailView(APIView):
    """Vista para obtener, actualizar y eliminar una bancada por ID"""

    def get(self, request, pk):
        repository = BancadaRepositorySingleton.get_instance()
        use_case = GetBancadaByIdUseCase(repository)
        bancada = use_case.execute(pk)
        if bancada:
            serializer = BancadaSerializer(bancada)
            return Response(serializer.data)
        return Response(
            {"error": "Bancada no encontrada"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, pk):
        serializer = BancadaSerializer(data=request.data)
        if serializer.is_valid():
            bancada = Bancada(
                id_miembro=str(serializer.validated_data["id_miembro"]),
                id_partido=str(serializer.validated_data["id_partido"]),
                tipo_curul=TipoCurul(serializer.validated_data["tipo_curul"]),
                fin_periodo=serializer.validated_data["fin_periodo"],
                declaraciones_bienes=serializer.validated_data.get(
                    "declaraciones_bienes", ""
                ),
                antecedentes_siri_sirus=serializer.validated_data.get(
                    "antecedentes_siri_sirus", "Sin antecedentes"
                ),
                comision_permanente=ComisionPermanente(
                    serializer.validated_data["comision_permanente"]
                ),
                correo_institucional=serializer.validated_data["correo_institucional"],
                profesion=serializer.validated_data["profesion"],
            )
            repository = BancadaRepositorySingleton.get_instance()
            use_case = UpdateBancadaUseCase(repository)
            try:
                updated = use_case.execute(pk, bancada)
                response_serializer = BancadaSerializer(updated)
                return Response(response_serializer.data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        repository = BancadaRepositorySingleton.get_instance()
        use_case = DeleteBancadaUseCase(repository)
        deleted = use_case.execute(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"error": "Bancada no encontrada"}, status=status.HTTP_404_NOT_FOUND
        )


class BancadaByMiembroView(APIView):
    """Vista para obtener bancadas por ID de miembro"""

    def get(self, request, id_miembro):
        repository = BancadaRepositorySingleton.get_instance()
        use_case = GetBancadasByMiembroUseCase(repository)
        try:
            bancadas = use_case.execute(id_miembro)
            serializer = BancadaListSerializer(bancadas, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BancadaByPartidoView(APIView):
    """Vista para obtener bancadas por ID de partido"""

    def get(self, request, id_partido):
        repository = BancadaRepositorySingleton.get_instance()
        use_case = GetBancadasByPartidoUseCase(repository)
        try:
            bancadas = use_case.execute(id_partido)
            serializer = BancadaListSerializer(bancadas, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
