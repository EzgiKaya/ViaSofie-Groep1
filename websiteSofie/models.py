# imports voor werkende models
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from uuid import uuid4
from websiteSofie.storage import OverwriteStorage
from django.db.models import signals
from django.conf import settings

#mail functie importeren
from django.core.mail import send_mail

# vertalingsconventie
from django.utils.translation import ugettext_lazy as _

# ophalen server tijd
def get_current_date():
    return timezone.now

#account model waarbij de gegevens van een verkoper worden opgeslagen
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', verbose_name="Gebruiker")
    city = models.CharField(max_length = 50, blank=True, verbose_name="Stad")
    street = models.CharField(max_length = 50, blank=True, verbose_name="Straat")
    house_number = models.CharField(max_length = 50, blank=True, verbose_name="Huisnummer")
    area_code = models.CharField(max_length = 50, blank=True, verbose_name="Postcode")
    birth_date = models.DateField(null = True, blank=True, verbose_name="Geboortedatum")
    mobile_number = models.CharField(max_length = 15, null = True, blank=True, verbose_name="GSM nummer")
    telephone_number = models.CharField(max_length = 15, null = True, blank=True, verbose_name="Telefoonnummer")

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)

    # maakt een Account model aan gelinkt met
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            profile, created = Account.objects.get_or_create(user=instance)

    post_save.connect(create_user_account, sender=User)

User.profile = property(lambda u: Account.objects.get_or_create(user=u)[0])

#Estate model voor het aanmaken van een nieuw pand
class Estate(models.Model):
    #verschillende mogelijkheden voor het pand
    ISAVALAIBLE_CHOICES = (
        ('AVAILABLE', 'Beschikbaar voor site'),
        ('N_AVAILABLE', 'Niet beschikbaar voor site'),
        ('IS_VERKOCHT', 'Is verkocht'),
        ('IS_REFERENTIE', 'Is verkocht en referentie'),
    )
    #provincies van belgie
    PROVINCE_CHOICES=(
        ('ANTWERPEN', 'Antwerpen'),
        ('OOST_VLAANDEREN', 'Oost-Vlaanderen'),
        ('WEST_VLAANDEREN', 'West-Vlaanderen'),
        ('LIMBURG', 'Limburg'),
        ('LUIK', 'Luik'),
        ('NAMEN', 'Namen'),
        ('VLAAMS_BRABANT', 'Vlaams-brabant'),
        ('WAALS_BRABANT', 'Waals-Brabant'),
        ('HENEGOUWEN', 'Henegouwen'),
        ('BRUSSEL', 'Brussel'),
        ('LUXEMBURG', 'Luxemburg'),
    )
    #typen bebouwing
    BEBOUWING_KEUZES=(
        (_('OPEN'), _('Open')),
        (_('HALFOPEN'),_('Halfopen')),
        (_('GESLOTEN'),_('Gesloten')),
    )
    #pand types
    ESTATE_TYPES=(
        (_('HUIS'),_('Huis')),
        (_('APPARTEMENT'),_('Appartement')),
        (_('GROND'),_('Grond')),
        (_('KAMER/KOT'),_('Kamer/Kot')),
        (_('ANDERE'),_('Andere')),
    )

    # pand gegevens
    adres = models.CharField(max_length = 20, verbose_name="Adres")
    house_number = models.IntegerField(default = '1', verbose_name="Huisnummer")
    bus_nummer = models.CharField(max_length = 20, blank=True)
    area_code = models.CharField(max_length = 8, verbose_name="Postcode")
    town = models.CharField(max_length = 50, verbose_name="Gemeente")
    provincie = models.CharField(max_length=30,choices=PROVINCE_CHOICES, default='ANTWERPEN', verbose_name="Provincie")
    country = models.CharField(max_length=50,default='Belgie', verbose_name="Land")

    hits = models.IntegerField(default='0', verbose_name="Hits")
    sale = models.BooleanField(verbose_name="Te koop")
    rent = models.BooleanField(verbose_name="Te huur")

    sale_price = models.DecimalField(max_digits = 19, decimal_places = 2, verbose_name="Verkoopprijs")
    rent_price = models.DecimalField(max_digits = 19, decimal_places = 2, verbose_name="Verhuurprijs")
    date_placed = models.DateField(default = get_current_date(), verbose_name="Datum geplaatst")
    beschikbaarheid = models.CharField(max_length=20,choices=ISAVALAIBLE_CHOICES, default='AVAILABLE', verbose_name="Beschikbaarheid")

    bedrooms = models.IntegerField(default='1', verbose_name="Slaapkamers")
    bathrooms = models.IntegerField(default='1', verbose_name="Badkamers")

    bebouwing = models.CharField(max_length=30,choices=BEBOUWING_KEUZES,blank=True, verbose_name="Bebouwing")
    type_estate = models.CharField(max_length=50,choices=ESTATE_TYPES,default='HUIS',blank=True, verbose_name="Type vastgoed")
    surface = models.CharField(max_length=50,default=" ", verbose_name="Oppervlakte")
    habitable_surface = models.CharField(max_length=50,default=" ", verbose_name="Bewoonbare oppervlakte")
    description = models.TextField(default="Geen beschrijving beschikbaar", verbose_name="Beschrijving")
    referencenumber = models.CharField(max_length=50,default=" ",unique=True, verbose_name="Referentienummer")

    indekijker = models.BooleanField(default=False, verbose_name="In de kijker")

    class Meta:
        verbose_name_plural = "Vastgoed"

    # returnt alle afbeeldingen van een pand
    def get_estateImages(self):
        estate_images=EstateImage.objects.filter(estate=self)
        return estate_images

    # returnt de Displayimage van een pand
    def get_estateDisplayImage(self):
        display_image=EstateImage.objects.filter(estate=self,is_display="1")
        return display_image

    # maakt een qr-code voor een pand aan en displayt deze op de admin estate-view pagina
    def qr_code(self):
        return '<img src="https://chart.googleapis.com/chart?chs=150x150&amp;cht=qr&amp;chl=http://www.viasofie.be/pand/%s">' % self.id
    qr_code.allow_tags = True

    # displayt de Hoofdafbeelding op de admin estate-view pagina
    def image_tag(self):
        photos = EstateImage.objects.filter(estate=self,is_display="1")
        for img in photos:
            return u'<img src="http://localhost:8000/media/%s"style="max-width:200px;" />' % img.image
    image_tag.short_description = "Foto"
    image_tag.allow_tags = True

    def __unicode__(self):
        return u'%s %s' % (self.adres, self.house_number)

#model voor het opslaan van afbeeldingen gelinkt aan een pand
class EstateImage(models.Model):
    estate = models.ForeignKey(Estate, related_name='images', verbose_name="Vastgoed")
    image = models.ImageField(upload_to = "images/", verbose_name = 'Afbeelding')
    is_display = models.BooleanField(default=False, verbose_name="Hoofdafbeelding")

#model om een status toe te voegen en aan te passen
class Status(models.Model):
    status_name = models.CharField(max_length = 50)
    date_placed = models.DateField(default=get_current_date())
    description=models.TextField(default="Geen beschrijving beschikbaar")

    class Meta:
        verbose_name_plural="Status"

    def __unicode__(self):
        return self.status_name

# stuurt een mail bij het wijzigen of aanmaken van een pand status
def update_status(sender,instance, **kw):
    pand = instance.estate_ID
    if pand.estate_sellers_set.all():
        for seller in pand.estate_sellers_set.all():
            if seller.user_ID.email:
                #mail sturen naar verkoper waar status van een pand is aangespast/toegevoegd
                user_email = seller.user_ID.email
                page_url = 'http://localhost:8000/userPage'
                subject = 'Jouw pand heeft een nieuwe status'
                mesagge = 'Een van jouw panden heeft een nieuwe status, bekijk deze op: %s' %(page_url)
                from_email = settings.EMAIL_HOST_USER
                send_mail(subject, mesagge, from_email, [user_email], fail_silently=False)
                print('mail sent to '+user_email)
            else:
                print('no email.')

#model om status toe te voegen/ aan te passen gelinkt met een pand
class Estate_Status(models.Model):
    estate_ID = models.ForeignKey(Estate, on_delete=models.CASCADE)
    status_ID = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_placed = models.DateField(default=get_current_date())

    def __unicode__(self):
        return u'%s %s: %s' % (self.estate_ID.adres, self.estate_ID.house_number, self.status_ID.status_name)
    class Meta:
        verbose_name_plural = "Vastgoed status"

# signal die mail verstuurt bij het updaten van een Estate Status
signals.post_save.connect(update_status, sender=Estate_Status)

#model om criterias toe te voegen die een pand kunnen hebben
class Criteria(models.Model):
    name = models.CharField(max_length = 50, verbose_name="Naam")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Criteria voor vastgoed"

#model om een criteria te linken met een pand
class Estate_Criteria(models.Model):
    estate_ID = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name="Vastgoed_ID")
    criteria_ID = models.ForeignKey(Criteria, on_delete=models.CASCADE, verbose_name="Criteria_ID")
    value = models.CharField(max_length = 100, verbose_name="Waarde")

    def __unicode__(self):
        return u'%s => %s' % (self.criteria_ID.name, self.value)

    class Meta:
        verbose_name_plural = "Vastgoed criteria"

#model om een review op te slaan in de database, hierdoor kan de admin bepalen welke review er op haar site worden getoond
class Review(models.Model):
    review_text = models.TextField(verbose_name="Review tekst")
    review_title = models.CharField(max_length = 50, verbose_name="Review titel")
    review_rating = models.IntegerField(default = 0, verbose_name="Review beoordeling")
    date = models.DateField(default=get_current_date(), verbose_name="Datum")
    approved = models.BooleanField(default=False, verbose_name="Goedgekeurd")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruikers_ID")

    def __unicode__(self):
        return u'%s %s' % (self.user_ID, self.review_title)

    class Meta:
        verbose_name_plural = "Geschreven reviews"

#model om volgers aan ene pand te linken
class Estate_Followers(models.Model):
    date_followed = models.DateField(verbose_name="Datum gevolgd")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruikers_ID")
    estate_ID = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name="Vastgoed_ID")

    def __unicode__(self):
        return unicode(self.date_followed)

#model om een verkoper aan een pand te linken
class Estate_Sellers(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruikers_ID")
    estate_ID = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name="Vastgoed_ID")

    class Meta:
        verbose_name = "Vastgoed verkoper"

#model om een persoon te linken aan een verkocht huis
class Estate_Bought(models.Model):
    date_bought = models.DateField(verbose_name="Datum gekocht")
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Gebruikers_ID")
    estate_ID = models.ForeignKey(Estate, on_delete=models.CASCADE, verbose_name="Vastgoed_ID")
    def __unicode__(self):
        return unicode(self.date_bought)

#model voor het aanpassen/toevoegen van veelgestelde vragen die worden geplaatst bij advies
class FAQ(models.Model):
    vraag = models.TextField(verbose_name="Vraag")
    antwoord = models.TextField(verbose_name="Antwoord")

    def __unicode__(self):
        return u'%s' % (self.vraag)
    class Meta:
        verbose_name_plural = "Advies"

#model voor het aanpassen/toevoegen van het dislaimer beleid
class Disclaimer(models.Model):
    text_disclaimer = models.TextField(verbose_name="Disclaimer tekst")

    def __unicode__(self):
        return u'%s' % (self.text_disclaimer)

    class Meta:
        verbose_name_plural = "Mijn disclaimer"

#model voor het aanpassen/toevoegen van het privacybeleid beleid
class Privacybeleid(models.Model):
    text_privacybeleid = models.TextField(verbose_name="Privacybeleid tekst")

    def __unicode__(self):
        return u'%s' % (self.text_privacybeleid)

    class Meta:
        verbose_name_plural = "Mijn privacybeleid"

#model voor het registreren voor het ebook. Deze worden opgeslagen in de DB
class Ebook(models.Model):
    email = models.EmailField(max_length = 50, verbose_name="Email")
    name=models.CharField(max_length=80, verbose_name="Naam")

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name_plural= "Geregistreerden voor Ebook"

#model voor het contactformulier te registreren in de database
class Contact(models.Model):
    name=models.CharField(max_length=80, verbose_name="Naam")
    email = models.EmailField(max_length = 50, verbose_name="Email")
    subject=models.CharField(max_length=100, verbose_name="Onderwerp")
    text=models.TextField(verbose_name="Tekst")

    def __unicode__(self):
        return u'%s' % (self.subject)

    class Meta:
        verbose_name= "Contactformulieren"

#model voor het toevoegen/aanpassen van een partner
class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Naam")
    image = models.ImageField(upload_to = "partner/", verbose_name = 'Afbeelding')
    is_visible = models.BooleanField(default = True, verbose_name="Zichtbaar")
    date_partnered = models.DateField(verbose_name="Datum gepartnerd")
    description = models.TextField(default="description", verbose_name="Beschrijving")
    level = models.IntegerField(verbose_name="Niveau")

    def __unicode__(self):
        return u'%s %s %s' % (self.image, self.name, self.description)

    class Meta:
        verbose_name_plural= "Mijn partners"

#model om iemand toe te voegen voor de nieuwsbrief
class Subscription(models.Model):
    name=models.CharField(max_length=80, verbose_name="Naam")
    email = models.EmailField(max_length = 50,unique=True, verbose_name="Email")
    is_Subscribed=models.BooleanField(default=True, verbose_name="Geabonneerd")

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        verbose_name_plural= "Geregistreerden voor nieuwsbrief"


#importeren om o.a mails te kunnnen sturen na aanmaken account
import signals
