from django.urls import path

from . import views

urlpatterns = [
    path('wallets/', views.WalletList.as_view()),
    path('wallets/<int:pk>/', views.WalletDetail.as_view()),
    path('cards/', views.CardList.as_view()),
    path('cards/<int:pk>/', views.CardDetail.as_view()),
    path('cards/<int:pk>/block', views.BlockCard.as_view()),
    path('cards/<int:pk>/unblock', views.UnblockCard.as_view()),
    path('transfers/', views.TransferList.as_view()),
    path('transfers/<int:pk>/', views.TransferDetail.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/<int:pk>/cards/', views.UserCards.as_view()),
    path('users/<int:pk>/wallets/', views.UserWallets.as_view()),
]
