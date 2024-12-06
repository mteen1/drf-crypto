from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from crpt.users.api.views import UserViewSet
from crpt.trading.api.views import TradingPairViewSet, PriceHistoryViewSet, TradeViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("trading-pairs", TradingPairViewSet)
router.register("price-history", PriceHistoryViewSet)
router.register("trades", TradeViewSet)

app_name = "api"
urlpatterns = router.urls
