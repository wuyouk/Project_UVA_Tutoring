from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^course/$', views.course_info, name='course_info'),
    url(r'^course/(?P<pk>[0-9]+)/$', views.course_info, name='course_info'),
    url(r'^courses/$', views.courses_info, name='courses_info'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^listing/$', views.listing, name='listing'),
    url(r'^search/$', views.search, name='search')
) 

# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)