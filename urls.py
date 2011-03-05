from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/smorgasboard/'}),
	
	url(r'^smorgasboard/$', 'bom.views.index', name='board-change'),
	(r'^smorgasboard/board/$', 'bom.views.board'),
	(r'^smorgasboard/board/(?P<board_id>\d+)/$', 'bom.views.board'),
	url(r'^smorgasboard/parts/$', 'bom.views.parts', name='parts'),
	url(r'^smorgasboard/order/$', 'bom.views.order', name='order'),
	(r'^smorgasboard/order/(?P<order_id>\d+)/$', 'bom.views.order'),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)

# Static files
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^' + settings.STATIC_PATH +'(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
	)

