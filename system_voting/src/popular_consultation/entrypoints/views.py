"""
Vistas (Endpoints) para Consulta Popular
Capa de Presentación - Maneja las peticiones HTTP
"""

import json
import logging
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from system_voting.src.popular_consultation.domain.entities.consultation import (
    CreateConsultationCommand,
    UpdateConsultationCommand,
)
from system_voting.src.popular_consultation.application.services.consultation_service import (
    ConsultationService,
)

logger = logging.getLogger(__name__)

consultation_service = ConsultationService()


@method_decorator(csrf_exempt, name="dispatch")
class ConsultationListCreateView(View):
    """Vista para listar y crear consultas populares"""

    def get(self, request):
        """Obtener todas las consultas"""
        logger.info("=== VIEW: GET /consultations - Listar todas ===")

        try:
            consultations = consultation_service.get_all_consultations()

            data = [
                {
                    "id": c.id,
                    "title": c.title,
                    "description": c.description,
                    "questions": [
                        {
                            "id": q.id,
                            "text": q.text,
                            "question_type": q.question_type.value
                            if hasattr(q.question_type, "value")
                            else q.question_type,
                            "options": q.options,
                            "required": q.required,
                        }
                        for q in c.questions
                    ],
                    "proprietary_representation": c.proprietary_representation,
                    "status": c.status.value
                    if hasattr(c.status, "value")
                    else c.status,
                    "created_at": c.created_at,
                    "updated_at": c.updated_at,
                }
                for c in consultations
            ]

            logger.info(f"=== VIEW: Retornando {len(data)} consultas ===")
            return JsonResponse(data, safe=False, status=200)

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request):
        """Crear una nueva consulta"""
        logger.info("=== VIEW: POST /consultations - Crear consulta ===")

        try:
            body = json.loads(request.body)

            command = CreateConsultationCommand(
                title=body.get("title", ""),
                description=body.get("description", ""),
                questions=body.get("questions", []),
                proprietary_representation=body.get("proprietary_representation", ""),
                status=body.get("status", "draft"),
            )

            consultation = consultation_service.create_consultation(command)

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "description": consultation.description,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "question_type": q.question_type.value
                        if hasattr(q.question_type, "value")
                        else q.question_type,
                        "options": q.options,
                        "required": q.required,
                    }
                    for q in consultation.questions
                ],
                "proprietary_representation": consultation.proprietary_representation,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "created_at": consultation.created_at,
                "updated_at": consultation.updated_at,
            }

            logger.info(f"=== VIEW: Consulta creada: {consultation.id} ===")
            return JsonResponse(data, status=201)

        except ValueError as ve:
            logger.warning(f"=== VIEW VALIDATION ERROR: {str(ve)} ===")
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ConsultationDetailView(View):
    """Vista para obtener, actualizar y eliminar una consulta específica"""

    def get(self, request, consultation_id):
        """Obtener una consulta por ID"""
        logger.info(f"=== VIEW: GET /consultations/{consultation_id} ===")

        try:
            consultation = consultation_service.get_consultation(consultation_id)

            if not consultation:
                return JsonResponse({"error": "Consulta no encontrada"}, status=404)

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "description": consultation.description,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "question_type": q.question_type.value
                        if hasattr(q.question_type, "value")
                        else q.question_type,
                        "options": q.options,
                        "required": q.required,
                    }
                    for q in consultation.questions
                ],
                "proprietary_representation": consultation.proprietary_representation,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "created_at": consultation.created_at,
                "updated_at": consultation.updated_at,
            }

            return JsonResponse(data, status=200)

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, consultation_id):
        """Actualizar una consulta"""
        logger.info(f"=== VIEW: PUT /consultations/{consultation_id} ===")

        try:
            body = json.loads(request.body)

            command = UpdateConsultationCommand(
                id=consultation_id,
                title=body.get("title"),
                description=body.get("description"),
                questions=body.get("questions"),
                proprietary_representation=body.get("proprietary_representation"),
                status=body.get("status"),
            )

            consultation = consultation_service.update_consultation(command)

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "description": consultation.description,
                "questions": [
                    {
                        "id": q.id,
                        "text": q.text,
                        "question_type": q.question_type.value
                        if hasattr(q.question_type, "value")
                        else q.question_type,
                        "options": q.options,
                        "required": q.required,
                    }
                    for q in consultation.questions
                ],
                "proprietary_representation": consultation.proprietary_representation,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "created_at": consultation.created_at,
                "updated_at": consultation.updated_at,
            }

            logger.info(f"=== VIEW: Consulta actualizada: {consultation.id} ===")
            return JsonResponse(data, status=200)

        except ValueError as ve:
            logger.warning(f"=== VIEW VALIDATION ERROR: {str(ve)} ===")
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, consultation_id):
        """Eliminar una consulta"""
        logger.info(f"=== VIEW: DELETE /consultations/{consultation_id} ===")

        try:
            result = consultation_service.delete_consultation(consultation_id)

            if result:
                logger.info(f"=== VIEW: Consulta eliminada: {consultation_id} ===")
                return JsonResponse(
                    {"message": "Consulta eliminada exitosamente"}, status=200
                )
            else:
                return JsonResponse(
                    {"error": "No se pudo eliminar la consulta"}, status=400
                )

        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ConsultationPublishView(View):
    """Vista para publicar una consulta"""

    def post(self, request, consultation_id):
        """Publicar una consulta"""
        logger.info(f"=== VIEW: POST /consultations/{consultation_id}/publish ===")

        try:
            consultation = consultation_service.publish_consultation(consultation_id)

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "message": "Consulta publicada exitosamente",
            }

            logger.info(f"=== VIEW: Consulta publicada: {consultation.id} ===")
            return JsonResponse(data, status=200)

        except ValueError as ve:
            logger.warning(f"=== VIEW ERROR: {str(ve)} ===")
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ConsultationCloseView(View):
    """Vista para cerrar una consulta"""

    def post(self, request, consultation_id):
        """Cerrar una consulta"""
        logger.info(f"=== VIEW: POST /consultations/{consultation_id}/close ===")

        try:
            consultation = consultation_service.close_consultation(consultation_id)

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "message": "Consulta cerrada exitosamente",
            }

            logger.info(f"=== VIEW: Consulta cerrada: {consultation.id} ===")
            return JsonResponse(data, status=200)

        except ValueError as ve:
            logger.warning(f"=== VIEW ERROR: {str(ve)} ===")
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class ConsultationUpdateStatusView(View):
    """Vista para actualizar el estado de una consulta"""

    def patch(self, request, consultation_id):
        """Actualizar el estado de una consulta"""
        logger.info(f"=== VIEW: PATCH /consultations/{consultation_id}/status ===")

        try:
            body = json.loads(request.body)
            new_status = body.get("status")

            if not new_status:
                return JsonResponse(
                    {"error": "El campo 'status' es requerido"}, status=400
                )

            consultation = consultation_service.update_status(
                consultation_id, new_status
            )

            data = {
                "id": consultation.id,
                "title": consultation.title,
                "status": consultation.status.value
                if hasattr(consultation.status, "value")
                else consultation.status,
                "message": "Estado actualizado exitosamente",
            }

            logger.info(f"=== VIEW: Estado actualizado: {consultation.id} ===")
            return JsonResponse(data, status=200)

        except ValueError as ve:
            logger.warning(f"=== VIEW VALIDATION ERROR: {str(ve)} ===")
            return JsonResponse({"error": str(ve)}, status=400)
        except Exception as e:
            logger.error(f"=== VIEW ERROR: {str(e)} ===")
            return JsonResponse({"error": str(e)}, status=500)
