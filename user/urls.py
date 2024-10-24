from rest_framework import routers

from . import views

app_name = 'user'


router = routers.DefaultRouter()
router.register(prefix=r'chefs', viewset=views.ChefViewSet, basename='chefs')

urlpatterns = router.urls
