import uuid
from django.db import models
from system_voting.src.bancada.domain.value_objects.tipo_curul import (
    TipoCurul,
    ComisionPermanente,
)


class BancadaModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_miembro = models.UUIDField(
        db_index=True, help_text="UUID del miembro del consejo municipal"
    )
    id_partido = models.UUIDField(db_index=True, help_text="UUID del partido político")
    tipo_curul = models.CharField(
        max_length=50, choices=TipoCurul.choices(), default=TipoCurul.ORDINARIA.value
    )
    fin_periodo = models.DateField()
    declaraciones_bienes = models.TextField(blank=True, default="")
    antecedentes_siri_sirus = models.TextField(
        blank=True, default="Sin antecedentes", verbose_name="Antecedentes SIRI/SIRHUS"
    )
    comision_permanente = models.CharField(
        max_length=100,
        choices=ComisionPermanente.choices(),
        default=ComisionPermanente.GOBIERNO.value,
    )
    correo_institucional = models.EmailField()
    profesion = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bancada"
        ordering = ["-created_at"]
        verbose_name = "Bancada"
        verbose_name_plural = "Bancadas"

    def __str__(self):
        return f"Bancada {self.id} - Miembro {self.id_miembro}"
