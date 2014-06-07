from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^next_turn/$', 'tictactoe.views.play_next_turn'),
    url(r'^new_game/$', 'tictactoe.views.start_new_game'),
    url(r'^history/$', 'tictactoe.views.game_history'),
    url(r'^clear_history/$', 'tictactoe.views.clear_history'),
    url(r'^back_to_game/$', 'tictactoe.views.back_to_game'),
    url(r'^load_game/$', 'tictactoe.views.load_game'),
)
