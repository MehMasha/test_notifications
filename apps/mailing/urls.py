from django.urls import include, path
from rest_framework import routers

from apps.mailing.views import MailingViewSet, MessageViewSet

app_name = 'mailing'

router = routers.DefaultRouter()
router.register(r'mailings', MailingViewSet)
router.register(
    r'mailings/(?P<mailing_id>\d+)/messages',
    MessageViewSet,
    basename='messages'
)


urlpatterns = [
    path('', include(router.urls))
]
