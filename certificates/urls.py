from django.urls import path
from . import views

urlpatterns = [
    path(
        "my-certificates/",
        views.my_certificates,
        name="my_certificates"
    ),
    path(
        "certificate/<int:certificate_id>/",
        views.view_certificate,
        name="view_certificate"
    ),
]