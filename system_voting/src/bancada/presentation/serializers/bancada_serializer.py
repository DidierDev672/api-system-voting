from rest_framework import serializers
from system_voting.src.bancada.domain.value_objects.tipo_curul import (
    TipoCurul,
    ComisionPermanente,
)


class BancadaSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    id_miembro = serializers.UUIDField(
        required=True, help_text="UUID del miembro del consejo municipal"
    )
    id_partido = serializers.UUIDField(
        required=True, help_text="UUID del partido político"
    )
    tipo_curul = serializers.ChoiceField(
        choices=TipoCurul.values(), default=TipoCurul.ORDINARIA.value
    )
    fin_periodo = serializers.DateField(required=True)
    declaraciones_bienes = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    antecedentes_siri_sirus = serializers.CharField(
        required=False,
        allow_blank=True,
        default="Sin antecedentes",
        label="Antecedentes SIRI/SIRHUS",
    )
    comision_permanente = serializers.ChoiceField(
        choices=ComisionPermanente.values(), default=ComisionPermanente.GOBIERNO.value
    )
    correo_institucional = serializers.EmailField(required=True)
    profesion = serializers.CharField(required=True, max_length=200)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class BancadaListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    id_miembro = serializers.UUIDField()
    id_partido = serializers.UUIDField()
    tipo_curul = serializers.CharField()
    fin_periodo = serializers.DateField()
    declaraciones_bienes = serializers.CharField()
    antecedentes_siri_sirus = serializers.CharField()
    comision_permanente = serializers.CharField()
    correo_institucional = serializers.EmailField()
    profesion = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
