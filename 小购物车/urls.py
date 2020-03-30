"""小购物车 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from goods_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.AllGoods.as_view()),
    path('favicon.ico', RedirectView.as_view(url='/static/ico1.jpg')),
    path('goods/', include('goods_app.urls')),
]


from django.conf import settings
if settings.DEBUG is False:
    from django.views import static
    from django.conf.urls import url
    urlpatterns += [url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static')]
