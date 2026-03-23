from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", blank=True, related_name="watchlisted_by")


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction')
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=600)
    init_bet = models.PositiveIntegerField()
    img_url = models.URLField(blank=True)
    current_bet = models.ForeignKey('Bet', on_delete=models.SET_NULL, null=True, blank=True, related_name='current_auction')

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bets')
    current_bet = models.IntegerField()
    def __str__(self):
        return f"{self.current_bet} from {self.user.username}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=600)
