from system_voting.src.popular_consultations.domain.value_objects.consultation_level import ConsultationLevel


class ConsultationValidator:

    @staticmethod
    def validate(data):
        if "?" not in data["question"]:
            raise ValueError("La pregunta debe ser clara y cerrada")

        if len(data["question"]) > 300:
            raise ValueError("La pregunta excede el limite permitido")

        if not ConsultationLevel.is_valid(data["level"]):
            raise ValueError("Nivel de consulta inválido")