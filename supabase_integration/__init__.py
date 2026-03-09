"""
Supabase integration package for the API system
"""

from .services import (
    SupabaseConfig,
    SupabaseService,
    political_parties_service,
    party_members_service,
    users_service,
    consultations_service
)

__all__ = [
    'SupabaseConfig',
    'SupabaseService', 
    'political_parties_service',
    'party_members_service',
    'users_service',
    'consultations_service'
]
