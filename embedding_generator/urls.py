from django.urls import path
from embedding_generator.views import process


urlpatterns = [
    path('process/', process, name='process_response'),
]
