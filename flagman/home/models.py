from django.db import models
import dadata

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

    def save(self, *args, **kwargs):
        client = dadata.Dadata(token, secret)
        result = client.clean(name="phone", source=str(self.phone))
        self.phone = result['phone']
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Transactions(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название транзакции')
    tags = models.ForeignKey('Tags', blank=True, null=True, on_delete=models.SET_NULL, related_name='tag')
    users = models.ForeignKey('User', blank=False, Null=True, on_delete=models.CASCADE, related_name='user')
    type = models.BooleanField(default=False, verbose_name='Тип транзакции')

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