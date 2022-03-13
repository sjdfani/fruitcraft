from django.contrib import admin
from .models import Account, AccountLevel, Icons, AccountIcon, AccountInfo, Cards, AccountCards


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_rank', 'clan_name',
                    'clan_position', 'last_login', 'state')
    list_filter = ('state',)


@admin.register(AccountLevel)
class AccountLevelAdmin(admin.ModelAdmin):
    list_display = ('account', 'stage', 'minimum', 'maximum')


@admin.register(AccountCards)
class AccountCardsAdmin(admin.ModelAdmin):
    list_display = ('account', 'card', 'stage', 'power',
                    'created_at', 'updated_at', 'state')
    list_filter = ('account', 'state')


@admin.register(AccountIcon)
class AccountIconAdmin(admin.ModelAdmin):
    list_display = ('account', 'icon_type', 'created_at', 'status')
    list_filter = ('account', 'status')


@admin.register(AccountInfo)
class AccountInfoAdmin(admin.ModelAdmin):
    list_display = ('account', 'gender', 'created_at', 'updated_at')


@admin.register(Icons)
class IconsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_type', 'stage',
                    'created_at', 'updated_at', 'status')
    list_filter = ('card_type',)
