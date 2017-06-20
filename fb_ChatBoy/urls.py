from django.conf.urls import include, url
from .views import fbc
urlpatterns = [
url(r'^64e773eaadfab2d65ce9a32a9e990ed56e842e53d8d4ad8589/?$',fbc.as_view())

]
