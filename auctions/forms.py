from django import forms
from .models import *

class ListingForm(forms.Form):
	title = forms.CharField()
	description = forms.CharField()
	starting_bid = forms.DecimalField(decimal_places=2, max_digits=10)
	category = forms.ChoiceField(choices=Listing.Categories.choices)
	photo = forms.URLField(required=False)

class BidForm(forms.ModelForm):
	class Meta:
		model = Bid
		fields = ['value']

class CommentForm(forms.Form):
	content=forms.CharField()

class CategoriesForm(forms.Form):
	category = forms.ChoiceField(choices=Listing.Categories.choices)