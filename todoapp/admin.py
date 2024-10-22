from django.contrib import admin
from .models import Task

# Register your models here.
# admin.site.register(Task)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'status', 'is_deleted', 'created_at')
    list_filter = ('is_deleted', 'status')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Include all tasks regardless of is_deleted
        return queryset.order_by('-created_at')

admin.site.register(Task, TaskAdmin)


# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('task', 'user', 'status', 'is_deleted', 'created_at')
#     list_filter = ('is_deleted', 'status')

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         # Order tasks by created_at in descending order
#         return queryset.order_by('-created_at')

# admin.site.register(Task, TaskAdmin)