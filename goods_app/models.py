from django.db import models

# Create your models here.


class Goods(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True, verbose_name='商品名称')
    price = models.FloatField(null=True, verbose_name='价格')
    inventory = models.PositiveSmallIntegerField(null=False, default=0, verbose_name='库存量')
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, related_name='kinds', verbose_name='所属种类')

    def __str__(self):
        return self.name
