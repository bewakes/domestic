from django.contrib import admin
from expenses.models import *

admin.autodiscover()

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Expense)
