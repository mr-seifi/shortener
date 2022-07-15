from django.urls import path
from .views import ShortenerRedirectView, ShortenerList


urlpatterns = [
    path('urls/', ShortenerList.as_view()),
    path('<str:shortener>', ShortenerRedirectView.as_view()),
]
