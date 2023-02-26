from django.urls import path
from .views import PassAPIView, reverse_to_submit


urlpatterns = [
    path('submitData/', PassAPIView.as_view({'post': 'post', 'get': 'get_records_by_user'}), name='submitData'),
    path('submitData/<int:pk>', PassAPIView.as_view({'get': 'get_one', 'patch': 'edit_one'})),
    path('', reverse_to_submit),
]