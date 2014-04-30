from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', 'tictactoe.views.login'),
    url(r'^accounts/logout/$', 'tictactoe.views.logout'),
    url(r'^accounts/auth/$', 'tictactoe.views.auth_view'),
    url(r'^accounts/loggedin/$', 'tictactoe.views.loggedin'),
    url(r'^accounts/register/$', 'tictactoe.views.register_user'),
    url(r'^accounts/register_success/$', 'tictactoe.views.register_success/$'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tictactoe/', include('tictactoe.urls')),
)
