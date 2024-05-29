from django.contrib import admin
from .models import Activity, ActivityInstance


class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "type",
        "public",
    ]


class ActivityInstanceAdmin(admin.ModelAdmin):
    list_display = [
        "activity",
        "start_time",
        "end_time",
        "duration",
    ]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityInstance, ActivityInstanceAdmin)
