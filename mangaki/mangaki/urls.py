from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django_js_reverse.views import urls_js

from mangaki import views
from mangaki.api.urls import urlpatterns as apipatterns
from mangaki.settings import DEBUG


urlpatterns = [
    # Examples:
    # url(r'^$', views.home, name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^jsreverse/$', urls_js, name='js_reverse'),
    url(r'^api/', include(apipatterns)),
    url(r'^$', views.index, name='home'),
    url(r'^data/(?P<category>\w+)\.json$', views.get_works, name='get-work'),
    url(r'^data/reco/(?P<algo>\w+)/(?P<category>\w+)\.json$', views.get_reco_algo_list, name='get-reco-algo-list'),
    url(r'^data/reco_dpp/(?P<category>\w+)\.json$', views.get_reco_list_dpp, name='get-dpp-list'),
    url(r'^getuser/(?P<work_id>\w+)\.json$', views.get_user_for_recommendations, name='get-user-for-reco'),
    url(r'^getuser\.json$', views.get_users, name='get-user'),
    url(r'^recommend/(?P<work_id>\w+)/(?P<target_id>\w+)$', views.recommend_work, name='reco-work'),
    url(r'^removeReco/(?P<work_id>\d+)/(?P<username>\w+)/(?P<targetname>\w+)$', views.remove_reco, name='remove-reco'),
    url(r'^removeReco/(?P<targetname>\w+)$', views.remove_all_reco, name='remove-all-reco'),
    url(r'^remove_anon_ratings/$', views.remove_all_anon_ratings, name='remove-all-anon-ratings'),
    # We explicitely want to override allauth's signup and login views
    url(r'^user/signup/$', views.signup, name="account_signup"),
    url(r'^user/login/$', views.login, name="account_login"),
    url(r'^user/', include('allauth.urls')),

    url(r'^profile/$', views.get_profile, name='my-profile'),
    url(r'^profile/(?P<category>\w+)/$', views.get_profile, name='my-profile'),
    url(r'^profile/(?P<category>\w+)/(?P<status>\w+)$', views.get_profile, name='my-profile'),
    url(r'^u/(?P<username>.+?)/(?P<category>\w+?)/$', views.get_profile, name='profile'),  # login_required?
    url(r'^u/(?P<username>.+?)/(?P<category>\w+?)/(?P<status>\w+)$', views.get_profile, name='profile'),  # login_required?
    url(r'^u/(?P<username>.+?)/?$', views.get_profile, name='profile'),  # login_required?

    url(r'^reco/$', views.get_reco, name='reco'),
    url(r'^reco_dpp/$', views.get_reco_dpp, name='reco_dpp'),
    url(r'^artists/$', views.ArtistList.as_view(), name='artist-list'),
    url(r'^artist/(?P<pk>\d+)$', views.ArtistDetail.as_view(), name='artist-detail'),
    url(r'^artist/(?P<artist_id>\d+)/add/(?P<work_id>\d+)$', views.add_pairing, name='add-pairing'),
    url(r'^vote_dpp/(?P<work_id>\d+)$', views.dpp_work, name='vote-dpp'),
    url(r'^vote/(?P<work_id>\d+)$', views.rate_work, name='vote'),
    url(r'^research/$', views.update_research, name='research'),
    url(r'^admin/', admin.site.urls),
    url(r'^about/(?P<lang>\w*)$', views.about, name='about'),
    url(r'^faq/$', views.faq_index, name='faq'),
    url(r'^legal/$', views.legal_mentions, name='legal'),
    url(r'^cgu/$', views.MarkdownView.as_view(), kwargs={'slug': 'cgu'}, name='cgu'),
    url(r'^events/$', views.events, name='events'),

    url(r'^fix/$', views.fix_index, name='fix-index'),
    url(r'^fix/suggestion/$', views.fix_index, name='fix-index'),
    url(r'^fix/suggestion/(?P<suggestion_id>\d+)$', views.fix_suggestion, name='fix-suggestion'),
    url(r'^evidence/$', views.update_evidence, name='update-evidence'),
    url(r'^grid/nsfw/$', views.nsfw_grid, name='nsfw-grid'),

    # url(r'^lookup/$', views.lookup_work'),
    url(r'^top/(?P<category_slug>[\w-]+)/$', views.top, name='top'),
    url(r'^event/(?P<pk>\d+)$', views.EventDetail.as_view(), name='event-detail'),
    url(r'^(?P<category>[\w-]+)/$', views.WorkList.as_view(), name='work-list'),
    url(r'^(?P<category>[\w-]+)/(?P<pk>\d+)$', views.WorkDetail.as_view(), name='work-detail'),
    url(r'^dpp/(?P<category>[\w-]+)/$', views.WorkList.as_view(), name='dpp-works', kwargs={'dpp': True})
]

handler404 = views.generic_error_view("Le contenu que tu cherches est introuvable.", 404)
handler403 = views.generic_error_view("L'accès au contenu que tu cherches est refusé.", 403)
handler400 = views.generic_error_view("Ta requête est incorrecte.", 400)

if DEBUG:  # https://docs.djangoproject.com/en/1.10/howto/static-files/#serving-files-uploaded-by-a-user-during-development
    import debug_toolbar

    urlpatterns += [
                       url(r'^__debug__/', include(debug_toolbar.urls)),
                   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
