from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoginView, logout_view, profile_view, IgrejaViewSet, CampusViewSet, UserViewSet, PapelViewSet

router = DefaultRouter()
router.register(r'igrejas', IgrejaViewSet, basename='igreja')
router.register(r'campus', CampusViewSet, basename='campus')
router.register(r'usuarios', UserViewSet, basename='usuario')
router.register(r'papeis', PapelViewSet, basename='papel')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('', include(router.urls)),
]
