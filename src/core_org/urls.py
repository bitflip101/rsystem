from django.urls import path
from . import views

app_name = 'core_org'

urlpatterns = [
    path('management/', views.org_management_dashboard, name='dashboard'),
    path('asset/new', views.asset_create, name = 'asset-create'),
    path('asset/<int:asset_id>/unit/add/', views.unit_add_to_asset, name='unit-add-to-asset'),
    path('unit/<int:pk>/edit/', views.unit_edit, name='unit-edit'),
    path('unit/<int:pk>/staff', views.unit_staff_list, name='unit-staff'),
    # path('asset/<int:pk>/edit/', views.asset_edit, name='asset-edit'),
]