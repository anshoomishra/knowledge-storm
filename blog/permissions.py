from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.exceptions import PermissionDenied

class DispatchRequest:
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            request.permission_denied = False
            try:
                raise PermissionDenied("You dont have required permissions")
            except Exception:
                request.permission_denied = True

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permission_denied'] = getattr(self.request, 'permission_denied', False)
        return context


class CreateViewPermissionMixin(DispatchRequest):
    def has_permission(self):
        print("in has permission")
        print(f"User: {self.request.user}, Authenticated: {self.request.user.is_authenticated}")

        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_staff:
            return True
        if self.request.user.is_superuser:
            return True

        if self.request.user.has_perm('blog.can_publish_article'):
            return True
        if self.request.user.has_perm('blog.can_create_article'):
            return True
        return False


class DetailViewPermissionMixin(DispatchRequest):
    def has_permission(self):
        print("in has permission")
        print(f"User: {self.request.user}, Authenticated: {self.request.user.is_authenticated}")

        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_staff:
            return True
        if self.request.user.is_superuser:
            return True

        # This should only be used in detail views
        article = self.get_object()
        return self.request.user == article.created_by or self.request.user.has_perm('blog.can_publish_article')


