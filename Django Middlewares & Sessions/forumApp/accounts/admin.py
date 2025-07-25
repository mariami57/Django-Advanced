from django.contrib import admin
from django.contrib.auth import get_user_model


from posts.models import Post

UserModel = get_user_model()

# Register your models here.
@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    pass