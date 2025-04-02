from django import forms
from .models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="Full name",
                                         widget=forms.TextInput(
                                             attrs={'class': 'form-control', 'placeholder': 'Full name'}),
                                         required=False)
    shipping_email = forms.CharField(label="Email",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                                     required=False)
    shipping_address1 = forms.CharField(label="Address1",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Address1'}),
                                        required=False)
    shipping_address2 = forms.CharField(label="Address2",
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control', 'placeholder': 'Address2'}),
                                        required=False)
    shipping_country = forms.CharField(label="Country",
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Country'}),
                                       required=False)
    shipping_city = forms.CharField(label="City",
                                    widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                                    required=False)
    shipping_state = forms.CharField(label="State",
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                                     required=False)
    shipping_zipcode = forms.CharField(label="Zipcode",
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                                       required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_country',
                  'shipping_city', 'shipping_state', 'shipping_zipcode']

        exclude = ['user']


class PaymentForm(forms.ModelForm):
    card_name = forms.CharField(label="Card Name",
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Card Name'}),
                                required=False)
    card_number = forms.CharField(label="Card Number",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
                                  required=False)
    card_expiry = forms.CharField(label="Card Exp",
                                  widget=forms.TextInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Card Exp'}),
                                  required=False)
    card_cvv = forms.CharField(label="CVV",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'CVV'}),
                               required=False)

    class Meta:
        model = ShippingAddress
        fields = ['card_name', 'card_number', 'card_expiry', 'card_cvv']
        exclude = ['user']