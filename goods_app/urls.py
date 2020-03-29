from django.urls import path, include

from goods_app import views

app_name = 'goods'
urlpatterns = [
    path('', views.AllGoods.as_view(), name='all_goods'),
    path('add_goods<int:goods_id>/', views.add_goods, name='add_goods'),
    path('sub_goods<int:goods_id>/', views.sub_goods, name='sub_goods'),
    path('clear_goods/', views.clear_goods, name='clear_goods'),
    path('settle/', views.settle, name='settle'),
    path('pay/', views.pay, name='pay'),
]
