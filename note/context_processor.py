from django.conf import settings
from .models import Note,Category


def global_categories(request):
    categories = None
    if request.user.is_authenticated:
        categories = Category.objects.filter(user=request.user)

    return {

        'categories': categories
    }
