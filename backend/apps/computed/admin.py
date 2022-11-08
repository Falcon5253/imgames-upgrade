from django.contrib import admin
from .models import ChannelComputed, StageComputed


@admin.register(ChannelComputed)
class ChannelComputedAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'cardinal_value', 'channel')
    list_display_links = ('id', 'turn')


@admin.register(StageComputed)
class StageComputedAdmin(admin.ModelAdmin):
    list_display = ('id', 'turn', 'conversion', 'stage')
    list_display_links = ('id', 'turn')
