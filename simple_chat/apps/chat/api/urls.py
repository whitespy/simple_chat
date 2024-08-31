from rest_framework.routers import SimpleRouter

from .views import ThreadViewSet

router = SimpleRouter()
router.register("threads", ThreadViewSet)

urlpatterns = router.urls
