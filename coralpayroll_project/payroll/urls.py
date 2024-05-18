from django.urls import path
from .views import BusinessListView, client_detail
#from .views import BusinessDetailView
from .views import business_update
from .views import create_business
from .views import create_client, list_clients,update_client,delete_client
from .views import list_staff, business_detail, add_staff

urlpatterns = [
    path('business/', BusinessListView.as_view(), name='business-list'),
    path('business/<int:business_id>/', business_detail, name='business-detail'),  
     path('business/<int:pk>/update/', business_update, name='business-update'),
     path('business/<int:business_id>/staff/', list_staff, name='list_staff'),
     path('create-business/', create_business, name='create-business'),     

     path('clients/', list_clients, name='list-clients'),
     path('clients/create', create_client, name='create-client'),
     path('clients/add_staff/<int:person_id>/', add_staff, name='add_staff'),
     path('clients/<int:pk>/', client_detail, name='client-detail'),
     path('clients/<int:pk>/update/', update_client, name='update-client'),
     path('clients/<int:pk>/delete/', delete_client, name='delete-client'),
    
]
