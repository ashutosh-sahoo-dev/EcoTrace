from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("assets/", views.asset_list_view, name="asset_list"),
    path("assets/add/", views.add_asset_view, name="add_asset"),
    path("assets/<str:asset_id>/", views.asset_detail_view, name="asset_detail"),
    path("responsible-ai/", views.responsible_ai_view, name="responsible_ai"),
]
