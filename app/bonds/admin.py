from django.contrib import admin

from bonds import models


admin.site.register(models.Bond)
admin.site.register(models.Transaction)
