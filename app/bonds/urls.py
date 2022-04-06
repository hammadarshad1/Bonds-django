from rest_framework.routers import DefaultRouter

from bonds import views


app_name = "bond"

router = DefaultRouter()
router.register(r'sell', views.SellBondViewset, basename='sell')
router.register(r'list', views.ListBondsViewset, basename='list')
router.register(r'buy', views.BondBuyViewset, basename="buy")

urlpatterns = router.urls
