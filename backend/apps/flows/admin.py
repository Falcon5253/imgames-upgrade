from django.contrib import admin
from .models import Flow, Card, Channel, Stage, ParameterChange


@admin.register(Flow)
class FlowAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organization')
    list_display_links = ('id', 'title')


class ParameterChangeInline(admin.TabularInline):
    model = ParameterChange
    extra = 0


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'short_description', 'flow')
    list_display_links = ('id', 'header')
    list_filter = ('flow',)
    search_fields = ('header', 'flow__title',)
    inlines = [ParameterChangeInline, ]


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'default_value', 'flow')
    list_display_links = ('id', 'name')


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'conversion', 'flow')
    list_display_links = ('id', 'name')


@admin.register(ParameterChange)
class ParameterChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'channel', 'type', 'math_operator',
                    'value', 'month_of_application', 'card')
    list_display_links = ('id', 'channel')
