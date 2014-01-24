from django.conf.urls import patterns, include, url

urlpatterns = patterns('',

    url(r'^$',              'gguru.views.main'),
    url( r'^login/$',       'gguru.views.login' ),
    url( r'^logout/$',      'gguru.views.logout' ),

    url( r'^groups/$',                  'gguru.views.groups' ),
    url( r'^groups/add/$',              'gguru.views.groups_add' ),
    url( r'^groups/edit/(?P<id>\d+)/$', 'gguru.views.groups_edit' ),
    url( r'^groups/cud_ajax/',          'gguru.views.groups_cud_ajax' ),

    url( r'^members/$',                  'gguru.views.members' ),
    url( r'^members/add/$',              'gguru.views.members_add' ),
    url( r'^members/edit/(?P<id>\d+)/$', 'gguru.views.members_edit' ),
    url( r'^members/cud_ajax/',          'gguru.views.members_cud_ajax' ),

    url( r'^users/$',                    'gguru.views.users' ),
    url( r'^users/add/$',                'gguru.views.users_add' ),
    url( r'^users/edit/(?P<id>\d+)/$',   'gguru.views.users_edit' ),
    url( r'^users/cud_ajax/$',           'gguru.views.users_cud_ajax' ),
)

from django.conf import settings
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
