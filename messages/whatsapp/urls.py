from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.whatsAppWebHook, name="whatsapp-webhook"),
    path("sendOTP", view=views.sendOTP, name="sendotp"),
    path("addtemplate", view=views.addTemplate, name="addtemplate"),
]