## Imports
from django.db.models.signals import post_save
from models import Account
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader , Context
from django.template.loader import get_template
#importeren mail functie
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives

# Post-save methode voor het aanmaken van nieuwe gebruikers :
# Dit zorgt ervoor dat de nieuwe gebruiker een willekeurige wachtwoord krijgt
# en alsook een mail krijgt verstuurd naar zijn emailadres met logingegevens en inlogpagina url.
def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    # Wordt enkel uitgevoerd bij creatie en niet bij update
    if created:
        # random password generator
        user_password = get_random_string()
        user.set_password(user_password)
        user.save()
        print(user_password)

        # Email gegevens
        page_url = 'http://localhost:8000/'
        email_Sofie = settings.EMAIL_HOST_USER
        host_email = [email_Sofie]
        client_email = [user.email]
        client_subject = 'Welkom bij Via Sofie'

        #ctx = context, data dat wordt gebruikt in de mail
        ctx = {
            'page_url' : page_url,
            'password' : user_password,
            'username' : user.username
        }
        #mail template
        message = get_template("mails/accountMailClient.html").render(Context(ctx))
        #alles wordt samengevoegd, from_email wordt nu uit settings gehaald.
        msg = EmailMessage(client_subject, message, to=client_email)
        msg.content_subtype = 'html'
        msg.send()

post_save.connect(user_created, sender=User)
