from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from pwd_mgr.views import add_user

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/$', 'pwd_mgr.views.login'),
    url(r'^accounts/logout/$', 'pwd_mgr.views.logout'),
    url(r'^accounts/auth/$', 'pwd_mgr.views.auth_view'),
    url(r'^accounts/loggedin/$', 'pwd_mgr.views.loggedin'),
    url(r'^accounts/register/$', 'pwd_mgr.views.register_user'),
    url(r'^accounts/register_success/$', 'pwd_mgr.views.register_success'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pwd_mgr/', include('pwd_mgr.urls')),
)
