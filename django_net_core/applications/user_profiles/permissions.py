from django.http import HttpResponseForbidden


class UserProfilePermissionMixin:
    def has_permission(self):
        return self.request.user.pk == self.kwargs.get('pk')

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            text = """<div style=\"width: 700px; margin: auto; margin-top: 50px; font-size: 24px;\" >
            <h1 style=\"font-size: 44px;\"> Access forbidden!</h1> 
            <p>You don't have permission to access</p>
            </div>"""
            return HttpResponseForbidden(text)
        return super().dispatch(request, *args, **kwargs)
