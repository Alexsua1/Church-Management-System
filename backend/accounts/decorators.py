from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(*allowed_roles):
    """Restrict a view to specific User.Role values (superusers always allowed)."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied("You do not have permission to access this page.")
        return _wrapped
    return decorator


admin_required = role_required("ADMIN")
pastor_required = role_required("ADMIN", "PASTOR")
secretary_required = role_required("ADMIN", "SECRETARY")
finance_required = role_required("ADMIN", "FINANCE_OFFICER")
staff_required = role_required("ADMIN", "PASTOR", "SECRETARY", "FINANCE_OFFICER")
