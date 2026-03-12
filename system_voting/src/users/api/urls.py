from django.urls import path
from .views import RegisterUserView, ListUsersView, GetUserView
from .permission_views import (
    CreatePermissionView,
    UserPermissionView,
    UpdatePermissionView,
    AssignPermissionView,
    RevokePermissionView,
    ListPermissionsView,
    RolesAndPermissionsView,
    CheckPermissionView,
)
from .supabase_auth_views import (
    SupabaseLoginView,
    SupabaseRegisterView,
    SupabaseLogoutView,
    SupabaseProfileView,
    SupabaseRefreshTokenView,
)
from .auth_views import CompleteUserProfileView
from .voting_views import (
    ConsultationListView,
    ConsultationDetailView,
    CreateConsultationView,
    VoteView,
    VotingEligibilityView,
    ConsultationResultsView,
    VotingPermissionView,
    VotingDashboardView,
    UserVotingHistoryView,
)

app_name = "users"

urlpatterns = [
    # Endpoints de autenticación con Supabase
    path("auth/login/", SupabaseLoginView.as_view(), name="supabase_login"),
    path("auth/register/", SupabaseRegisterView.as_view(), name="supabase_register"),
    path("auth/logout/", SupabaseLogoutView.as_view(), name="supabase_logout"),
    path("auth/profile/", SupabaseProfileView.as_view(), name="supabase_profile"),
    path("auth/refresh/", SupabaseRefreshTokenView.as_view(), name="supabase_refresh"),
    path(
        "auth/complete-profile/",
        CompleteUserProfileView.as_view(),
        name="complete_profile",
    ),
    # Endpoints de votación
    path("voting/dashboard/", VotingDashboardView.as_view(), name="voting_dashboard"),
    path(
        "voting/consultations/",
        ConsultationListView.as_view(),
        name="consultation_list",
    ),
    path(
        "voting/consultations/create/",
        CreateConsultationView.as_view(),
        name="create_consultation",
    ),
    path(
        "voting/consultations/<uuid:consultation_id>/",
        ConsultationDetailView.as_view(),
        name="consultation_detail",
    ),
    path(
        "voting/consultations/<uuid:consultation_id>/vote/",
        VoteView.as_view(),
        name="cast_vote",
    ),
    path(
        "voting/consultations/<uuid:consultation_id>/eligibility/",
        VotingEligibilityView.as_view(),
        name="voting_eligibility",
    ),
    path(
        "voting/consultations/<uuid:consultation_id>/results/",
        ConsultationResultsView.as_view(),
        name="consultation_results",
    ),
    path(
        "voting/consultations/<uuid:consultation_id>/permissions/",
        VotingPermissionView.as_view(),
        name="voting_permissions",
    ),
    path(
        "voting/history/", UserVotingHistoryView.as_view(), name="user_voting_history"
    ),
    # Endpoints de usuarios (legacy)
    path("register/", RegisterUserView.as_view(), name="register_user"),
    path("", ListUsersView.as_view(), name="list_users"),
    path("<uuid:user_id>/", GetUserView.as_view(), name="get_user"),
    # Endpoints de permisos
    path("permissions/", CreatePermissionView.as_view(), name="create_permission"),
    path("permissions/list/", ListPermissionsView.as_view(), name="list_permissions"),
    path(
        "permissions/info/",
        RolesAndPermissionsView.as_view(),
        name="roles_permissions_info",
    ),
    path("permissions/check/", CheckPermissionView.as_view(), name="check_permission"),
    path(
        "permissions/assign/", AssignPermissionView.as_view(), name="assign_permission"
    ),
    path(
        "permissions/<uuid:permission_id>/",
        UpdatePermissionView.as_view(),
        name="update_permission",
    ),
    path(
        "<uuid:user_id>/permissions/",
        UserPermissionView.as_view(),
        name="user_permissions",
    ),
    path(
        "<uuid:user_id>/permissions/<str:permission>/",
        RevokePermissionView.as_view(),
        name="revoke_permission",
    ),
]
