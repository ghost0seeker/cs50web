from django import forms

class NewItemForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    image = forms.URLField()
    initial_bid_price = forms.DecimalField(max_digits=10, decimal_places=2)
    category = forms.CharField()

class NewBidForm(forms.Form):
    bid_amount = forms.DecimalField(max_digits=10, decimal_places=2)