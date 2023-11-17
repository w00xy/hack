import re

from django.db import models
import dadata
from django.core.exceptions import ValidationError

# Create your models here.

token = "38d51ccf58bf0b9c95fcbb47ab8db3ccceeeea08"
secret = "b92f02f9f01388d0e657e3dc2cf48946e7ac44b5"

class User(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone = models.CharField(max_length=18, verbose_name='Номер Телефона')
    password = models.CharField(max_length=255, verbose_name='Пароль')

    def __str__(self):
        return self.name

    client = dadata.Dadata(token, secret)

    def clean(self):
        client = dadata.Dadata(token, secret)
        correct_phone = re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', str(self.phone))
        if correct_phone is not None:
            result = client.clean(name="phone", source=str(self.phone))
            self.phone = result['phone']
        else:
            raise ValidationError('Неправильный номер телефона')

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем метод clean() перед сохранением объекта
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Transactions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название транзакции')
    tags = models.ForeignKey('Tags', blank=True, null=True, on_delete=models.SET_NULL, related_name='tag')
    users = models.ForeignKey('User', blank=False, null=True, on_delete=models.CASCADE, related_name='user')
    type = models.BooleanField(default=False, verbose_name='Тип транзакции')
    summ = models.PositiveIntegerField(null=False, verbose_name='Сумма')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя тега')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'