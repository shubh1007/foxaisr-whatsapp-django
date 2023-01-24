from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.index, name="index")
]



# from django.urls import re_path
# from django.contrib import admin

# from .views import (
#     FacebookWebhookView
#     )
# WEBHOOK_ENDPOINT = "45c66b3a06d11ad094a28d752f174d756d44e8cc242f44fe05d6193980e0"
# app_name ='bot_webhooks'
# urlpatterns = [
#     re_path(r'^45c66b3a06d11ad094a28d752f174d756d44e8cc242f44fe05d6193980e0/$', FacebookWebhookView.as_view(), name='webhook'),
# ]

# # replace <string_endpoint> with the one you created above


