from nudge import handlers
from nudge import hyperdjango
from nudge import views
from django.conf.urls import url


# urlpatterns = (
#     url(r'^$', views.hello),
# )

urlpatterns = (
    hyperdjango.resource(r'^collect$', 'POST', handlers.collect, 'dashboard.html'),
    hyperdjango.resource(r'^$', 'GET', handlers.dashboard, 'dashboard.html'),
)
