from django.urls import path
from .views import (HomeView, 
                    SubstationView, 
                    MCCView, 
                    NodeView, 
                    AddNodeView, 
                    UpdateNodeView, 
                    SearchNodeView, 
                    NodeDeleteView,
                    NodeDeleteConfirmView,
                    LoginUserView, 
                    logout_user)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('substation/<int:sub_num>/', SubstationView.as_view(), name='substation'),
    path('mcc/<slug:mcc_slug>/', MCCView.as_view(), name='mcc'),
    path('node/<slug:slug>/', NodeView.as_view(), name='node-detail'),
    path('add_node/', AddNodeView.as_view(), name='add_node'),
    path('edit/<slug:slug>/', UpdateNodeView.as_view(), name='edit_node'),
    path('search/', SearchNodeView.as_view(), name='search_node'),
    path('node/<slug:slug>/delete/', NodeDeleteView.as_view(), name='node_delete'),
    path('node_delete_confirm/', NodeDeleteConfirmView.as_view(), name='node_delete_confirm'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user, name='logout_user'),
]
