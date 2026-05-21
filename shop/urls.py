from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.home, name="home"),
    path("collection/", views.collection, name="collection"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("chatbot/response/", views.chatbot_response, name="chatbot_response"),
]
