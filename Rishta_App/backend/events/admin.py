from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE

from backend.events.models import Event


class EventAdminForm(forms.ModelForm):
    detail = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Event
        fields = '__all__'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    list_display = ('title', 'start_date', 'end_date', 'created_by', 'is_active')
    list_filter = ('start_date', 'end_date', 'is_active')
    search_fields = ('title',)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
