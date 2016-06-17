##Imports

from django import forms
from django.forms import ModelForm
from websiteSofie.models import *
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from nocaptcha_recaptcha.fields import NoReCaptchaField
from django.core.validators import MaxValueValidator, MinValueValidator

# Form voor ingave zoekfilter -> kopen.html | huren.html | results.html
class SearchForm(forms.Form):
    search = forms.CharField(label='search',
                    widget=forms.TextInput(attrs={'placeholder': 'Gemeente, referentienummer, adres...'}), max_length=50)

# Login pop up form voor grote schermen -> _navbar.html
# Login form voor mobile/kleine schermen -> loginpage.html
class LoginForm(forms.ModelForm):
    email = forms.EmailField(label = _('E-mailadres'))
    password = forms.EmailField(label = _('Wachtwoord'),widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['email','password']

# Form om te registreren voor de Ebook -> more.html
class Ebook(forms.ModelForm):
    name = forms.CharField(label='Naam', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    captcha = NoReCaptchaField()
    class Meta:
        model=Ebook
        fields=['name','email']

# Form voor contactformulier -> contact.html
class ContactForm(forms.ModelForm):
    name=forms.CharField(label='Naam', max_length=100)
    email=forms.EmailField(label='E-mail', max_length=100)
    subject=forms.CharField(label='Onderwerp',max_length=100)
    text=forms.CharField(label='Tekst',widget=forms.Textarea)
    captcha = NoReCaptchaField(label="")
    class Meta:
        model=Contact
        fields=['name','email','subject','text']

# Form om een review te schrijven -> more.html
class ReviewForm(forms.ModelForm):
    review_title = forms.CharField(label='Review titel', max_length = 50)
    review_text = forms.CharField(label='Review tekst', widget=forms.Textarea)
    review_rating = forms.IntegerField(label='Review beoordeling',validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
        widget=forms.TextInput(attrs={'placeholder': 'beoordeling van 0 tot 5'}),)

    class Meta:
        model=Review
        fields=['review_title','review_text','review_rating']

# Form om te registreren voor de nieuwsbrief -> more.html
class SubscriptionForm(forms.ModelForm):
    name=forms.CharField(label='Naam', max_length=80)
    email=forms.EmailField(label='Email', max_length=50)
    class Meta:
        model=Subscription
        fields=['name','email']

# UpdateForm voor Userprofielen -> userPage.html
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Voornaam', max_length = 20)
    last_name = forms.CharField(label='Achternaam', max_length = 20)

    class Meta:
        model=User
        fields=['first_name','last_name']

# UpdateForm voor Accountgegevens -> userpage.html
class AccountUpdateForm(forms.ModelForm):
    city = forms.CharField(label='Stad', max_length=50)
    street = forms.CharField(label='Straat', max_length=50)
    house_number = forms.CharField(label='Huisnummer',max_length=10)
    area_code = forms.CharField(label='Postcode',max_length=50)
    birth_date = forms.DateField(label='Geboortedatum', widget=forms.TextInput(attrs={'placeholder': 'jjjj-mm-dd'}))
    mobile_number = forms.CharField(label='Gsm nummer', max_length=15)
    telephone_number = models.CharField(max_length=15)

    class Meta:
        model=Account
        fields=['city','street','house_number','area_code','birth_date','mobile_number','telephone_number']
