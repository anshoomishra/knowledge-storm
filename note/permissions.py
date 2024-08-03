from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

class UserIsOwnerMixin:
    """
    Mixin to ensure that the logged-in user is the owner of the object.
    """

    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=kwargs['pk'])
        if obj.user != request.user:
            return HttpResponseForbidden("You are not allowed to access this object.")
        return super().dispatch(request, *args, **kwargs)
