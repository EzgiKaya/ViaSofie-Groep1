## Imports
# django redirect imports
from django.shortcuts import render, redirect , get_object_or_404
import re
# import om views te schrijven
from django.views.generic import View
# Create your views here.
import csv
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
# importeren mail functie
from django.core.mail import send_mail,EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string , get_template
from django.template import Context
# user authenticatie
from django.contrib import auth
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# bescherming tegen csrf aanval - security
from django.template.context_processors import csrf
# importeren van modellen en forms
from django import forms
from websiteSofie.models import *
from websiteSofie.forms import *
# vertalingsconventie voor python files
from django.utils.translation import ugettext_lazy as _
# showing messages
from django.contrib import messages
# querylinks searchfilter
from django.db.models import Q
# paginering van panden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


## views
# Homepagina
def home(request):

    # immo in de kijker worden gefilterd op een bool=True
    immoindekijker_list = Estate.objects.filter(indekijker="1")[:6]
    # deze worden op de home.html template geladen
    template = loader.get_template('websiteSofie/home.html')
    context = { 'immoindekijker_list': immoindekijker_list,}
    return HttpResponse(template.render(context,request))


# Contactpagina
def contact(request):
    #post methode voor contactformulier
    if request.method == 'POST':
        #form wordt gelinkt aan specifieke form
        form = ContactForm(request.POST)
        #controle of form correct is
        if form.is_valid():
        #haalt data uit form
        #mail naar Sofie
            email_Sofie = settings.EMAIL_HOST_USER
            name=form.cleaned_data['name']
            email=form.cleaned_data['email']
            subject=form.cleaned_data['subject']
            text=form.cleaned_data['text']

            host_email = [email_Sofie]
            client_email = [email]
            client_subject = 'Contact Via Sofie'

            #ctx = context, data dat wordt gebruikt in de mail
            ctx = {
                'name' : name,
                'text' : text,
                'email' : email
            }
            #mail template
            message = get_template("mails/contactMailClient.html").render(Context(ctx))
            #alles wordt samengevoegd, from_email wordt nu uit settings gehaald.
            msg = EmailMessage(client_subject, message, to=client_email)
            msg.content_subtype = 'html'
            msg.send()

            # mail naar Sofie
            message = get_template("mails/contactMailSofie.html").render(Context(ctx))
            msg = EmailMessage(subject, message, to=host_email)
            msg.content_subtype = 'html'
            msg.send()
            #subject, from_email, to = 'Contactformulier viasofie.be: '+subject, email, 'viasofiegroep1@gmail.com'
            #html_content ='<p>U hebt volgende mail ontvangen via het contacformulier op uw website.</p><br>'+'<p>Van: '+name+'</p><br>'+'<p>email: '+email+'</p>'+'<br><br>Vraag: '+text
            #msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            #msg.attach_alternative(html_content, "text/html")
            #msg.send()
            return render(request,'websiteSofie/contact_succes.html')
    else:
        form = ContactForm()
    return render(request, 'websiteSofie/contact.html', {'form': form})
            #<html lang="en">

# Morepagina
def more(request):
    #ebook form
    if request.method == 'POST':
        #form wordt gelinkt aan specifieke form
        form_ebook = Ebook(request.POST)
        #controle of form correct is
        if form_ebook.is_valid():
            # Stuur een mail naar registratie ebook
            email_Sofie = settings.EMAIL_HOST_USER
            name=form_ebook.cleaned_data['name']
            email=form_ebook.cleaned_data['email']

            host_email = [email_Sofie]
            client_email = [email]
            client_subject = 'Ebook Via Sofie'

            #ctx = context, data dat wordt gebruikt in de mail
            ctx = {
                'name' : name,
                'email' : email
            }

            message = get_template("mails/contactMailClient.html").render(Context(ctx))
            msg = EmailMessage(client_subject, message, to=client_email)
            msg.content_subtype = 'html'
            msg.send()

            message = get_template("mails/contactMailSofie.html").render(Context(ctx))
            msg = EmailMessage(client_subject, message, to=host_email)
            msg.content_subtype = 'html'
            msg.send()
            #succes boodschap ebook
            form_ebook.save()
            return render(request,'websitesofie/ebook_succes.html')

        else:
            form_ebook = Ebook()
#hier worden alle partners gedisplayed op de more pagina onder de tab partners
    partner_list=Partner.objects.all()
#hier worden de advies vragen gedisplayed op de more pagina onder de tab advies
    faq_list = FAQ.objects.all()
    #hier worden de panden die als referentie werden aangeduidt gefilterd
    referentie_list=Estate.objects.filter(beschikbaarheid="IS_REFERENTIE")
#hier worden de reviews gedisplayed op de more pagina onder de tab referenties
#de reviews worden gefilterd op waarde true
#Bij het ingeven van een review staat deze default op false, de beheerde moet deze op True zetten
    review_list = Review.objects.filter(approved=True)
    referentie_list=Estate.objects.filter(beschikbaarheid="IS_REFERENTIE")
    paginator = Paginator(referentie_list, 10)

    page = request.GET.get('page')
    try:
        referentiepand = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        referentiepand = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        referentiepand = paginator.page(paginator.num_pages)


    form_ebook=Ebook()
    #registreren voor de nieuwsbrief
    form_subscriber=SubscriptionForm()
    template=loader.get_template('websiteSofie/more.html')
    context={
                'partner_list' : partner_list,
                'faq_list' : faq_list,
                'review_list' : review_list,
                'referentie_list': referentiepand,
                'form_ebook':form_ebook,
                'form_subscriber':form_subscriber,
                'referentie_list':referentiepand,
            }
    return HttpResponse(template.render(context,request))

#nieuwsbrief
def subscribe(request):
    if request.method == "POST":
        #form wordt gelinkt aan specifieke form
        form_subscriber = SubscriptionForm(request.POST)

        #controle of form correct is
        if form_subscriber.is_valid():
            #haalt data uit de form
            email_Sofie = settings.EMAIL_HOST_USER
            name=form_subscriber.cleaned_data['name']
            email=form_subscriber.cleaned_data['email']

            host_email = [email_Sofie]
            client_email = [email]
            client_subject = 'Nieuwsbrief Via Sofie'

            #ctx = context, data dat wordt gebruikt in de mail
            ctx = {
                'name' : name,
                'email' : email
            }

            message = get_template("mails/subscribeMailSofie.html").render(Context(ctx))
            msg = EmailMessage(client_subject, message, to=host_email)
            msg.content_subtype = 'html'
            msg.send()

            message = get_template("mails/subscribeMailClient.html").render(Context(ctx))
            msg = EmailMessage(client_subject, message, to=client_email)
            msg.content_subtype = 'html'
            msg.send()

            form_subscriber.save()
            #succes html wordt getoond
            return render(request,'websitesofie/subscribe_succes.html')

        else:
            return redirect('websiteSofie.views.more')

    else:
        return redirect('websiteSofie.views.more')

#uitschrijven nieuwsbrief
def unsubscribe(request):
    if 'email' in request.GET:
        email_u=request.GET.get('email',None)
        #Checken of email adres in de database zit
        if Subscription.objects.filter(email=email_u).exists():
            #als email in db zit dan wordt hij verwijdert in database
            Subscription.objects.filter(email=email_u).delete()
            return render(request,'websiteSofie/unsubscribe_succes.html')
        else:
            return render(request,'websiteSofie/unsubscribe.html')
    else:
        return render(request,'websiteSofie/unsubscribe.html')


#huren pagina
def huren(request):
    #globale zoekfilter
    searchform = SearchForm()
    #huizen die te huur zijn worden gedisplayed op basis van bool rent=True
    huren_list = Estate.objects.filter(rent="1").filter(beschikbaarheid__exact='AVAILABLE')
    paginator = Paginator(huren_list, 10)

    page = request.GET.get('page')
    try:
        huren = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        huren = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        huren = paginator.page(paginator.num_pages)

    template = loader.get_template('websiteSofie/huren.html')
    string = None
    if 'empty_query' in request.session:
        string = True
        del request.session['empty_query']

    context = { 'huren_list': huren,'searchform' : searchform , 'string' : string}
    return HttpResponse(template.render(context,request))

#kopen pagina
def kopen(request):
    #globale zoekfilter
    searchform = SearchForm()
    #huizen die te koop zijn worden gedisplayed op basis van bool sale=True
    kopen_list = Estate.objects.filter(sale="1").filter(beschikbaarheid__exact='AVAILABLE')
    paginator = Paginator(kopen_list, 10)

    page = request.GET.get('page')
    try:
        kopen = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        kopen = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        kopen = paginator.page(paginator.num_pages)

    template = loader.get_template('websiteSofie/kopen.html')
    string = None
    if 'empty_query' in request.session:
        string = True
        del request.session['empty_query']

    context = { 'kopen_list': kopen,'searchform' : searchform , 'string' : string}
    return HttpResponse(template.render(context,request))

#login view
def LoginUser(request):
    #redirect naar loginpage bij GET request
    if request.GET:
        return redirect('websiteSofie.views.loginpage')
    if request.user.is_authenticated():
        #als user ingelogd is wordt hij naar de homepagina verwezen
        return redirect('websiteSofie.views.home')

    if request.POST:
        #gegevens in die worden ingegeven worden gechekt met de database
        l_email = request.POST.get('email')
        l_password=request.POST.get('password')
        if User.objects.filter(email=l_email).exists():
            l_username = User.objects.get(email = l_email).username
            user = auth.authenticate(username = l_username, password = l_password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['current_user_id'] = user.id
                    request.session['current_user_name'] = user.last_name
                    return redirect('websiteSofie.views.home')
                else:
                    return render(request,'websiteSofie/errorUserDeactivated.html')
            else:
                return render(request,'websiteSofie/errorUserAuth.html')
        else:
            return render(request,'websiteSofie/errorUserAuth.html')
    else:
        return redirect('websiteSofie.views.home')

#inlogpagina voor mobile
def loginpage(request):
    return render(request, 'websiteSofie/loginpage.html')

#view om user uit te loggen
def logout_user(request):
    logout(request)
    return redirect('websiteSofie.views.home')

#disclaimer
def disclaimer(request):
    #alle objecten uit disclaimer worden opgehaald uit de database
    disclaimer_list = Disclaimer.objects.all()
    template = loader.get_template('websiteSofie/disclaimer.html')
    #de lijst wordt in de context gestoken
    context={'disclaimer_list' : disclaimer_list,}
    return HttpResponse(template.render(context,request))

#privacybeleid
def privacybeleid(request):
    #alle objecten uit het privacybeleid worden opgehaald uit de database
    privacybeleid_list = Privacybeleid.objects.all()
    template = loader.get_template('websiteSofie/privacybeleid.html')
    #de lijst wordt in de context gestoken
    context={'privacybeleid_list' : privacybeleid_list,}
    return HttpResponse(template.render(context,request))

#pand view
def pand(request,pand_id):
    pand = get_object_or_404(Estate, pk=pand_id)
    if request.user.is_authenticated():
        is_seller = False
        # check of de gebruiker admin, staff of verkoper is van het pand
        if request.user.is_superuser or request.user.is_staff:
            pass
        elif Estate_Sellers.objects.filter(estate_ID = pand_id):
            for sellers in Estate_Sellers.objects.filter(estate_ID = pand_id):
                if request.user.id == sellers.user_ID.id:
                    is_seller = True
            if is_seller is False:
                pand.hits=pand.hits+1
                pand.save()
        else:
            pand.hits=pand.hits+1
            pand.save()
    else:
        pand.hits=pand.hits+1
        pand.save()


    template = loader.get_template('websiteSofie/pand.html')
    context =   {
                    'pand': pand,
                }

    return HttpResponse(template.render(context,request))

#zoekfilter
def search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)
        if searchform.is_valid():
            # inkomende zoekopdracht wordt opgesplitst in verschillende afzonderlijke zoektermen
            string = searchform.cleaned_data['search']
            terms = re.compile(r'[^\s",;.:]+').findall(string)
            # zoektermen worden vergeleken met de relevante velden van Model Estate
            fields = ['adres','area_code','town','description','provincie','referencenumber','estate_criteria__criteria_ID__name'] # your field names
            query = None
            # query wordt opgesteld voor elke overeenkomende zoekterm
            for term in terms:
                for field in fields:
                    qry = Q(**{'%s__icontains' % field: term})
                    if query is None:
                        query = qry
                    else:
                        query = query | qry

            query &= Q(beschikbaarheid__exact='AVAILABLE')
            # Panden worden gefilterd volgens de oorspronkelijke pagina van de zoekopdracht
            if request.POST.get('status') == 'kopen':
                query &= Q(sale__exact='1')
                found_entries = Estate.objects.filter(query).distinct().order_by('sale_price') # your model

                paginator = Paginator(found_entries, 10)

                page = request.GET.get('page')
                try:
                    result = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    result = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    result = paginator.page(paginator.num_pages)

            else:
                query &= Q(rent__exact='1')
                found_entries = Estate.objects.filter(query).distinct().order_by('rent_price') # your model


                paginator = Paginator(found_entries, 10)

                page = request.GET.get('page')
                try:
                    result = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    result = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    result = paginator.page(paginator.num_pages)


            status = request.POST.get('status')
            return render(request, 'websiteSofie/results.html', {'found_entries':result , 'string':string , 'searchform':searchform, 'status':status })
        else:
            if request.POST.get('status') == 'kopen':
                return redirect('websiteSofie.views.kopen')
            else:
                return redirect('websiteSofie.views.huren')
    else:
        searchform = SearchForm()
        return redirect('websiteSofie.views.home')

# Gedetailleerde zoekfilter
def detail_search(request):
    # Check of er minstens 1 veld ingevuld is
    if 'adres' or 'area_code' or 'town' or 'province' or 'range_values' or 'bedroomsmin' or 'bedroomsmax' or 'bathroomsmin' or 'bathroomsmax' or 'bebouwing' or 'type' in request.GET:
        # Ophalen velden
        adres = request.GET.get('adres', None)
        area_code = request.GET.get('area_code', None)
        town = request.GET.get('town', None)
        province = request.GET.get('province', None)
        bedroomsmin = request.GET.get('bedroomsmin', None)
        bedroomsmax = request.GET.get('bedroomsmax', None)
        bathroomsmin = request.GET.get('bathroomsmin', None)
        bathroomsmax = request.GET.get('bathroomsmax', None)
        bebouwing = request.GET.get('bebouwing', None)
        estate_type = request.GET.get('type', None)
        # Splitsen van prijzen van de prijs slider
        range_value = request.GET.get('range_value', None)
        price_values = range_value.split('-')
        pricegte = price_values[0]
        pricelte = price_values[1]

        # dubbele check of er relevante waarden zijn
        if not(adres, area_code, town, province, bedroomsmin, bedroomsmax, bathroomsmin, bathroomsmax, bebouwing, estate_type):
            if request.GET.get('status') == "kopen":
                return redirect('websiteSofie.views.kopen')
            elif request.GET.get('status') == "huren":
                return redirect('websiteSofie.views.huren')
            else:
                return redirect('websiteSofie.views.home')

        # opstellen query
        else:
            query = Q()
            empty = True
            if adres:
                query &= Q(adres__icontains=adres)
                empty = False

            if area_code:
                query &= Q(area_code__icontains=area_code)
                empty = False

            if town:
                query &= Q(town__icontains=town)
                empty = False

            if province:
                query &= Q(province__icontains=province)
                empty = False

            if bedroomsmin:
                query &= Q(bedrooms__gte=bedroomsmin)
                empty = False
            if bedroomsmax:
                query &= Q(bedrooms__lte=bedroomsmin)
                empty = False

            if bathroomsmin:
                query &= Q(bathrooms__lte=bathroomsmin)
                empty = False
            if bathroomsmax:
                query &= Q(bathrooms__lte=bathroomsmax)
                empty = False

            if bebouwing:
                query &= Q(bebouwing__exact=bebouwing)
                empty = False

            if estate_type:
                query &= Q(type_estate__exact=estate_type)
                empty = False

            if request.GET.get('status') == "kopen":
                query &= Q(sale='1')
                if pricelte:
                    query &= Q(sale_price__lte=pricelte)
                if pricegte:
                    query &= Q(sale_price__gte=pricegte)
            else:
                query &= Q(rent='1')
                if pricelte:
                    query &= Q(rent_price__lte=pricelte)
                if pricegte:
                    query &= Q(rent_price__gte=pricegte)

            if empty:
                found_entries = None
                request.session['empty_query'] = 'True'
                if request.GET.get('status') == "kopen":
                    return redirect('websiteSofie.views.kopen')
                else:
                    return redirect('websiteSofie.views.huren')
            else:
                query &= Q(beschikbaarheid__exact='AVAILABLE')
                found_entries = Estate.objects.filter(query).distinct()

                paginator = Paginator(found_entries, 10)

                page = request.GET.get('page')
                try:
                    result = paginator.page(page)
                except PageNotAnInteger:
                    # If page is not an integer, deliver first page.
                    result = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999), deliver last page of results.
                    result = paginator.page(paginator.num_pages)

                print(query)
                searchform = SearchForm()
                status = request.GET.get('status')
                return render(request, 'websiteSofie/results.html', {'found_entries':result , 'searchform':searchform, 'status':status})

    elif request.GET.get('status'):
        if request.GET.get('status') == "kopen":
            return redirect('websiteSofie.views.kopen')
        else:
            return redirect('websiteSofie.views.huren')
    else:
        return redirect('websiteSofie.views.home')

#checken of persoon is ingelogd
@login_required
def userPage(request):
    #verkoper zijn huizen worden opgelijst
    estate_list = Estate.objects.filter( estate_sellers__user_ID__exact = request.user.id ).order_by('date_placed')
    template=loader.get_template('websiteSofie/userPage.html')
    context={'estate_list':estate_list,}
    user_form = UserUpdateForm(instance=request.user)
    userprofile = get_object_or_404(Account, user=request.user)
    account_form = AccountUpdateForm(instance=userprofile)
    updated = False
    if 'updated' in request.session:
        updated = True
        del request.session['updated']
    else:
    #user kan een review schrijven op zijn pagina
        if request.method == 'POST':

            new_review_form = ReviewForm(request.POST)
                # check whether it's valid:

            if new_review_form.is_valid():

                review_title=new_review_form.cleaned_data['review_title']
                review_text=new_review_form.cleaned_data['review_text']
                new_review = new_review_form.save(commit=False)
                new_review.user_ID=request.user
                new_review.save()
                #Email versturen naar Sofie
                myEmail='viasofiegroep1@gmail.com'
                subject, from_email, to = 'Review viasofie.be: '+review_title, myEmail, myEmail
                urlValidatie='http://localhost:8000/admin/websiteSofie/review/change'
                html_content =request.user.username+'<p> heeft volgende review geschreven.</p><br>'+review_text+'<br><p>Valideer deze review op: </p>'+urlValidatie
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                # succes boodschap contacformulier
                messages.success(request,'Uw review is doorgestuurd')
                form = new_review_form

                return render(request,'websiteSofie/userPage.html', {'form': form , 'estate_list':estate_list, 'account_form' : account_form, 'user_form' : user_form})


    form = ReviewForm()
    return render(request, 'websiteSofie/userPage.html', {'form': form , 'estate_list':estate_list, 'account_form' : account_form,'user_form' : user_form, 'updated':updated,})


def update_account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        account_form = AccountUpdateForm(request.POST)
        if account_form.is_valid() and user_form.is_valid():
            u_user = request.user
            u_user.first_name = user_form.cleaned_data['first_name']
            u_user.last_name = user_form.cleaned_data['last_name']
            u_user.save()

            u_account = get_object_or_404(Account, user=request.user)
            u_account.city = account_form.cleaned_data['city']
            u_account.street = account_form.cleaned_data['street']
            u_account.house_number = account_form.cleaned_data['house_number']
            u_account.area_code = account_form.cleaned_data['area_code']
            u_account.birth_date = account_form.cleaned_data['birth_date']
            u_account.mobile_number = account_form.cleaned_data['mobile_number']
            u_account.telephone_number = account_form.cleaned_data['telephone_number']
            u_account.save()

            request.session['updated'] = 'True'
            return redirect('websiteSofie.views.userPage')
        else:
            return redirect('websiteSofie.views.userPage')

    else:
        return redirect('websiteSofie.views.userPage')

#view om paswoord te reseten
def password_reset(request):
    return render(request, 'websiteSofie/password_reset_form.html')
#view om nieuw paswoord te verzenden
def password_reset_sent(request):
    return render(request, 'websiteSofie/password_reset_sent.html')
#view om de paswoord reset te bevestigen
def password_reset_confirm(request):
    return render(request, 'websiteSofie/password_reset_confirm.html')
#view als reset klaar is
def password_reset_done(request):
    return render(request, 'websiteSofie/password_reset_done.html')
#error 404 view
def error_404(request):
    return render(request,'websitesofie/404.html')
#error 500 view
def error_500(request):
    return render(request,'websitesofie/500.html')
