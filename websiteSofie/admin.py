## Imports

from django.contrib import admin
from django.contrib.auth import admin as upstream , get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm , PasswordResetForm
from django.contrib.auth.models import Group, User

from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.crypto import get_random_string

from django import forms
from django.conf import settings
from django.core.mail import send_mail

from websiteSofie.models import *

User = get_user_model()

# Account-form inline voor User creation in admin
class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'accounts'

# Aangepaste User creation form met auto-gegenereerde wachtwoorden en verplicht email-veld
class UserCreationForm(UserCreationForm):
    auto_pass = get_random_string()
    password1 = forms.CharField(initial=auto_pass)
    password2 = forms.CharField(initial=auto_pass)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)


        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['email'].required = True
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    actions = ['download_emailadressen']
    inlines = (AccountInline, )
    add_fieldsets = (
        (None, {
            'description': (
                "Voer hier de gebruikersnaam en de emailadres van de nieuwe gebruiker in en klik op opslaan."
                " De gebruiker zal een email ontvangen met een link waarmee hij/zij zich kan inloggen"
                " op de site en wachtwoord veranderen."
            ),
            'fields': ('email', 'username',),
        }),
        ('Wachtwoord', {
            'description': "Deze wachtwoord wordt veranderd nadat de gebruiker opgeslaan wordt.",
            'fields': ('password1', 'password2'),
            'classes': ('collapse', 'collapse-closed'),
        }),
    )

    def download_emailadressen(self, request, queryset):
        import csv
        from django.http import HttpResponse
        import StringIO

        f = StringIO.StringIO()
        writer = csv.writer(f)
        writer.writerow([person.email for person in User.objects.all()])

        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=EmailAdressen.csv'
        return response

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# inlines voor Estate creation en change form
class Estate_CriteriaInline(admin.StackedInline):
    model = Estate_Criteria
    can_delete = True
    verbose_name = 'Vastgoed criteria'

class Estate_SellersInline(admin.StackedInline):

    model = Estate_Sellers
    can_delete = True
    verbose_name_plural = 'verkopers'

class EstateImageInline(admin.StackedInline):

    model = EstateImage
    can_delete = True
    verbose_name = 'Vastgoed afbeeling'
    list_display =("image_tag",)

# aangepaste estate admin form
class EstateAdmin(admin.ModelAdmin):
    exclude = ('date_placed', 'hits',)
    search_fields = ('adres','referencenumber','town')
    list_display = ('adres','house_number','date_placed','hits', 'sale','rent','qr_code','image_tag', )

    ordering = ('date_placed',)
    inlines = (Estate_CriteriaInline,Estate_SellersInline, EstateImageInline)

admin.site.register(Estate, EstateAdmin)

# Registreren van models voor admin beheerderspagina
admin.site.register(FAQ)
admin.site.register(Disclaimer)
admin.site.register(Privacybeleid)
admin.site.register(Estate_Criteria)
admin.site.register(Criteria)
admin.site.register(Estate_Status)
admin.site.register(Status)
admin.site.register(Estate_Sellers)
admin.site.register(Review)
admin.site.register(Partner)
admin.site.register(Subscription)
