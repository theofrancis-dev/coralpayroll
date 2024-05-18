# context_processors.py

from django.shortcuts import get_object_or_404
from .models import Business

def current_business(request):
    business_id = request.session.get('selected_business_id')
    if business_id:
        business = get_object_or_404(Business, pk=business_id)
    else:
        business = None
    return {'current_business': business}
