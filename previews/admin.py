from django.contrib import admin
from previews.models import Monthly, Weekly


@admin.register(Monthly)
class MonthlyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'price', 'discount', 'discount_superior', 'release_date')


@admin.register(Weekly)
class WeeklyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'price', 'discount', 'release_date')
