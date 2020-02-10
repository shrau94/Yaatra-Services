from django.contrib import admin
from .models import DailyCommute


class CustomDailyCommute(admin.ModelAdmin):
    list_display = (
        'user', 'journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long',
        'start_time', 'created_on')
    search_fields = ('journey_title',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(DailyCommute, CustomDailyCommute)
