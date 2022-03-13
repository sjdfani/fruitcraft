from django.db import models
from users.models import CustomUser
from django.utils import timezone


class Icons(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='icons/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class AccountMood(models.TextChoices):
    HAPPY = ('happy', 'Happy')
    ANGRY = ('angry', 'Angry')
    ASHAMED = ('ashamed', 'Ashamed')
    BORED = ('bored', 'Bored')
    CALM = ('calm', 'Calm')
    COLD = ('cold', 'Cold')
    PROUD = ('proud', 'Proud')
    CONFUSED = ('confused', 'Confused')
    CRAZY = ('crazy', 'Crazy')
    DEPRESSED = ('depressed', 'Depressed')
    GOOD = ('good', 'Good')
    HOPEFUL = ('hopeful', 'Hopeful')
    HUNGRY = ('hungry', 'Hungry')
    ALONE = ('alone', 'Alone')


class ClanPosition(models.TextChoices):
    NONE = ('none', 'None')
    LEADER = ('leader', 'Leader')
    COLEADER = ('co-leader', 'Co-leader')
    MEMBER = ('member', 'Member')


class AccountState(models.TextChoices):
    INGAME = ('in-game', 'In-Game')
    PENDING = ('pending', 'Pending')
    DELETED = ('deleted', 'Deleted')


class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    icon = models.ForeignKey(Icons, on_delete=models.CASCADE)
    mood = models.CharField(
        max_length=10, choices=AccountMood.choices, default=AccountMood.HAPPY)
    coin = models.PositiveBigIntegerField(default=0)
    total_rank = models.PositiveBigIntegerField(default=0)
    experience = models.PositiveBigIntegerField(default=0)
    clan_name = models.CharField(max_length=50, default='None')
    clan_position = models.CharField(
        max_length=10, choices=ClanPosition.choices, default=ClanPosition.NONE)
    invite_code = models.CharField(max_length=10)
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=10, choices=AccountState.choices, default=AccountState.INGAME)

    def __str__(self) -> str:
        return self.user.email


class IconType(models.TextChoices):
    COMMON = ('common', 'Common')
    VIP = ('vip', 'Vip')


class AccountIcon(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    icon = models.OneToOneField(Icons, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=10, choices=IconType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.account.user.email


class GenderAccountInfo(models.TextChoices):
    NONE = ('none', 'None')
    MALE = ('male', 'Male')
    FEMALE = ('female', 'Female')


class AccountInfo(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    real_name = models.CharField(max_length=50, blank=True, null=True)
    birth_year = models.CharField(max_length=5, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GenderAccountInfo.choices, default=GenderAccountInfo.NONE)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.account.user.email


class AccountLevel(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    stage = models.PositiveIntegerField(default=1)
    minimum = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField(default=50)

    def __str__(self) -> str:
        return self.account.user.email


class CardType(models.TextChoices):
    COMMON = ('common', 'Common')
    MONSTER = ('monster', 'Monster')
    LEGENDARY = ('legendary', 'Legendary')
    CHAMPION = ('champion', 'Champion')


class Cards(models.Model):
    name = models.CharField(max_length=50)
    card_type = models.CharField(max_length=10, choices=CardType.choices)
    stage = models.PositiveIntegerField(default=1)
    max_power = models.PositiveBigIntegerField(default=0)
    revive_time = models.DurationField()
    image = models.ImageField(upload_to='cards/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class StateAccountCards(models.TextChoices):
    BASKET = ('basket', 'Basket')
    MINING = ('mining', 'Mining')
    ATTACKBUILDING = ('attack-building', 'Attack-Building')
    DEFENSEBUILDING = ('defense-building', 'Defense-Building')
    STORE = ('store', 'Store')


class AccountCards(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    card = models.OneToOneField(Cards, on_delete=models.CASCADE)
    stage = models.PositiveIntegerField(default=1)
    power = models.PositiveBigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=20, choices=StateAccountCards.choices)

    def __str__(self) -> str:
        return self.account.user.email
