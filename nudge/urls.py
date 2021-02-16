from nudge import handlers, hyperdjango

# urlpatterns = (
#     url(r'^$', views.hello),
# )

urlpatterns = (
    hyperdjango.resource(
        r"^collect$", "POST", handlers.collect, "dashboard.html"
    ),
    hyperdjango.resource(r"^$", "GET", handlers.dashboard, "dashboard.html"),
)
