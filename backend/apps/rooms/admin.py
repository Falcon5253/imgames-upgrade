from django.contrib import admin
from apps.rooms.models import Winner, Turn, Month, Round, Room, RoomParticipant


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'place',  'round', 'result')
    list_display_links = ('place', 'user')


@admin.register(Turn)
class TurnAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'month')


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'round')
    readonly_fields = ('key',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'room', 'current_month',
                    'is_active', 'created_at')
    readonly_fields = ('key', 'created_at', 'updated_at')
    search_fields = ('room__organization__prefix',)


class RoundAdminInline(admin.TabularInline):
    model = Round
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'organization', 'room_owner',
                    'number_of_turns', 'current_round', 'current_month')
    list_filter = ('organization',)
    readonly_fields = ('key',)
    inlines = [RoundAdminInline, ]

    def current_month(self, obj):
        current_round = obj.current_round
        if (current_round is not None) and (
            current_round.current_month is not None
        ):
            return current_round.current_month
        return "-"
    current_month.short_description = "Текущий месяц"


@admin.register(RoomParticipant)
class RoomParticipantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room')
    list_display_links = ('id', 'user')
