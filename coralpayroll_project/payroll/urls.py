from django.urls import path
from .views import BusinessListView
from .views import BusinessDetailView
from .views import business_update
from .views import create_business

urlpatterns = [
    path('business/', BusinessListView.as_view(), name='business-list'),
    path('business/<int:pk>/', BusinessDetailView.as_view(), name='business-detail'),  # Add this line
     path('business/<int:pk>/update/', business_update, name='business-update'),
     #path('business/<int:pk>/update/', business_update, name='business-update'),  # Define URL pattern for update view
     path('create-business/', create_business, name='create-business'),
    # Add other urls as needed
]
