from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from rest_framework import routers

from accounts.views import UserViewSet
from companies.views import CompanyViewset
from reviews.views import ReviewList, ReviewDetail


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'companies', CompanyViewset, basename='companies')


urlpatterns = [
    path('', RedirectView.as_view(url='api/'), name='go-to-api'),
    path('api/users/<slug:username>/reviews/', ReviewList.as_view(), name='users-reviews-list'),
    path('api/users/<slug:username>/reviews/<int:pk>/', ReviewDetail.as_view(), name='users-reviews-detail'),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
