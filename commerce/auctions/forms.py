from django.forms import ModelForm
from .models import Bet, Comment

class BetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['current_bet']
        labels = {
            'current_bet': 'Your bet'
        }
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            "text": 'Comments text'
        }