from django.contrib import admin
from .models import Auction, Comment, Bet


admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(Bet)