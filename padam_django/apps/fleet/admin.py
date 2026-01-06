from django.contrib import admin

from . import models


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    pass


class BusStopInline(admin.TabularInline):
    model = models.BusStop

    # One empty default form
    extra = 1
    fields = ['order', 'place', 'stop_time']


@admin.register(models.BusShift)
class BusShiftAdmin(admin.ModelAdmin):

    # Admin view
    list_display = ['id', 'bus', 'driver', 'start_time', 'end_time']
    list_filter = ['bus', 'driver']

    inlines = [BusStopInline]
