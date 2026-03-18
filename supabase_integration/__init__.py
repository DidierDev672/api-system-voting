"""
Supabase integration package for the API system
"""

from supabase_integration.services import (
    BancadaSupabaseService,
    get_bancada_service,
)

from supabase_integration.base_services import (
    SupabaseService,
    party_members_service,
    political_parties_service,
    users_service,
    consultations_service,
)

__all__ = [
    "BancadaSupabaseService",
    "get_bancada_service",
    "SupabaseService",
    "party_members_service",
    "political_parties_service",
    "users_service",
    "consultations_service",
]
