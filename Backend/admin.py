from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .models import User


admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Executor)
admin.site.register(Categories)
admin.site.register(Trade)
admin.site.register(Total_Trade)
admin.site.register(E_Trade)
admin.site.register(E_Category)
admin.site.register(Donate)
# Register your models here.
