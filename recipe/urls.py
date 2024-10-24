from rest_framework import routers

from . import views

app_name = 'recipe'


router = routers.DefaultRouter()
router.register(prefix=r'recipes', viewset=views.RecipeViewSet, basename='recipes')
urlpatterns = router.urls
