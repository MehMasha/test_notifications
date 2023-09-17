from django.urls import include, path
from rest_framework import routers

from api.views import ClientViewSet, MailingViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)
router.register(
    r'mailings/(?P<mailing_id>\d+)/messages',
    MessageViewSet,
    basename='messages'
)


urlpatterns = [
    path('', include(router.urls))
]
