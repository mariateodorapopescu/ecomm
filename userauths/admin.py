from django.contrib import admin
from userauths.models import User
# from import_export.admin import ImportExportActionModelAdmin

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'bio'] # some variables names are predifined so beaware of the letters and dyslexic

# Register your models here.
admin.site.register(User, UserAdmin)