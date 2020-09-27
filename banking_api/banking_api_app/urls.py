from django.urls import path

from . import views

urlpatterns = [
    path('wallet/', views.WalletList.as_view()),
]
