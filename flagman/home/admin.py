from django.contrib import admin

# Register your models here.

from .models import *

class TransactionsInlines(admin.TabularInline):
    fk_name = 'users'
    model = Transactions
    verbose_name = 'Транзакции пользователя'
    verbose_name_plural = 'Транзакции пользователя'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [TransactionsInlines, ]

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass