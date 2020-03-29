from django.db.models import F
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView
from goods_app.models import Goods
import time
from django.db import transaction, DataError, IntegrityError
from django.views.decorators.http import require_http_methods


def _get_goods_dict(request):
    """
    根据session得到 {goods: num} 的字典
    :param request: request
    :return: goods <class: dict>
    """
    goods_dict = dict()
    for k in request.session.keys():
        if k.isdigit():
            goods = Goods.objects.get(pk=int(k))
            goods_dict[goods] = request.session[k]
    return goods_dict


def _get_total(request):
    """
    计算合计价钱
    :param request: request
    :return: total <class: int>
    """
    total = 0
    goods_dict = _get_goods_dict(request)
    for goods in goods_dict:
        total += goods.price * goods_dict[goods]
    return total


def _clear_goods_func(request):
    """
    调用此函数可清空购物车
    :param request: request
    :return: None
    """
    for k in list(request.session.keys()):
        if k.isdigit():
            del request.session[k]


def _check_goods_inventory(request):
    """
    校验商品库存
    :return: 如果库存足够能够购买，则返回空列表，否则返回库存不够的商品对象组成的列表
    """
    not_enough_goods = []
    goods_dict = _get_goods_dict(request)
    for goods in goods_dict:
        if goods.inventory < goods_dict[goods]:
            not_enough_goods.append(goods)
    return not_enough_goods


class AllGoods(ListView):
    """商品列表页"""
    template_name = 'goods/all_goods.html'
    queryset = Goods.objects.filter(parent=None)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['selected_goods'] = _get_goods_dict(self.request)
        return context


def add_goods(request, goods_id):
    """
    添加商品， 用session记录添加商品及购物车内的商品，在商品列表页展示出来
    :param goods_id: 商品id
    :return: redirect response
    """
    request.session[goods_id] = request.session.get(str(goods_id), 0) + 1
    return redirect('goods:all_goods')


def sub_goods(request, goods_id):
    """
    减少商品， 用session记录添加商品及购物车内的商品，在商品列表页展示出来
    :param goods_id: 商品id
    :return: redirect response
    """
    num = request.session.get(str(goods_id), 0)
    if num:
        if num == 1:
            del request.session[str(goods_id)]
        else:
            request.session[goods_id] = num - 1
    return redirect('goods:all_goods')


def clear_goods(request):
    """
    清空购物车
    :return: redirect response
    """
    _clear_goods_func(request)
    return redirect('goods:all_goods')


def settle(request):
    """
    结算
    :return: response
    """
    context = dict()
    context['total'] = _get_total(request)
    context['selected_goods'] = _get_goods_dict(request)
    context['not_enough_goods'] = _check_goods_inventory(request)
    return render(request, 'goods/settle.html', context)


@require_http_methods(['POST'])
@transaction.atomic
def pay(request):
    """
    支付界面
    :return: response
    """
    # 修改库存量
    goods_dict = _get_goods_dict(request)
    if request.POST['pay'] != '确认支付' or not goods_dict:
        raise Http404
    # time.sleep(10)
    try:
        with transaction.atomic():
            for goods in goods_dict:
                Goods.objects.filter(pk=goods.pk).update(inventory=F('inventory')-goods_dict[goods])
    except (DataError, IntegrityError):
        return redirect('goods:settle')
    total = _get_total(request)
    _clear_goods_func(request)
    return HttpResponse(f'支付成功({total}元),返回<a href="/goods/">商品列表</a>')
