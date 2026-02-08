from system_voting.src.party_members.domain.value_objects.document_type import DocumentType


class PartyMemberValidator:

    @staticmethod
    def validate(data):
        if not DocumentType.is_valid(data["document_type"]):
            raise ValueError("Tipo de documento no válido")

        if not data["consent"]:
            raise ValueError("Debe aceptar la afiliación política")

        if not data["data_authorization"]:
            raise ValueError("Debe autorizar tratamiento de datos")