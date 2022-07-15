from django.views import generic
from .services import ShortenerService
from rest_framework.generics import ListAPIView
from .models import Shortener
from rest_framework import serializers


class ShortenerRedirectView(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        service: ShortenerService = ShortenerService()
        return service.get_url(kwargs.get('shortener', ''))


class ShortenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shortener
        fields = ('shortener', 'url')


class ShortenerList(ListAPIView):
    queryset = Shortener.objects.all()
    serializer_class = ShortenerSerializer
