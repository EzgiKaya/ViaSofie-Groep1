## Imports
# Nodig om urls te laten werken
from django.conf import settings
from django.conf.urls import include, url , handler404 , handler500 , patterns
from django.conf.urls.static import static
# Django-Admin gerelateerde urls
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_reset
# Importeren van alle views
from . import views
# Vertalingsconventie
from django.conf.urls.i18n import i18n_patterns

## Url patterns
urlpatterns = [
    #admin url
    url(r'^admin/', admin.site.urls),
    #vertalingsconventie
    url(r'^i18n/', include('django.conf.urls.i18n')),
    #homepagina
    url(r'^$', views.home, name='home'),
    #contactpagina
    url(r'^contact/', views.contact, name='contact'),
    #pandenpagina die te koop zijn
    url(r'^kopen/', views.kopen, name='kopen'),
    #pandenpagina die te huur zijn
    url(r'^huren/', views.huren, name='huren'),
    #disclaimer footer
    url(r'^disclaimer/', views.disclaimer, name='disclaimer'),
    #privacybeleid footer
    url(r'^privacybeleid/', views.privacybeleid, name='privacybeleid'),
    #loginpagina
    url(r'^login/', views.LoginUser, name='login'),
    #more pagina incl. partners, referenties, ebook, nieuwsbrief,advies
    url(r'^more/', views.more, name='more'),
    #loginpagina mobile
    url(r'^loginpage/', views.loginpage, name='loginpage'),
    #logout
    url(r'^logout/', views.logout_user, name='logout'),
    #pand detail
    url(r'^pand/(?P<pand_id>[0-9]+)',views.pand, name='pand'),
    #zoekfilter
    url(r'^search/$', views.search, name='search_estate'),
    #paswoord is verstuurd
    url(r'^resetpassword/passwordsent/$', auth_views.password_reset_done, {'template_name': 'websiteSofie/password_reset_done.html'}, name='password_reset_done'),
    #reset paswoord pagina
    url(r'^resetpassword/$', auth_views.password_reset, {'template_name': 'websiteSofie/password_reset_form.html'}, name='password_reset'),
    #unieke url voor paswoord te reseten
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm,{'template_name': 'websiteSofie/password_reset_confirm.html'}, name='password_reset_confirm'),
    #paswoord reset voltooid
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'websiteSofie/password_reset_complete.html'}, name='password_reset_complete'),
    #verkoperspagina
    url(r'^userPage/', views.userPage, name='userPage'),
    #detail zoekfilter
    url(r'^detail_search/$',views.detail_search, name='detail_search_estate'),
    #nieuwsbrief inschrijven
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    #nieuwsbrief uitschrijven
    url(r'^unsubscribe/', views.unsubscribe, name='unsubscribe'),
    #accountgegevens updaten
    url(r'^update_account/', views.update_account, name='update account'),
    #media url
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,}),
]

# Error handlers
handler404 = views.error_404
handler500 = views.error_500
