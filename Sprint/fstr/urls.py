from django.urls import path
from .views import (
    PassDDetailView
)

path('<int:pk>', (PassDDetailView.as_view()), name='pass_detail'),
