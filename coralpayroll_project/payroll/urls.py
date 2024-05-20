from django.urls import path
from .views import BusinessListView, client_detail
#from .views import BusinessDetailView
from .views import business_update
from .views import create_business
from .views import create_client, list_clients,update_client,delete_client
from .views import list_staff, business_detail, add_staff
from .views import list_staff, remove_staff, add_earnings
from .views import view_earnings,delete_earning, update_earning;

urlpatterns = [
    path('business/', BusinessListView.as_view(), name='business-list'),
    path('business/<int:business_id>/', business_detail, name='business-detail'),  
    path('business/<int:pk>/update/', business_update, name='business-update'),
    path('business/<int:business_id>/staff/', list_staff, name='list_staff'),
    path('business/<int:business_id>/remove_staff/<int:person_id>/', remove_staff, name='remove_staff'),
    path('business/<int:business_id>/add_earnings/<int:person_id>/', add_earnings, name='add_earnings'),
    path('create-business/', create_business, name='create-business'), 
    path('business/<int:business_id>/view_earnings/<int:person_id>/', view_earnings, name='view_earnings'),
    path('business/<int:business_id>/delete_earning/<int:earning_id>/', delete_earning, name='delete_earning'),
    path('business/<int:business_id>/update_earning/<int:earning_id>/', update_earning, name='update_earning'),

    path('clients/', list_clients, name='list-clients'),
    path('clients/create', create_client, name='create-client'),
    path('clients/add_staff/<int:person_id>/', add_staff, name='add_staff'),
    path('clients/<int:pk>/', client_detail, name='client-detail'),
    path('clients/<int:pk>/update/', update_client, name='update-client'),
    path('clients/<int:pk>/delete/', delete_client, name='delete-client'),
    
]
